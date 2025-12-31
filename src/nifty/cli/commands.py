import logging
from pathlib import Path
from typing import Annotated

import typer

from nifty.cli.logger import configure_logging

log = logging.getLogger(__name__)

app = typer.Typer(help="Tools to automate NIF file operations.")
body_part_app = typer.Typer(name="body-part", help="Body part tools.")
app.add_typer(body_part_app)


@app.callback()
def callback(
    *,
    debug: Annotated[bool, typer.Option(help="Enable debug logging.")] = False,
    debug_all: Annotated[bool, typer.Option(help="Enable debug logging everywhere.")] = False,
) -> None:
    configure_logging(
        logging.DEBUG if debug else logging.INFO, logging.DEBUG if debug_all else logging.WARNING
    )


@body_part_app.command(name="set")
def set_body_part(
    *,
    file: Annotated[Path, typer.Argument(help="Path to the NIF file.")],
    partition: Annotated[int, typer.Argument(help="New partition.", min=30, max=61)],
    dry_run: Annotated[bool, typer.Option(help="Don't actually modify the NIF file.")] = True,
) -> None:
    """Set the body part of all BSDismemberSkinInstance blocks in a NIF file."""
