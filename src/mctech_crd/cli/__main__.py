from mctech_crd.cosmic import listen as crd_listen

"""Command-line interface."""
from mctech_crd import __version__
from pathlib import Path
import click
import subprocess
import sys
import logging

import os.path
import json
from pathlib import PurePath

logging.basicConfig(level=logging.INFO, format="%(message)s")

script_dir = PurePath(os.path.dirname(__file__)).parent.joinpath("shell")

INIT_ENV_PATH = script_dir.joinpath("init.sh")
UPDATE_PACKAGE_PATH = script_dir.joinpath("utils/update_package.sh")
UPDATE_PYENV_PATH = script_dir.joinpath("utils/update_pyenv.sh")
GH_GET_RELEASE = script_dir.joinpath("utils/get_latest_release.sh")

# os.path.normpath(os.path.join(script_dir, rel_path))


def get_latest_release_version():
    try:
        release = json.loads(subprocess.check_output(["bash", "-c", GH_GET_RELEASE]))
        return release.get("tag_name", None).removeprefix("v")
    except:
        return None


@click.group()
def cli():
    pass


@cli.command(name="listen")
@click.option("--config", envvar="COSMIC_CONFIG")
def listen(config):
    click.echo("Listening for cosmic ray detector events")
    # TODO: ensure service is not already running
    # sudo systemctl stop cosmicservice
    # TODO: ensure command is not already running
    crd_listen(config)


@cli.command(
    name="update", help="Update python package/environment for cosmic detector"
)
@click.option(
    "--force", "-f", is_flag=True, help="Update package even if have latest release"
)
@click.option(
    "--pyenv",
    is_flag=True,
    help="Update python environment based on ~/cosmic/.cosmic/.python-version",
)
def update(force, pyenv):
    # UPDATE PYTHON ENVIRONMENT (PYENV)
    if pyenv:
        cosmic_root = os.environ.get("COSMIC_ROOT", "")
        if not cosmic_root:
            click.echo("Could not locate COSMIC_ROOT")
            sys.exit(1)

        target_python_venv = f"{cosmic_root}/.python-version"
        if not os.path.exists(target_python_venv):
            click.echo(f"Could not find {target_python_venv}")
            sys.exit(1)

        with open(target_python_venv) as python_version_file:
            venv_name = python_version_file.readline()
            os.environ["COSMIC_VIRTUALENV"] = venv_name
            os.environ["COSMIC_PYTHON_VERSION"] = venv_name.split("-")[-1].strip()

        try:
            subprocess.run(["bash", "-c", UPDATE_PYENV_PATH], check=True)
        except:
            click.echo("Did not update python environment")
            sys.exit(1)

        click.echo("Python version updated for virtualenv (pyenv)")
        sys.exit(0)

    # UPDATE PYTHON PACKAGE
    click.echo("Updating cosmic ray detection client")
    if get_latest_release_version() == __version__ and not force:
        click.echo("Latest version already installed")
        return

    try:
        subprocess.run(["bash", "-c", UPDATE_PACKAGE_PATH], check=True)
    except:
        click.echo("Could not update cosmic ray detection client")


# TODO: this may no longer be required, as we run init.sh from .bashrc
@cli.command(name="env")
@click.option(
    "--target", is_flag=True, help="Get current or target environment name $COSMIC_ROOT"
)
@click.pass_context
def env(ctx, target):
    """
    Informs $COSMIC_ROOT/.python-version, which informs update_pyenv
    """
    if target:
        try:
            version_file_src = Path(os.path.dirname(__file__)).resolve().parent
            version_file = os.path.join(version_file_src, "shell/.python-version")
            with open(version_file) as python_version_file:
                click.echo(python_version_file.readline())
        except:
            ctx.exit(1)

        ctx.exit(0)

    # else return current env


@cli.command(name="boot")
@click.pass_context
def boot(ctx):
    """
    Return path for cosmic boot.sh cript to stdout

    This allows the service to run the shell script direct and set environment
    variables
    """
    package_dir = Path(os.path.dirname(__file__)).resolve().parent
    boot_script_path = os.path.join(package_dir, "shell/boot.sh")

    print(boot_script_path)
    ctx.exit(0)


@cli.command(name="login")
@click.pass_context
def login(ctx):
    """
    Return path for cosmic login.sh cript to stdout

    This allows .bashrc to run the shell script direct and set environment
    variables
    """
    package_dir = Path(os.path.dirname(__file__)).resolve().parent
    login_script = os.path.join(package_dir, "shell/login.sh")

    print(login_script)
    ctx.exit(0)


@cli.command(name="version")
@click.option("--latest", is_flag=True, help="Check if cosmic package is up to date")
def version(latest):
    if latest:
        if latest_release := get_latest_release_version():
            print(f"latest:    {latest_release}")
            print(f"installed: {__version__}")

            if latest_release == __version__:
                print("up to date")
                sys.exit(0)

            sl = latest_release.split(".")  # latest release semver
            sc = __version__.split(".")  # current release semver
            # Check if running a minor version greater than latest release (ie dev)
            if sc[0] == sl[0] and sc[1] == sl[1] and int(sc[2]) > int(sl[2]):
                sys.exit(0)

        sys.exit(1)
    click.echo(__version__)


# @cli.command(name="start")
# @click.pass_context
# def start(ctx):
#     click.echo("Starting cosmic ray detection client")
#     ctx.invoke(update)
#     ctx.invoke(listen)


if __name__ == "__main__":
    cli()
