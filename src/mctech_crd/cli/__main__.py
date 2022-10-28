"""Command-line interface."""
from mctech_crd.cosmic import listen as crd_listen
from mctech_crd import __version__

import click
import subprocess

import os.path
from pathlib import PurePath

UPDATE_SCRIPT_PATH = PurePath(os.path.dirname(__file__)).parent.joinpath("shell/update.sh")

# os.path.normpath(os.path.join(script_dir, rel_path))

@click.group()
def cli():
    pass


@cli.command(name="listen")
def listen():
    click.echo("Listening for cosmic ray detector events")
    crd_listen()


@cli.command(name="update")
def update():
    click.echo("Updating cosmic ray detection client")
    try:
        subprocess.run(["bash", "-c", UPDATE_SCRIPT_PATH], check=True)
    except:
        import pudb; pu.db

@cli.command(name="version")
def version():
    click.echo(__version__)

if __name__ == "__main__":
    cli()
