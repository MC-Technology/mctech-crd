"""Command-line interface."""
import click

@click.group()
def cli():
  pass


@cli.command(name='launch')
def launch():
    click.echo('Launching cosmic ray detection client')


@cli.command(name='update')
def welcome():
    click.echo('Updating cosmic ray detection client')

if __name__ == '__main__':
    cli()
