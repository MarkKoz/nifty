__all__ = ("configure_logging",)

import logging

from rich.console import Console
from rich.highlighter import NullHighlighter
from rich.logging import RichHandler


def configure_logging(level: int = logging.INFO, level_all: int = logging.WARNING) -> None:
    handler = RichHandler(
        rich_tracebacks=False,
        show_path=False,
        markup=True,
        highlighter=NullHighlighter(),
        console=Console(no_color=False, color_system="truecolor"),
    )

    logging.basicConfig(level=level_all, format="%(message)s", datefmt="[%X]", handlers=[handler])

    logging.getLogger("nifty").setLevel(level)
