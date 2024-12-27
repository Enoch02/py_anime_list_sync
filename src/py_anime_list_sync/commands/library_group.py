import click

from ..utils.console import console
from ..logic.authentication import get_authenticated_accounts, list_authenticated_accounts
from ..logic.list_management import get_list_for
from ..utils.models import AuthenticatedAccount
from ..utils.mal_models import MALSortOptions, MALStatusFilters
from ..utils.helpers import get_enum_names


@click.group(name="library")
def commands():
    """View and manage anime and manga lists"""
    pass


@commands.command("anime")
@click.argument("account_id", type=int)
@click.option(
    "-o", "--order",
    default=MALSortOptions.title.name,
    type=click.Choice(get_enum_names(MALSortOptions), case_sensitive=False),
    help="Sorts the anime list in the specified method"
)
@click.option(
    "-s", "--status",
    default=MALStatusFilters.all.name,
    type=click.Choice(get_enum_names(MALStatusFilters), case_sensitive=False),
    help="Filters anime list."
)
@click.option("-l", "--limit", type=int, default=100)
def anime_list(account_id: int, order: str, status: str, limit: int):
    """View your anime list"""
    _id = account_id
    selected_account: AuthenticatedAccount | None

    def account_filter(account: AuthenticatedAccount) -> bool:
        return account.id == _id

    with console.status("Loading..", spinner="runner"):
        authenticated_accounts = get_authenticated_accounts()
        selected_account = next(filter(account_filter, authenticated_accounts), None)

    while not selected_account:
        console.print("Invalid account selection", style="warning")
        list_authenticated_accounts()
        _id = click.prompt("Select a valid id", type=int)
        selected_account = next(filter(account_filter, authenticated_accounts), None)
    else:
        console.print(f"Welcome {selected_account.account_name}!")
        with console.status("Getting anime list..", spinner="clock"):
            get_list_for(selected_account, order, status, limit)


@commands.command("manga")
# @click.option()
def manga_list():
    """View your manga list"""
    ...
