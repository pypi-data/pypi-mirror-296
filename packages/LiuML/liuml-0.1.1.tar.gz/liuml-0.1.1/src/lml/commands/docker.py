import configparser
import os
import threading

import rich
import typer
import requests
import tarfile
import json
import gzip
import shutil
import hashlib
import urllib3
import signal
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, TextColumn, BarColumn, TaskID, DownloadColumn, TransferSpeedColumn
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout

# Disable SSL warnings
urllib3.disable_warnings()

console = Console()
app = typer.Typer(help="Docker related commands")

# Global flag to control download
stop_download = False


def signal_handler(signum, frame):
    global stop_download
    stop_download = True
    console.print("\n[bold red]Interrupting download. Please wait for ongoing operations to complete...[/bold red]")


signal.signal(signal.SIGINT, signal_handler)


print_lock = threading.Lock()

def log(message: str, style: str = None):
    """Log messages with optional style."""
    with print_lock:
        rich.print(f"[{style}]{message}[/{style}]" if style else message)

@app.command("pull")
def pull_docker_image(
        ctx: typer.Context,
        image_name: str = typer.Argument(..., help="Docker image name to pull"),
        registry: str = typer.Option(None, help="Docker registry to use")
):
    """
    Pull a Docker image and save it as a tar file.

    IMAGE_NAME should be in the format [repository/]image[:tag|@digest]
    """
    config: configparser.ConfigParser = ctx.obj

    # If registry is not provided, try to get it from the config
    if registry is None:
        registry = config['Docker']['registry'] if config.has_section('Docker') and 'registry' in config['Docker'] else "registry-1.docker.io"

    global stop_download
    stop_download = False

    try:
        repository, image, tag = parse_image_name(image_name)

        auth_url, reg_service = get_auth_info(registry)
        auth_head = get_auth_header(auth_url, reg_service, repository, image)

        manifest = get_manifest(registry, repository, image, tag, auth_head)
        if not manifest:
            return

        layers = manifest['layers']
        config_digest = manifest['config']['digest']

        img_dir, content = create_image_structure(image, tag, config_digest, auth_head, registry, repository)

        # Fetch the config file
        config_resp = requests.get(f'https://{registry}/v2/{repository}/{image}/blobs/{config_digest}',
                                   headers=auth_head,
                                   verify=False)
        config = json.loads(config_resp.content)

        download_layers(layers, img_dir, auth_head, registry, repository, image, content, config)

        if not stop_download:
            create_tar_archive(img_dir, repository, image)
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")
        raise typer.Exit(1)


def parse_image_name(image_name):
    """Parse the image name into repository, image, and tag components."""
    parts = image_name.split('/')
    if len(parts) == 1:
        repository = 'library'
        image_and_tag = parts[0]
    else:
        repository = '/'.join(parts[:-1])
        image_and_tag = parts[-1]

    if '@' in image_and_tag:
        image, tag = image_and_tag.split('@')
    elif ':' in image_and_tag:
        image, tag = image_and_tag.split(':')
    else:
        image = image_and_tag
        tag = 'latest'

    return repository, image, tag


def get_auth_info(registry):
    """Get authentication information for the registry."""
    resp = requests.get(f'https://{registry}/v2/', verify=False)
    if resp.status_code == 401:
        auth_url = resp.headers['WWW-Authenticate'].split('"')[1]
        try:
            reg_service = resp.headers['WWW-Authenticate'].split('"')[3]
        except IndexError:
            reg_service = ""
    else:
        auth_url = 'https://auth.docker.io/token'
        reg_service = 'registry.docker.io'
    return auth_url, reg_service


def get_auth_header(auth_url, reg_service, repository, image):
    """Get the authentication header for API requests."""
    resp = requests.get(f'{auth_url}?service={reg_service}&scope=repository:{repository}/{image}:pull', verify=False)
    access_token = resp.json()['token']
    return {'Authorization': f'Bearer {access_token}', 'Accept': 'application/vnd.docker.distribution.manifest.v2+json'}


