import json

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
                tracker="MAL",
                account_name=user_info["name"]
            )
        )

    return authenticated_accounts
