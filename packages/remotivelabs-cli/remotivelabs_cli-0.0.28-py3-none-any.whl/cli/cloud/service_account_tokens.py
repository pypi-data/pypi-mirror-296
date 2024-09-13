import json
import os
from pathlib import Path

import typer

from .rest_helper import RestHelper as Rest

app = typer.Typer()

CONFIG_DIR_NAME = str(Path.home()) + "/.config/.remotive/"
TOKEN_FILE_NAME = str(Path.home()) + "/.config/.remotive/cloud.secret.token2"


@app.command(name="create", help="Create new access token")
def create(
    expire_in_days: int = typer.Option(default=365, help="Number of this token is valid"),
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    response = Rest.handle_post(
        url=f"/api/project/{project}/admin/accounts/{service_account}/keys",
        return_response=True,
        body=json.dumps({"daysUntilExpiry": expire_in_days}),
    )

    if response is None:
        return

    if response.status_code == 200:
        name = response.json()["name"]
        write_token(f"service-account-{service_account}-{name}-token.json", response.text)
    else:
        print(f"Got status code: {response.status_code}")
        print(response.text)


@app.command(name="list", help="List service-account access tokens")
def list_keys(
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_get(f"/api/project/{project}/admin/accounts/{service_account}/keys")


@app.command(name="list-files")
def list_files() -> None:
    """
    List personal access token files in remotivelabs config directory
    """
    personal_files = filter(lambda f: f.startswith("service-account"), os.listdir(CONFIG_DIR_NAME))
    for file in personal_files:
        print(file)


@app.command(name="revoke", help="Revoke service account access token")
def revoke(
    name: str = typer.Argument(..., help="Access token name"),
    service_account: str = typer.Option(..., help="Service account name"),
    project: str = typer.Option(..., help="Project ID", envvar="REMOTIVE_CLOUD_PROJECT"),
) -> None:
    Rest.handle_delete(f"/api/project/{project}/admin/accounts/{service_account}/keys/{name}")


def write_token(file: str, token: str) -> None:
    path = str(Path.home()) + f"/.config/.remotive/{file}"
    with open(path, "w", encoding="utf8") as f:
        f.write(token)
        print(f"Secret token written to {path}")
