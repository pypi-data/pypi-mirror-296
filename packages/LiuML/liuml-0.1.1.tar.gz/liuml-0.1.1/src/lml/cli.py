"""Console script for lml."""
import typer
from lml.commands import docker, pip, huggingface
import configparser
import os

app = typer.Typer(help="LiMixLib (LML) is a collection of utility functions and toolkits for Python.")
config = typer.Typer(help="Configuration management")

# Define the config file path
CONFIG_FILE = os.path.expanduser("~/.lmlconfig")

def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    return config

def save_config(config: configparser.ConfigParser):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

@app.callback()
def main(ctx: typer.Context):
    """
    Callback to be executed before any command.
    """
    # Read the config and store it in the context
    ctx.obj = get_config()

@config.command("show")
def show_config(ctx: typer.Context):
    """Show the current configuration."""
    config = ctx.obj
    for section in config.sections():
        typer.echo(f"[{section}]")
        for key, value in config[section].items():
            typer.echo(f"{key} = {value}")
        typer.echo("")

@config.command("set")
def set_config(
    ctx: typer.Context,
    section: str = typer.Option(..., help="Configuration section"),
    key: str = typer.Option(..., help="Configuration key"),
    value: str = typer.Option(..., help="Configuration value")
):
    """Set a configuration value."""
    config = ctx.obj
    if not config.has_section(section):
        config.add_section(section)
    config[section][key] = value
    save_config(config)
    typer.echo(f"Configuration updated: [{section}] {key} = {value}")

@config.command("edit")
def open_config(ctx: typer.Context):
    """Open the configuration file."""
    typer.edit(CONFIG_FILE)

# Add subcommands with context
app.add_typer(config, name="config")
app.add_typer(docker.app, name="docker")
app.add_typer(pip.app, name="pip")
app.add_typer(huggingface.app, name="huggingface")

def run():
    app(obj={})

if __name__ == "__main__":
    run()