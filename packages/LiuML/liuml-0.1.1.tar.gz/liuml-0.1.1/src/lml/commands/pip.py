#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import subprocess
from typing import List

import click
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

app = typer.Typer(help="Package installation commands")
console = Console()

MIRRORS = {
    "tuna": "https://pypi.tuna.tsinghua.edu.cn/simple",
    "aliyun": "https://mirrors.aliyun.com/pypi/simple",
    "ustc": "https://pypi.mirrors.ustc.edu.cn/simple",
    "douban": "https://pypi.douban.com/simple",
    "huawei": "https://mirrors.huaweicloud.com/repository/pypi/simple",
    "pypi": "https://pypi.org/simple",
}


@app.command("install")
def install(
        ctx: typer.Context,
        packages: List[str] = typer.Argument(None, help="Packages to install"),
        mirror: str = typer.Option("tuna", help="Mirror to use for installation",
                                   click_type=click.Choice(list(MIRRORS.keys())))
):
    if not packages:
        console.print("[bold red]Error:[/bold red] No packages specified for installation.")
        raise typer.Exit(code=1)

    mirror_url = MIRRORS.get(mirror)
    cmd = ["pip", "install", "-i", mirror_url] + packages
    cmd_text = " ".join(cmd)

    console.print(Panel(
        Syntax(cmd_text, "bash", theme="monokai", line_numbers=True),
        title="Installation Command",
        border_style="green"
    ))

    with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
    ) as progress:
        task = progress.add_task("[cyan]Installing packages...", total=None)
        try:
            result = subprocess.run(cmd, env=dict(os.environ),
                                    capture_output=True, text=True, check=True)
            progress.update(task, completed=True)
            console.print("[bold green]Installation completed successfully![/bold green]")
            console.print(Panel(result.stdout, title="Installation Output", border_style="blue"))
        except subprocess.CalledProcessError as e:
            progress.update(task, completed=True)
            console.print("[bold red]Installation failed![/bold red]")
            console.print(Panel(e.stdout, title="Error Output", border_style="red"))
            console.print(Panel(e.stderr, title="Error Details", border_style="red"))
            raise typer.Exit(code=1)
