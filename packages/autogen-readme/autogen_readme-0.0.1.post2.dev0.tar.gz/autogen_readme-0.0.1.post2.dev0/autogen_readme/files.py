import shutil
import tempfile
from pathlib import Path
from typing import List

from autogen_readme import console


def locate_py_files(root: Path) -> List[Path]:
    return [
        path
        for path in root.rglob("*.py")
        if not any(part.startswith(".") for part in path.parts)
    ]


def process_py_files(root: Path, py_files: List[Path]) -> str:
    files_content = []

    for py_file in py_files:
        try:
            with py_file.open("r", encoding="utf-8") as file:
                content = file.read()
                files_content.append(
                    f"```{Path(file.name).relative_to(root)}\n{content}\n```\n"
                )
        except UnicodeDecodeError:
            console.log(f"Error when decoding the file: {file.name}", style="danger")
            raise
        except FileNotFoundError:
            console.log(f"File {py_file} not found.", style="danger")
            raise
        except PermissionError:
            console.log(f"Permission denied to access file {py_file}.", style="danger")
            raise
    return "".join(files_content)


def write_file(content: str, root: Path, path: Path) -> None:
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=root, encoding="utf-8"
    ) as temp_file:
        temp_file.write(content)
        temp_path = Path(temp_file.name)

    shutil.move(str(temp_path), str(path))
