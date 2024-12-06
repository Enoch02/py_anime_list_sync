"""Console script for py_anime_list_sync."""

import py_anime_list_sync

import click
from rich.console import Console

console = Console()


@click.command()
def main():
    """Console script for py_anime_list_sync."""
    console.print(
        "Replace this message by putting your code into " "py_anime_list_sync.cli.main"
    )
    console.print("See Typer documentation at https://typer.tiangolo.com/")


if __name__ == "__main__":
    app()
