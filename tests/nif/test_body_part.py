import importlib.resources
import re
from collections.abc import Iterator

import pytest
from pyffi.formats.nif import NifFormat

import tests.resources
from nifty.nif import body_part
from nifty.nif.io import read_nif


@pytest.fixture
def nif_file() -> Iterator[NifFormat.Data]:
    with importlib.resources.path(tests.resources, "cuirass_1.nif") as path:
        yield read_nif(path)


def get_body_parts(geometry: NifFormat.NiGeometry) -> list[int]:
    if not geometry.skin_instance:
        raise ValueError("Geometry does not have a skin instance")

    if not isinstance(geometry.skin_instance, NifFormat.BSDismemberSkinInstance):
        raise TypeError(
            f"Skin instance is {type(geometry.skin_instance.__name__)} "
            f"but expected {type(NifFormat.BSDismemberSkinInstance).__name__}"
        )

    return [p.body_part for p in geometry.skin_instance.partitions]


def test_set_body_parts(nif_file: NifFormat.Data):
    body_part.set_body_parts(nif_file, 50)

    root = nif_file.roots[0]
    assert get_body_parts(root.children[0]) == [50, 50]
    assert get_body_parts(root.children[1]) == [50]
    assert get_body_parts(root.children[2]) == [50, 50, 50]
    assert get_body_parts(root.children[3]) == [50]
    assert get_body_parts(root.children[4]) == [50, 50]
    assert get_body_parts(root.children[5]) == [50, 50, 50]
    assert get_body_parts(root.children[6]) == [50, 50, 50, 50]


def test_set_body_parts_with_filter(nif_file: NifFormat.Data):
    body_part.set_body_parts(nif_file, 50, re.compile(b"Armor"))

    root = nif_file.roots[0]
    assert get_body_parts(root.children[0]) == [50, 50]
    assert get_body_parts(root.children[1]) == [32]
    assert get_body_parts(root.children[2]) == [38, 32, 32]
    assert get_body_parts(root.children[3]) == [32]
    assert get_body_parts(root.children[4]) == [38, 32]
    assert get_body_parts(root.children[5]) == [50, 50, 50]
    assert get_body_parts(root.children[6]) == [34, 32, 38, 32]


def test_replace_body_parts_with_filter(nif_file: NifFormat.Data):
    body_part.replace_body_parts(nif_file, 38, 44, re.compile(b"Cuirass"))

    root = nif_file.roots[0]
    assert get_body_parts(root.children[0]) == [32, 32]
    assert get_body_parts(root.children[1]) == [32]
    assert get_body_parts(root.children[2]) == [38, 32, 32]
    assert get_body_parts(root.children[3]) == [32]
    assert get_body_parts(root.children[4]) == [44, 32]
    assert get_body_parts(root.children[5]) == [32, 32, 32]
    assert get_body_parts(root.children[6]) == [34, 32, 38, 32]


def test_set_body_parts_no_partitions():
    with importlib.resources.path(tests.resources, "ring.nif") as path:
        body_part.set_body_parts(read_nif(path), 50)
