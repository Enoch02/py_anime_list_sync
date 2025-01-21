import click

from ..utils.console import console
from ..logic.authentication import (
    get_authenticated_accounts,
    list_authenticated_accounts,
)
from ..logic.list_management import get_list_for
from ..utils.models import AuthenticatedAccount
from ..utils.mal_models import MALSortOptions, MALStatusFilters
from ..utils.helpers import get_enum_names


@click.group(name="library")
def commands():
    """View and manage anime and manga lists"""
    pass


@commands.command("anime")
@click.argument("account_id", type=int, required=False)
@click.option(
    "-o",
    "--order",
    default=MALSortOptions.title.value,
    type=click.Choice(get_enum_names(MALSortOptions), case_sensitive=False),
    help="Sorts the anime list in the specified method",
)
@click.option(
    "-s",
    "--status",
    default=MALStatusFilters.all.value,
    type=click.Choice(get_enum_names(MALStatusFilters), case_sensitive=False),
    help="Filters anime list.",
)
@click.option("-l", "--limit", type=int, default=100)
@click.option("--verbose/--no-verbose", default=False)
def anime_list(account_id: int, order: str, status: str, limit: int, verbose: bool):
    """View your anime list"""
    _id = account_id
    selected_account: AuthenticatedAccount | None

    if not account_id:
        list_authenticated_accounts()
        _id = click.prompt("Select an account id", type=int)

    def account_filter(account: AuthenticatedAccount) -> bool:
        return account.id == _id

    with console.status("Loading..", spinner="runner"):
        authenticated_accounts = get_authenticated_accounts()
        if authenticated_accounts is None:
            console.print("No authenticated account could be loaded", style="error")
            return
        selected_account = next(filter(account_filter, authenticated_accounts), None)

    while not selected_account:
        console.print("Invalid account selection", style="warning")
        list_authenticated_accounts()
        _id = click.prompt("Select a valid id", type=int)
        selected_account = next(filter(account_filter, authenticated_accounts), None)
    else:
        console.print(f"Welcome {selected_account.account_name}!")
        get_list_for(selected_account, order, status, limit, verbose)


@commands.command("manga")
# @click.option()
def manga_list():
    """View your manga list"""
    ...
