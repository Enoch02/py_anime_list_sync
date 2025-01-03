import click

from ..utils.console import console
from ..utils.constants import AVAILABLE_TRACKERS
from ..logic.authentication import (
    authenticate_tracker,
    list_authenticated_accounts,
    remove_authenticated_account,
)


@click.group(name="auth")
def commands():
    """Add or remove list tracking services"""
    pass


@commands.command()
@click.option(
    "--tracker",
    type=click.Choice(AVAILABLE_TRACKERS, case_sensitive=False),
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
        console.print(
            "Run [italic]alsync auth whoami[/italic] to view authenticated accounts",
            style="msg",
        )
    else:
        console.print("Authentication failed", style="error")


@commands.command()
@click.argument("account_id", type=int)
def remove_tracker(account_id: int):
    """Remove a Anime list tracker account"""
    if remove_authenticated_account(account_id):
        console.print("Account removed", style="msg")
    else:
        console.print("Account not found or does not exist", style="warning")


# TODO: add then list multiple accounts from the same service
@commands.command()
def whoami():
    """List the currently authenticated accounts"""
    list_authenticated_accounts()
