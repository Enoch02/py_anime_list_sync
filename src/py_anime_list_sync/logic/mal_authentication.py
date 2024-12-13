import json
import secrets
import signal

import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import requests

from ..utils.console import console
from ..utils.constants import MAL_CLIENT_ID

received_code = None
server_closed = threading.Event()


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

        if self.path.startswith('/oauth'):
            query_components = parse_qs(urlparse(self.path).query)

            if 'code' in query_components:
                received_code = query_components['code'][0]

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Authorization successful! You can close this window.')

                # Signal that we received the code
                server_closed.set()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'No authorization code found')
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format: str, *args) -> None:
        # silence built-in logging
        pass


def start_oauth_server():
    server = HTTPServer(('localhost', 80), OAuthHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server


# FIXME: can't ctrl+c to stop server after it starts
def add_mal_account():
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


if __name__ == "__main__":
    add_mal_account()
