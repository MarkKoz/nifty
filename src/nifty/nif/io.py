__all__ = ("read_nif",)

from pathlib import Path

from pyffi.formats.nif import NifFormat


def read_nif(path: Path) -> NifFormat.Data:
    """Read a NIF file."""
    data = NifFormat.Data()

    with path.open("rb") as f:
        data.read(f)

    return data
