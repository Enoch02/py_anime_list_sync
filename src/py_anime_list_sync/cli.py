import click
from rich.console import Console
from .commands import dummy_group
from .utils.console import console


@click.group()
@click.version_option()
def cli():
    """My CLI App description"""
    pass


cli.add_command(dummy_group.commands)

if __name__ == "__main__":
    cli()
