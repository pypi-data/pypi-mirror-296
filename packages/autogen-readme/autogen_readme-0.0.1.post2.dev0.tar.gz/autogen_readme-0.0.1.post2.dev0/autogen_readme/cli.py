import getpass
import os
from pathlib import Path
from typing import Optional

import typer
from pydantic.v1 import SecretStr
from typing_extensions import Annotated

from autogen_readme import README_NAME, console

from .generator import (
    generate_main_readme_from_local_script,
    generate_main_readme_from_openai,
)

# from rich.progress import Progress, SpinnerColumn, TextColumn

app = typer.Typer()


@app.command()
def generate_from_openai(
    directory: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    readme_path: Optional[Path] = typer.Option(
        None, "--output-path", "-o", exists=False
    ),
    temperature: float = typer.Option(
        0.0,
        "--temperature",
        "-t",
        min=0.0,
        max=1.0,
        help="The temperature of the OpenAI model, between 0 and 1. The higher the more creative. Default to 0.",
    ),
    use_env_api_key: Optional[bool] = typer.Option(
        False,
        "--use-env-api-key",
        "-e",
        help="Use the local OPENAI_API_KEY environment variable.",
    ),
):
    root = Path(directory).resolve()

    openai_api_key: Optional[SecretStr] = None
    if use_env_api_key:
        if not os.getenv("OPENAI_API_KEY"):
            console.log(
                "OPENAI_API_KEY not found in the environment. Either restart and provide it or enter your OpenAI API key.",
                style="warning",
            )
        else:
            openai_api_key = SecretStr(str(os.getenv("OPENAI_API_KEY")))
    if not openai_api_key:
        openai_api_key = SecretStr(getpass.getpass("Enter your OpenAI API Key: "))

    readme_path = generate_main_readme_from_openai(
        root=root,
        openai_api_key=openai_api_key,
        temperature=temperature,
        readme_path=readme_path,
    )
    console.log(f"{README_NAME} generated at {readme_path}", style="success")


@app.command()
def generate_from_local_script(
    directory: Annotated[Path, typer.Argument(exists=True, file_okay=False)],
    local_script: Annotated[Path, typer.Argument(exists=True, dir_okay=False)],
    readme_path: Optional[Path] = typer.Option(
        None, "--output-path", "-o", exists=False
    ),
) -> None:
    root = Path(directory).resolve()

    readme_path = generate_main_readme_from_local_script(
        root=root, local_script=local_script, readme_path=readme_path
    )
    console.log(f"{README_NAME} generated at {readme_path}", style="success")
