from rich.table import Table

from .mal_logic import print_mal_table
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
        # TODO: how do i handle paging?
        anime_list = mal_get_anime_list(account, sort, status, limit)
        anime_list_with_data = mal_get_anime_list_data(account, anime_list, verbose)
        print_mal_table(account.account_name, anime_list_with_data)

    elif account.tracker == AVAILABLE_TRACKERS[1]:
        console.print("Coming soon!")