def get_manifest(registry, repository, image, tag, auth_head):
    """Fetch the manifest for the specified image."""
    resp = requests.get(f'https://{registry}/v2/{repository}/{image}/manifests/{tag}', headers=auth_head, verify=False)
    if resp.status_code != 200:
        log(f'Cannot fetch manifest for {repository}/{image} [HTTP {resp.status_code}]', style="bold red")
        return None
    return resp.json()


def create_image_structure(image, tag, config, auth_head, registry, repository):
    """Create the directory structure for the image and save config."""
    img_dir = f'tmp_{image}_{tag.replace(":", "@")}'
    os.makedirs(img_dir, exist_ok=True)
    log(f'Creating image structure in: {img_dir}', style="blue")

    config_resp = requests.get(f'https://{registry}/v2/{repository}/{image}/blobs/{config}', headers=auth_head,
                               verify=False)
    with open(f'{img_dir}/{config[7:]}.json', 'wb') as f:
        f.write(config_resp.content)

    content = [{
        'Config': f'{config[7:]}.json',
        'RepoTags': [f'{repository}/{image}:{tag}'],
        'Layers': []
    }]

    with open(f'{img_dir}/manifest.json', 'w') as f:
        json.dump(content, f)

    return img_dir, content


def download_and_extract_layer(progress: Progress, layer_tasks: Dict[str, TaskID], registry: str, repository: str,
                               image: str, ublob: str, layer_dir: str, auth_head: dict, diff_id: str):
    """Download and extract a single layer with progress bar and verify diff_id."""
    global stop_download

    resp = requests.get(f'https://{registry}/v2/{repository}/{image}/blobs/{ublob}',
                        headers=auth_head, stream=True, verify=False)
    if resp.status_code != 200:
        raise Exception(f'Cannot download layer {ublob[7:19]} [HTTP {resp.status_code}]')

    total_size = int(resp.headers.get('content-length', 0))

    layer_tasks[ublob] = progress.add_task(f"[green]Downloading {ublob[7:19]}", total=total_size)

    downloaded_hash = hashlib.sha256()
    with open(os.path.join(layer_dir, 'layer_gzip.tar'), 'wb') as f:
        for data in resp.iter_content(chunk_size=8192):
            if stop_download:
                return
            if data:
                size = f.write(data)
                downloaded_hash.update(data)
                progress.update(layer_tasks[ublob], advance=size)

    if stop_download:
        return

    # Verify the downloaded layer's hash
    if downloaded_hash.hexdigest() != ublob[7:]:
        progress.update(layer_tasks[ublob], description=f"[red]Hash mismatch {ublob[7:19]}")
        os.remove(os.path.join(layer_dir, 'layer_gzip.tar'))
        return download_and_extract_layer(progress, layer_tasks, registry, repository, image, ublob, layer_dir, auth_head, diff_id)

    progress.update(layer_tasks[ublob], description=f"[yellow]Extracting {ublob[7:19]}")

    extracted_hash = hashlib.sha256()
    with gzip.open(os.path.join(layer_dir, 'layer_gzip.tar'), 'rb') as gz_file:
        with open(os.path.join(layer_dir, 'layer.tar'), 'wb') as tar_file:
            while True:
                chunk = gz_file.read(8192)
                if not chunk:
                    break
                extracted_hash.update(chunk)
                tar_file.write(chunk)

    # Verify the extracted layer's hash (diff_id)
    if extracted_hash.hexdigest() != diff_id[7:]:
        progress.update(layer_tasks[ublob], description=f"[red]Diff ID mismatch {ublob[7:19]}")
        os.remove(os.path.join(layer_dir, 'layer_gzip.tar'))
        os.remove(os.path.join(layer_dir, 'layer.tar'))
        return download_and_extract_layer(progress, layer_tasks, registry, repository, image, ublob, layer_dir, auth_head, diff_id)

    os.remove(os.path.join(layer_dir, 'layer_gzip.tar'))

    progress.update(layer_tasks[ublob], description=f"[blue]Completed {ublob[7:19]}")

