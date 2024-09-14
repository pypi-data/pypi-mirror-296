from pathlib import Path
from typing import Optional

from pydantic.v1 import SecretStr
from rich.progress import Progress, SpinnerColumn, TextColumn

from autogen_readme import README_NAME, console

from .chat_models import execute_local_script, openai_chat_model
from .files import locate_py_files, process_py_files, write_file
from .prompts import make_main_readme_prompt


def generate_main_readme_from_openai(
    root: Path,
    openai_api_key: SecretStr,
    temperature: float = 0.0,
    readme_path: Optional[Path] = None,
) -> Path:
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            # Task 1: Locating project files
            locate_files_tasks = progress.add_task(
                description="Analyzing project files...", total=1
            )
            py_files = locate_py_files(root)
            general_content = process_py_files(root, py_files)
            model_prompt = make_main_readme_prompt(general_content)
            progress.advance(locate_files_tasks)

            # Task 2: Generating the README
            generate_readme_task = progress.add_task(
                description="Writing the README...", total=1
            )
            readme_content = openai_chat_model(
                human_prompt=model_prompt,
                openai_api_key=openai_api_key,
                temperature=temperature,
            )
            progress.advance(generate_readme_task)

            # Task 3: Saving the file
            write_file_task = progress.add_task(
                description="Saving to file...", total=1
            )
            if not readme_path:
                readme_path = root / README_NAME
            write_file(content=readme_content, root=root, path=readme_path)
            progress.advance(write_file_task)

        return readme_path

    except Exception as e:
        console.log(f"An error occurred: {e}", style="danger")
        raise


def generate_main_readme_from_local_script(
    root: Path, local_script: Path, readme_path: Optional[Path] = None
) -> Path:
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            # Task 1: Locating project files
            locate_files_tasks = progress.add_task(
                description="Analyzing project files...", total=1
            )
            py_files = locate_py_files(root)
            general_content = process_py_files(root, py_files)
            model_prompt = make_main_readme_prompt(general_content)
            progress.advance(locate_files_tasks)

            # Task 2: Generating the README using the local script
            generate_readme_task = progress.add_task(
                description="Running local script to generate README...", total=1
            )
            readme_content = execute_local_script(
                script_path=local_script,
                prompt=model_prompt,
            )
            progress.advance(generate_readme_task)

            # Task 3: Saving the file
            write_file_task = progress.add_task(
                description="Saving to file...", total=1
            )
            if not readme_path:
                readme_path = root / README_NAME
            write_file(content=readme_content, root=root, path=readme_path)
            progress.advance(write_file_task)

        return readme_path

    except Exception as e:
        console.log(f"An error occurred: {e}", style="danger")
        raise
