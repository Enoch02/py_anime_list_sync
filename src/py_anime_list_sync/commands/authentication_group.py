import click
import requests.exceptions

from ..utils.console import console
from ..utils.constants import AVAILABLE_TRACKERS
from ..logic.authentication import authenticate_tracker, get_authenticated_accounts
from rich.table import Table


@click.group(name="auth")
def commands():
    """Add or remove list tracking services"""
    pass


@commands.command()
@click.option(
    "--tracker",
    type=click.Choice(AVAILABLE_TRACKERS, case_sensitive=False),
    help="Add a new list tracker account",
)
def add_tracker(tracker: str):
    """Add new Anime list service"""
    authenticated = None

    if tracker is None:
        console.print("You have not selected a tracker", style="warning")
        tracker = click.prompt(
            text="Select a sync service",
            type=click.Choice(AVAILABLE_TRACKERS, case_sensitive=False),
        )
        authenticated = authenticate_tracker(tracker)
    else:
        authenticated = authenticate_tracker(tracker)

    if authenticated:
        console.print("Authentication successful", style="msg")
        console.print("Run [italic]alsync auth whoami[/italic] to view authenticated accounts", style="msg")
    else:
        console.print("Authentication failed", style="error")


# TODO: add then list multiple accounts from the same service
@commands.command()
def whoami():
    """List the currently authenticated accounts"""
    table = Table(title="Authenticated Accounts")
    table.add_column("Tracker", justify="center", style="blue")
    table.add_column("Account Name", justify="center")

    try:
        with console.status("Loading accounts..", spinner="earth"):
            for account in get_authenticated_accounts():
                table.add_row(account.tracker, account.account_name)
                console.print(table)
    except requests.exceptions.ConnectionError:
        console.print("Alsync could not connect to the server 😔", style="error")
        console.print("Check your internet connection and try again", style="info")
