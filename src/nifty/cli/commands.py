import logging
import re
from pathlib import Path
from typing import Annotated

import typer

from nifty import nif
from nifty.cli.logger import configure_logging
from nifty.nif.io import read_nif

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
def set_body_parts(
    *,
    file: Annotated[Path, typer.Argument(help="Path to the NIF file.")],
    body_part: Annotated[int, typer.Argument(help="New body part ID.", min=30, max=61)],
    replacing: Annotated[
        int | None,
        typer.Option(
            help="Existing body part ID to replace. Others will be skipped.", min=30, max=61
        ),
    ] = None,
    name: Annotated[
        str | None,
        typer.Option(help="Regular expression pattern to filter geometry by name."),
    ] = None,
    dest: Annotated[
        Path | None,
        typer.Option(
            help="Destination path for the modified NIF file. "
            "Otherwise, overwrite the original file.",
        ),
    ] = None,
    dry_run: Annotated[bool, typer.Option(help="Don't actually modify the NIF file.")] = True,
) -> None:
    """Set the body part of all BSDismemberSkinInstance blocks in a NIF file."""
    log.info("Reading file: %s", file)
    data = read_nif(file)

    name_pattern = re.compile(name.encode("utf8")) if name else None

    if replacing is None:
        nif.body_part.set_body_parts(data, body_part, name_pattern)
    else:
        nif.body_part.replace_body_parts(data, replacing, body_part, name_pattern)

    if not dry_run:
        destination = dest or file
        with destination.open("wb") as stream:
            data.write(stream)

        log.info("Wrote file: %s", destination)


@body_part_app.command(name="list")
def list_body_parts(
    *,
    file: Annotated[Path, typer.Argument(help="Path to the NIF file.")],
    name: Annotated[
        str | None,
        typer.Option(help="Regular expression pattern to filter geometry by name."),
    ] = None,
    error: Annotated[bool, typer.Option(help="Exit with an error if no body parts found.")] = False,
) -> None:
    """List the body part of all partitions in all BSDismemberSkinInstance blocks in a NIF file."""
    log.info("Reading file: %s", file)
    data = read_nif(file)

    name_pattern = re.compile(name.encode("utf8")) if name else None

    found = False
    for geometry_name, partition, body_part in nif.body_part.list_body_parts(data, name_pattern):
        log.info("%s partition %d: %s", geometry_name, partition, body_part)
        found = True

    if not found:
        log.log(logging.ERROR if error else logging.WARNING, "No body parts found")
        if error:
            raise typer.Exit(1)
