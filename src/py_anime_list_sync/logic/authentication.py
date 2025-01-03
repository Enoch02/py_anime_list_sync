import json
import os
import requests.exceptions

from rich.table import Table
from .mal_logic import add_mal_account, get_user_info
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
        ds_json = json.load(file)
        user_info = get_user_info(ds_json["access_token"])
        authenticated_accounts.append(
            AuthenticatedAccount(
                id=1,
                tracker="MAL",
                account_name=user_info["name"],
                token=ds_json["access_token"],
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


def remove_authenticated_account(id: int) -> bool:
    with console.status("Removing account..", spinner="dots"):
        try:
            authenticated_accounts = get_authenticated_accounts()
            acc_to_del = list(filter(lambda acc: acc.id == id, authenticated_accounts))

            if acc_to_del[0].tracker == "MAL":
                os.remove("mal_token.json")
            return True
        except FileNotFoundError:
            return False
        except PermissionError:
            return False
        except Exception as e:
            console.print(f"An error occurred: {e}", style="error")
            return False
