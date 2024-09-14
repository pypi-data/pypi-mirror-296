from rich.console import Console
from rich.theme import Theme

# Version
__version__ = "0.0.1.post2.dev0"

# Logging
custom_theme = Theme(
    {
        "success": "bold green",
        "info": "bold cyan",
        "warning": "bold magenta",
        "danger": "bold red",
    }
)
console = Console(theme=custom_theme)

# Variables
README_NAME: str = "README.md"
