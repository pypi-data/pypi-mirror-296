#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import signal
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import typer
from pathlib import Path
import concurrent.futures
from requests.adapters import HTTPAdapter
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from urllib3.util.retry import Retry
from typing import Optional, Dict
from rich.progress import Progress, TaskID, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
from rich.console import Console, Group

# Constants
MAX_CACHE_SIZE = 2 ** 27  # 128MB
HF_OFFICIAL_URL = 'https://huggingface.co'
HF_MIRROR_URL = 'https://hf-mirror.com'

app = typer.Typer(help="Hugging Face model download tool")
console = Console()

# 全局变量来控制下载
stop_download = False

def signal_handler(signum, frame):
    global stop_download
    stop_download = True
    console.print("\n[bold red]Interrupting download. Please wait for ongoing operations to complete...[/bold red]")

signal.signal(signal.SIGINT, signal_handler)

class Config:
    hf_endpoint: str = HF_MIRROR_URL

config = Config()

def check_url_availability(url: str, fallback_url: str, error_msg: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise requests.exceptions.RequestException
    except requests.exceptions.RequestException:
        console.print(error_msg, style="bold red")
        config.hf_endpoint = fallback_url

def check_hfmirror_availability():
    check_url_availability(
        HF_MIRROR_URL,
        HF_OFFICIAL_URL,
        f"警告： HF-mirror镜像网站异常=【{HF_MIRROR_URL}】，切换为huggingface官网地址[{HF_OFFICIAL_URL}]"
    )

def check_huggingface_availability():
    check_url_availability(
        HF_OFFICIAL_URL,
        None,
        f"警告：huggingface官网地址访问异常[{HF_OFFICIAL_URL}]，请检查网络或者代理是否正常"
    )
    if config.hf_endpoint is None:
        sys.exit(1)

def get_remote_file_size(url: str) -> int:
    session = get_requests_retry_session()
    try:
        response = session.head(url, allow_redirects=True)
        return int(response.headers['Content-Length'])
    except KeyError:
        return get_file_size_by_download(url)
    except Exception:
        return -1

def get_file_size_by_download(url: str) -> int:
    session = get_requests_retry_session()
    response = session.get(url, stream=True, timeout=60)
    size = 0
    for chunk in response.iter_content(8192):
        if chunk:
            if size <= MAX_CACHE_SIZE:
                size += len(chunk)
            else:
                return size
    return size

def check_disk_space(file_size: int, filename: str, url: str):
    if os.name != 'posix':
        return

    dir_path = os.getcwd()
    stat = os.statvfs(dir_path)
    free_space = stat.f_bavail * stat.f_frsize
    free_space_mb = free_space / (1024 * 1024)

    if free_space > 0 and free_space - file_size < 1024 * 1024 * 1024:
        console.print(f"警告: 磁盘空间不足1GB，无法安全下载文件。fileName:{filename},url:{url},free_space:{free_space_mb}MB", style="bold red")
        sys.exit(1)

def get_requests_retry_session(retries: int = 3, backoff_factor: float = 0.3,
                               status_forcelist: tuple = (500, 502, 504, 404),
                               session: Optional[requests.Session] = None) -> requests.Session:
    session = session or requests.Session()
    retry = Retry(total=retries, read=retries, connect=retries,
                  backoff_factor=backoff_factor, status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def get_hfd_file_path() -> Path:
    cache_path = Path.home() / ".cache" / "huggingface" / "hub" / 'hfd'
    cache_path.mkdir(parents=True, exist_ok=True)
    return cache_path

@app.command("download", help="Download a Hugging Face model and save it locally.")
def download_model(
        ctx: typer.Context,
        model_id: str = typer.Argument(..., help='The id of the model, example: Intel/dynamic_tinybert'),
        max_workers: int = typer.Option(5, help='Maximum number of concurrent downloads')
):
    """
    Download a Hugging Face model and save it locally.
    """
    global stop_download
    stop_download = False

    model_dir = model_id.split('/')[-1]
    repo_url = f"{config.hf_endpoint}/{model_id}"

    model_cache_local_path = get_hfd_file_path()
    os.chdir(model_cache_local_path)
    download_dir = model_cache_local_path / model_dir
    download_dir.mkdir(exist_ok=True)

    api_url = f"{config.hf_endpoint}/api/models/{model_id}"
    response = requests.get(api_url)
    if response.status_code != 200:
        console.print(f"无法访问模型API: {response.status_code}", style="bold red")
        return

    model_data = response.json()
    file_names = [file['rfilename'] for file in model_data.get('siblings', [])]

    if not file_names:
        console.print(f"未找到任何文件在模型 {model_id} 中。", style="bold red")
        return

    download_url = f"{config.hf_endpoint}/{model_id}"

    overall_progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    )
    file_progress = Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        DownloadColumn(),
        TransferSpeedColumn(),
        expand=True
    )

    overall_task = overall_progress.add_task(f"[cyan]Overall Progress", total=len(file_names))
    file_tasks: Dict[str, TaskID] = {
        filename: file_progress.add_task(f"[green]{filename}", visible=False, total=100)
        for filename in file_names
    }

    layout = Layout()
    layout.split(
        Layout(Panel(overall_progress, title="Overall Progress", border_style="cyan"), size=3),
        Layout(Panel(file_progress, title="File Progress", border_style="green"))
    )

    def download_file(filename):
        if stop_download:
            return

        url = f"{download_url}/resolve/main/{filename}"
        download_path = download_dir / filename

        # 确保文件的父目录存在
        download_path.parent.mkdir(parents=True, exist_ok=True)

        file_progress.update(file_tasks[filename], visible=True)

        if download_path.exists():
            local_file_size = download_path.stat().st_size
            remote_file_size = get_remote_file_size(url)
            if local_file_size < remote_file_size:
                file_progress.update(file_tasks[filename], completed=local_file_size, total=remote_file_size)
                download_file_with_range(file_progress, file_tasks[filename], url, str(download_path), local_file_size,
                                         remote_file_size)
            elif remote_file_size == -1:
                download_file_simple(file_progress, file_tasks[filename], url, str(download_path))
            elif local_file_size == remote_file_size:
                file_progress.update(file_tasks[filename], completed=remote_file_size, total=remote_file_size)
            else:
                file_progress.update(file_tasks[filename], completed=local_file_size, total=local_file_size)
        else:
            download_file_simple(file_progress, file_tasks[filename], url, str(download_path))

        overall_progress.update(overall_task, advance=1)

    with Live(layout, console=console, refresh_per_second=10, vertical_overflow="visible") as live:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(download_file, filename) for filename in file_names]
            for future in concurrent.futures.as_completed(futures):
                if stop_download:
                    executor.shutdown(wait=False)
                    break
                future.result()  # This will raise any exceptions that occurred during download

    if stop_download:
        console.print("[bold yellow]Download interrupted by user.[/bold yellow]")
    else:
        console.print(f"Model {model_id} downloaded successfully.", style="bold green")


def download_file_with_range(progress: Progress, task_id: TaskID, url: str, filename: str, start_byte: int,
                             total_size: int):
    headers = {'Range': f'bytes={start_byte}-'}
    response = requests.get(url, headers=headers, stream=True)

    with open(filename, 'ab') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if stop_download:
                return
            if chunk:
                f.write(chunk)
                progress.update(task_id, advance=len(chunk))


def download_file_simple(progress: Progress, task_id: TaskID, url: str, filename: str):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))

    progress.update(task_id, total=total_size)
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if stop_download:
                return
            if chunk:
                f.write(chunk)
                progress.update(task_id, advance=len(chunk))