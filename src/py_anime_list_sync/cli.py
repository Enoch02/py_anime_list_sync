import click

from .commands import dummy_group, authentication_group, library_group


@click.group()
@click.version_option()
def cli():
    """Anime list syncing tool"""
    pass


# noinspection PyTypeChecker
cli.add_command(dummy_group.commands)
# noinspection PyTypeChecker
cli.add_command(authentication_group.commands)
# noinspection PyTypeChecker
cli.add_command(library_group.commands)

if __name__ == "__main__":
    cli()
