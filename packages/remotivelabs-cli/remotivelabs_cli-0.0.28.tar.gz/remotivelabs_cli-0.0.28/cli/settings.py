import os
import sys
from pathlib import Path

from rich.console import Console

err_console = Console(stderr=True)

CONFIG_DIR_NAME = str(Path.home()) + "/.config/.remotive/"
TOKEN_FILE_NAME = str(Path.home()) + "/.config/.remotive/cloud.secret.token"


def read_token() -> str:
    if not os.path.exists(TOKEN_FILE_NAME):
        err_console.print(":boom: [bold red]Access failed[/bold red] - No access token found")
        err_console.print("Login with [italic]remotive cloud auth login[/italic]")
        err_console.print(
            "If you have downloaded a personal access token, you can activate "
            "it with [italic]remotive cloud auth tokens activate [FILE_NAME][/italic]"
        )
        sys.exit(1)

    with open(TOKEN_FILE_NAME, "r", encoding="utf-8") as f:
        token = f.read()
        return token
