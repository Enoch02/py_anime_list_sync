from ..logic.mal_logic import mal_get_anime_list
from ..utils.models import AuthenticatedAccount
from ..utils.console import console
from ..utils.constants import AVAILABLE_TRACKERS


def get_list_for(account: AuthenticatedAccount, order: str):
    """
        Handles getting anime lists from various services.

        Args:
            account (AuthenticatedAccount): an authenticated account

        Returns:

        """
    if account.tracker == AVAILABLE_TRACKERS[0]:
        anime_list = mal_get_anime_list(account)
        console.print(anime_list)

    elif account.tracker == AVAILABLE_TRACKERS[1]:
        console.print("Coming soon!")