def process_layer(layer: dict, img_dir: str, auth_head: dict, registry: str, repository: str, image: str,
                  overall_progress: Progress, overall_task: TaskID, layer_progress: Progress, layer_tasks: Dict[str, TaskID],
                  parent_id: str, diff_id: str):
    """Process a single layer."""
    if stop_download:
        return None, None

    ublob = layer['digest']
    fake_layer_id = hashlib.sha256(f'{parent_id}\n{ublob}\n'.encode('utf-8')).hexdigest()
    layer_dir = os.path.join(img_dir, fake_layer_id)
    os.makedirs(layer_dir, exist_ok=True)

    with open(os.path.join(layer_dir, 'VERSION'), 'w') as f:
        f.write('1.0')

    download_and_extract_layer(layer_progress, layer_tasks, registry, repository, image, ublob, layer_dir,
                               auth_head, diff_id)

    create_layer_json(layer_dir, fake_layer_id, parent_id)

    overall_progress.update(overall_task, advance=1)
    return fake_layer_id, f'{fake_layer_id}/layer.tar'

def download_layers(layers: List[dict], img_dir: str, auth_head: dict, registry: str, repository: str, image: str,
                    content: List[dict], config: dict):
    """Download and extract all layers of the image using multiple threads."""
    parent_id = ''

    overall_progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    )
    layer_progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        DownloadColumn(),
        TransferSpeedColumn(),
        expand=True
    )

    overall_task = overall_progress.add_task("[cyan]Overall progress", total=len(layers))
    layer_tasks: Dict[str, TaskID] = {}

    layout = Layout()
    layout.split(
        Layout(Panel(overall_progress, title="Overall Progress", border_style="cyan"), size=3),
        Layout(Panel(layer_progress, title="Layer Progress", border_style="green"))
    )

    with Live(layout, console=console, refresh_per_second=10):
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_layer, layer, img_dir, auth_head, registry, repository, image,
                                       overall_progress, overall_task, layer_progress, layer_tasks, parent_id, config['rootfs']['diff_ids'][i])
                       for i, layer in enumerate(layers)]
            for future in as_completed(futures):
                if stop_download:
                    executor.shutdown(wait=False)
                    break
                try:
                    fake_layer_id, layer_info = future.result()
                    if fake_layer_id and layer_info:
                        content[0]['Layers'].append(layer_info)
                        parent_id = fake_layer_id
                except Exception as exc:
                    console.print(f"Layer download failed: {exc}", style="bold red")

    if not stop_download:
        # Save updated manifest.json
        with open(f'{img_dir}/manifest.json', 'w') as f:
            json.dump(content, f)


def create_layer_json(layer_dir, layer_id, parent_id):
    """Create the JSON file for a layer."""
    json_data = {
        "id": layer_id,
        "parent": parent_id if parent_id else None,
        "created": "1970-01-01T00:00:00Z",
        "container_config": {
            "Hostname": "",
            "Domainname": "",
            "User": "",
            "AttachStdin": False,
            "AttachStdout": False,
            "AttachStderr": False,
            "Tty": False,
            "OpenStdin": False,
            "StdinOnce": False,
            "Env": None,
            "Cmd": None,
            "Image": "",
            "Volumes": None,
            "WorkingDir": "",
            "Entrypoint": None,
            "OnBuild": None,
            "Labels": None
        }
    }

    with open(os.path.join(layer_dir, 'json'), 'w') as f:
        json.dump(json_data, f)


def create_tar_archive(img_dir: str, repository: str, image: str):
    """Create the final tar archive of the image."""
    docker_tar = f'{repository.replace("/", "_")}_{image}.tar'
    console.print(f"Creating archive {docker_tar}...", style="yellow")
    with tarfile.open(docker_tar, "w") as tar:
        tar.add(img_dir, arcname=os.path.sep)
    shutil.rmtree(img_dir)
    console.print(f'Docker image pulled: {docker_tar}', style="green")
