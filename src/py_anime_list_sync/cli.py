"""Console script for py_anime_list_sync."""
import py_anime_list_sync

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for py_anime_list_sync."""
    console.print("Replace this message by putting your code into "
               "py_anime_list_sync.cli.main")
    console.print("See Typer documentation at https://typer.tiangolo.com/")
    


if __name__ == "__main__":
    app()
