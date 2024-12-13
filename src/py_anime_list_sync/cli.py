import click
from rich.console import Console
from .commands import dummy_group, authentication_group
from .utils.console import console


@click.group()
@click.version_option()
def cli():
    """Anime list syncing tool"""
    pass


# noinspection PyTypeChecker
cli.add_command(dummy_group.commands)
# noinspection PyTypeChecker
cli.add_command(authentication_group.commands)

if __name__ == "__main__":
    cli()
