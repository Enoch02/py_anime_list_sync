"""Console script for py_anime_list_sync."""

import py_anime_list_sync

import click
from rich.console import Console
import time

console = Console()


@click.command()
def main():
    """Console script for py_anime_list_sync."""

    with console.status("Something great is coming", spinner="earth"):
        time.sleep(60)


if __name__ == "__main__":
    main()
