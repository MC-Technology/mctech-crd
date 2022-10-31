"""Command-line interface."""
from mctech_crd.cosmic import listen as crd_listen
from mctech_crd import __version__
from pathlib import Path
import click
import subprocess
import sys
import logging

import os.path
import json
from pathlib import PurePath

logging.basicConfig(level=logging.INFO, format='%(message)s')

script_dir = PurePath(os.path.dirname(__file__)).parent.joinpath("shell")

INIT_ENV_PATH = script_dir.joinpath("init.sh")
UPDATE_SCRIPT_PATH = script_dir.joinpath("update.sh")
GET_RELEASE = script_dir.joinpath("get_latest_release.sh")

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
@click.option('--config', envvar='COSMIC_CONFIG')
def listen(config):
    click.echo("Listening for cosmic ray detector events")
    crd_listen(config)


@cli.command(name="update")
@click.option('--force', '-f', is_flag=True, help="Update package even if have latest release")
def update(force):
    # TODO: This manual checking unnecessary if move to PyPi package
    click.echo("Updating cosmic ray detection client")
    if not force and get_latest_release_version() == __version__:
        click.echo("Latest version already installed")
        return

    try:
        subprocess.run(["bash", "-c", UPDATE_SCRIPT_PATH], check=True)
    except:
        click.echo("Could not update cosmic ray detection client")


# TODO: this may no longer be required, as we run init.sh from .bashrc
@cli.command(name="env")
@click.pass_context
def env(ctx):
    """
    Setup a python version and return name to stdout
    """
    # TODO: Unnecessary if move to PyPi package
    try:
        cosmic_venv = subprocess.check_output(["bash", "-c", INIT_ENV_PATH]).decode("utf-8").strip()
        print(cosmic_venv)
    except:
        ctx.exit(1)

    ctx.exit(0)


@cli.command(name="init")
@click.pass_context
def init(ctx):
    """
    Return path for cosmic init.sh cript to stdout

    This allows the bashrc to run the shell script direct and set environment
    variables
    """
    package_dir = Path(os.path.dirname(__file__)).resolve().parent
    init_script = os.path.join(package_dir, "shell/init.sh")

    print(init_script)
    ctx.exit(0)


@cli.command(name="version")
def version():
    click.echo(__version__)


@cli.command(name="start")
@click.pass_context
def start(ctx):
    click.echo("Starting cosmic ray detection client")
    ctx.invoke(update)
    ctx.invoke(listen)


if __name__ == "__main__":
    cli()
