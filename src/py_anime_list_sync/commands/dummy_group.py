import click
from ..utils.console import console
import time


@click.group(name="dummy")
def commands():
    """Dummy commands that serve no purpose!"""
    pass


@commands.command()
@click.option("--duration", type=int, help="How long should nothing load for?")
def load_nothing(duration: int):
    """Shows a cool progress indicator (maybe it does something?)"""
    with console.status("Something great is coming", spinner="earth"):
        time.sleep(duration)
