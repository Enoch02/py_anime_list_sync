from concurrent.futures import ThreadPoolExecutor
import json
import secrets
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, List
from urllib.parse import urlparse, parse_qs

import requests
from rich.table import Table

from rich.traceback import install
from ..utils.console import console
from ..utils.constants import MAL_CLIENT_ID
from ..utils.mal_helpers import parse_anime_response
from ..utils.mal_models import (
    MALAnimeListResponse,
    MALAnimeData,
    MALNode,
    MALPaging,
    Anime,
)
from ..utils.models import AuthenticatedAccount

# TODO: remove?
# install(show_locals=True)
install()

received_code: str | None = None
server_closed = threading.Event()


# AUTHENTICATION LOGIC
def get_new_code_verifier() -> str:
    token = secrets.token_urlsafe(100)
    return token[:128]


# 2. Print the URL needed to authorize your application.
def print_new_authorization_url(code_challenge: str):
    url = f"https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={MAL_CLIENT_ID}&code_challenge={code_challenge}"
    console.print("Authorise your application by clicking here:")
    console.print(f"{url}\n", style="url")


# 3. Once you've authorized your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorization
#    Code). You need to feed that code to the application.
def generate_new_token(authorization_code: str, code_verifier: str) -> dict:
    url = "https://myanimelist.net/v1/oauth2/token"
    data = {
        "client_id": MAL_CLIENT_ID,
        "code": authorization_code,
        "code_verifier": code_verifier,
        "grant_type": "authorization_code",
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()

    with open("mal_token.json", "w") as file:
        json.dump(token, file, indent=4)

    return token


# 4. Test the API by requesting your profile information
def get_user_info(access_token: str):
    url = "https://api.myanimelist.net/v2/users/@me"
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})

    response.raise_for_status()
    user = response.json()
    response.close()
    return user


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global received_code

        if self.path.startswith("/oauth"):
            query_components = parse_qs(urlparse(self.path).query)

            if "code" in query_components:
                received_code = query_components["code"][0]

                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(
                    b"Authorization successful! You can close this window."
                )

                # Signal that we received the code
                server_closed.set()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No authorization code found")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args) -> None:
        # silence built-in logging
        pass


def start_oauth_server():
    server = HTTPServer(("localhost", 8080), OAuthHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server


# FIXME: can't ctrl+c to stop server after it starts
# TODO: more secure method of storing access token
def add_mal_account():
    """
    Starts the process of authenticating a new MAL account and saving
    its access token locally on the device for future queries
    """
    code_verifier = code_challenge = get_new_code_verifier()
    print_new_authorization_url(code_challenge)

    # Start the server to listen for the callback
    server = start_oauth_server()

    server_closed.wait()
    server.shutdown()
    server.server_close()

    if received_code:
        token = generate_new_token(received_code, code_verifier)
        get_user_info(token["access_token"])
        return True
    else:
        return False


# LIST MANAGEMENT LOGIC
def mal_get_anime_list(
    account: AuthenticatedAccount, sort: str, status: str, limit=100
) -> Optional[MALAnimeListResponse]:
    """
    Fetch anime data from MyAnimeList API.

    Args:
        account (AuthenticatedAccount): an authenticated account
        limit (int): Maximum number of results to return (default: 100)
        sort: sorting option
        status: status filter

    Returns:
        dict: JSON response from the API if successful
        None: If the request fails
    """

    url = "https://api.myanimelist.net/v2/users/@me/animelist"
    headers = {"Authorization": f"Bearer {account.token}"}
    params = {"status": status, "sort": sort, "limit": limit}

    if status == "all":
        params["status"] = ""

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_json = response.json()
        parsed_response = MALAnimeListResponse(
            data=[
                MALAnimeData(
                    node=MALNode(id=item["node"]["id"], title=item["node"]["title"])
                )
                for item in response_json["data"]
            ],
            paging=MALPaging(next=response_json["paging"].get("next")),
        )

        return parsed_response

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return None


def fetch_anime_data(anime_data, account, verbose):
    url = f"https://api.myanimelist.net/v2/anime/{anime_data.node.id}"
    params = {
        "fields": "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,mean,rank,popularity,num_list_users,num_scoring_users,nsfw,created_at,updated_at,media_type,status,genres,my_list_status,num_episodes,start_season,broadcast,source,average_episode_duration,rating,pictures,background,related_anime,related_manga,recommendations,studios,statistics"
    }
    headers = {"Authorization": f"Bearer {account.token}"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        if response.status_code == 200:
            if verbose:
                console.print(f"Loading data for {anime_data.node.title}", style="info")
            return parse_anime_response(response.json())
    except requests.exceptions.RequestException:
        return None


def mal_get_anime_list_data(
    account: AuthenticatedAccount, parsed_list: MALAnimeListResponse, verbose: bool
) -> Optional[List[Anime]]:
    """
    Gather Anime data from the Anime List Nodes using thread pool

    Args:
        account: Authenticated account
        parsed_list: Parsed anime list response
        verbose: Enable verbose output

    Returns:
        Optional[List[Anime]]: list of Anime instances containing parsed data or None
    """
    max_workers = min(32, len(parsed_list.data))  # Cap at 32 threads
    anime_list_with_data = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(fetch_anime_data, anime_data, account, verbose)
            for anime_data in parsed_list.data
        ]

        for future in futures:
            result = future.result()
            if result is not None:
                anime_list_with_data.append(result)

    return anime_list_with_data if anime_list_with_data else None


# TODO
def print_mal_table(acc_name: str, anime_list: List[Anime]):
    """ """
    table = Table(title=f"{acc_name}'s Anime List")

    table.add_column("ID", justify="right")
    table.add_column("Title")
    table.add_column("Episodes", justify="right")
    table.add_column("Episodes Watched", justify="right")
    table.add_column("Status")

    for anime in anime_list:
        table.add_row(
            str(anime.id),
            anime.title,
            str(anime.num_episodes),
            str(anime.my_list_status.num_episodes_watched),
            anime.my_list_status.status,
        )

    console.print(table)
