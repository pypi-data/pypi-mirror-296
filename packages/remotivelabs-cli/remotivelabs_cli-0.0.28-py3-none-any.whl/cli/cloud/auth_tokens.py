import json
import os
import sys
from json.decoder import JSONDecodeError
from pathlib import Path

import typer

from .rest_helper import RestHelper as Rest

app = typer.Typer()

TOKEN_FILE_NAME = str(Path.home()) + "/.config/.remotive/cloud.secret.token"
CONFIG_DIR_NAME = str(Path.home()) + "/.config/.remotive/"


@app.command(name="create", help="Create and download a new personal access token")
def get_personal_access_token(activate: bool = typer.Option(False, help="Activate the token for use after download")) -> None:  # pylint: disable=W0621
    Rest.ensure_auth_token()
    response = Rest.handle_post(url="/api/me/keys", return_response=True)

    if response is None:
        return

    if response.status_code == 200:
        name = response.json()["name"]
        path_to_file = write_personal_token(f"personal-token-{name}.json", response.text)
        print(f"Personal access token written to {path_to_file}")
        if not activate:
            print(f"Use 'remotive cloud auth tokens activate {os.path.basename(path_to_file)}' to use this access token from cli")
        else:
            do_activate(path_to_file)
            print("Token file activated and ready for use")
        print("\033[93m This file contains secrets and must be kept safe")
    else:
        print(f"Got status code: {response.status_code}")
        print(response.text)


@app.command(name="list", help="List personal access tokens")
def list_personal_access_tokens() -> None:
    Rest.ensure_auth_token()
    Rest.handle_get("/api/me/keys")


@app.command(name="revoke")
def revoke(name_or_file: str = typer.Argument(help="Name or file path of the access token to revoke")) -> None:
    """
    Revoke an access token by token name or path to a file containing that token

    Name is found in the json file
    ```
    {
        "expires": "2034-07-31",
        "token": "xxx",
        "created": "2024-07-31T09:18:50.406+02:00",
        "name": "token_name"
    }
    ```
    """
    name = name_or_file
    if "." in name_or_file:
        json_str = read_file(name_or_file)
        try:
            name = json.loads(json_str)["name"]
        except JSONDecodeError:
            sys.stderr.write("Failed to parse json, make sure its a correct access token file\n")
            sys.exit(1)
        except KeyError:
            sys.stderr.write("Json does not contain a name property, make sure its a correct access token file\n")
            sys.exit(1)
    Rest.ensure_auth_token()
    Rest.handle_delete(f"/api/me/keys/{name}")


@app.command()
def describe(file: str = typer.Argument(help="File name")) -> None:
    """
    Show contents of specified access token file
    """
    print(read_file(file))


@app.command()
def activate(file: str = typer.Argument(..., help="File name")) -> None:
    """
    Activate a access token file to be used for authentication.

    --file

    This will be used as the current access token in all subsequent requests. This would
    be the same as login with a browser.
    """
    do_activate(file)


def do_activate(file: str) -> None:
    # Best effort to read file
    if os.path.exists(file):
        token_file = json.loads(read_file_with_path(file))
        write_token(token_file["token"])
    elif os.path.exists(str(Path.home()) + f"/.config/.remotive/{file}"):
        token_file = json.loads(read_file(file))
        write_token(token_file["token"])
    else:
        sys.stderr.write("File could not be found \n")


@app.command(name="list-files")
def list_files() -> None:
    """
    List personal access token files in remotivelabs config directory
    """
    personal_files = filter(lambda f: f.startswith("personal"), os.listdir(CONFIG_DIR_NAME))
    for file in personal_files:
        print(file)


def read_file(file: str) -> str:
    """
    Reads a file using file path or if that does not exist check under ~/.config/.remotive
    """
    path = file
    if not Path(file).exists():
        path = str(Path.home()) + f"/.config/.remotive/{file}"
        if not Path(path).exists():
            sys.stderr.write(f"Failed to find file using {file} or {path}\n")
            sys.exit(1)
    with open(path, "r", encoding="utf8") as f:
        token = f.read()
        f.close()
        return token


def read_file_with_path(file: str) -> str:
    with open(file, "r", encoding="utf8") as f:
        token = f.read()
        f.close()
        return token


def write_token(token: str) -> None:
    with open(TOKEN_FILE_NAME, "w", encoding="utf8") as f:
        f.write(token)
        f.close()


def write_personal_token(file: str, token: str) -> str:
    path = str(Path.home()) + f"/.config/.remotive/{file}"
    with open(path, "w", encoding="utf8") as f:
        f.write(token)
        f.close()
        return path
