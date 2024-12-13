from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "cyan",
        "warning": "yellow",
        "error": "red bold",
        "url": "blue underline",
        "msg": "bold green"
    }
)

console = Console(theme=custom_theme)
