"""Command-line interface."""
from mctech_crd.cosmic import listen as crd_listen
from mctech_crd import __version__

import click
import subprocess

import os.path
import json
from pathlib import PurePath

UPDATE_SCRIPT_PATH = PurePath(os.path.dirname(__file__)).parent.joinpath("shell/update.sh")
GET_RELEASE = PurePath(os.path.dirname(__file__)).parent.joinpath("shell/get_latest_release.sh")

# os.path.normpath(os.path.join(script_dir, rel_path))

def get_latest_release_version():
    try:
        release = json.loads(subprocess.check_output(["bash", "-c", GET_RELEASE]))
        return release.get("tag_name", None).removeprefix("v")
    except:
        return None

@click.group()
def cli():
    pass


@cli.command(name="listen")
def listen():
    click.echo("Listening for cosmic ray detector events")
    crd_listen()


@cli.command(name="update")
def update():
    # TODO: This manual checking unnecessary if move to PyPi package
    click.echo("Updating cosmic ray detection client")

    if get_latest_release_version() == __version__:
        click.echo("Latest version already installed")
        return

    try:
        subprocess.run(["bash", "-c", UPDATE_SCRIPT_PATH], check=True)
    except:
        click.echo("Could not update cosmic ray detection client")


@cli.command(name="version")
def version():
    click.echo(__version__)

if __name__ == "__main__":
    cli()
