import json
import requests.exceptions

from rich.table import Table
from .mal_authentication import add_mal_account, get_user_info
from ..utils.constants import AVAILABLE_TRACKERS
from ..utils.console import console
from ..utils.models import AuthenticatedAccount


def authenticate_tracker(tracker: str) -> bool:
    if tracker == AVAILABLE_TRACKERS[0]:
        return add_mal_account()
    elif tracker == AVAILABLE_TRACKERS[1]:
        console.print("Anilist coming soon...")
        return False


def get_authenticated_accounts() -> list[AuthenticatedAccount]:
    authenticated_accounts = []

    with open("mal_token.json", "r") as file:
        token = json.load(file)
        user_info = get_user_info(token["access_token"])
        authenticated_accounts.append(
            AuthenticatedAccount(
                id=1,
                tracker="MAL",
                account_name=user_info["name"]
            )
        )

    return authenticated_accounts


def list_authenticated_accounts() -> None:
    table = Table(title="Authenticated Accounts")
    table.add_column("Tracker", justify="center", style="blue")
    table.add_column("Account Name", justify="center")
    table.add_column("ID", justify="center")

    try:
        with console.status("Loading accounts..", spinner="earth"):
            for account in get_authenticated_accounts():
                table.add_row(account.tracker, account.account_name, str(account.id))
                console.print(table)
    except requests.exceptions.ConnectionError:
        console.print("Alsync could not connect to the server 😔", style="error")
        console.print("Check your internet connection and try again", style="info")
