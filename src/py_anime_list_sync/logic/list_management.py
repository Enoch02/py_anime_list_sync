import click
from rich.table import Table

from .mal_logic import get_mal_list
from ..logic.mal_logic import mal_get_anime_list, mal_get_anime_list_data
from ..utils.models import AuthenticatedAccount
from ..utils.console import console
from ..utils.constants import AVAILABLE_TRACKERS


def get_list_for(
    account: AuthenticatedAccount, sort: str, status: str, limit: int, verbose: bool
):
    """
    Handles getting anime lists from various services.

    Args:
        account (AuthenticatedAccount): an authenticated account
        sort (str): list sort order
        status (str): watch status of the items in the list
        limit (int): limit the amount of items to fetch

    Returns:

    """
    if account.tracker == AVAILABLE_TRACKERS[0]:
        get_mal_list(account, sort, status, limit, verbose)

    elif account.tracker == AVAILABLE_TRACKERS[1]:
        console.print("Coming soon!")
