"""Command-line interface."""
from mctech_crd.cosmic import listen as crd_listen

import click


@click.group()
def cli():
    pass


@cli.command(name="listen")
def listen():
    click.echo("Listening for cosmic ray detector events")
    crd_listen()


@cli.command(name="update")
def welcome():
    click.echo("Updating cosmic ray detection client")


if __name__ == "__main__":
    cli()
