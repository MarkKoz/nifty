import io
from collections.abc import Generator
from typing import Any

from pyffi.object_models.xml import FileFormat
from pyffi.utils.graph import EdgeFilter

class NifFormat(FileFormat):
    class Data(FileFormat.Data):
        roots: list[Any]

        def read(self, stream: io.BufferedIOBase) -> None: ...
        def write(self, stream: io.BufferedIOBase) -> None: ...
        def get_global_iterator(self, edge_filter: EdgeFilter = ...) -> Generator[Any, Any]: ...

    class NiGeometry:
        name: bytes
        skin_instance: NifFormat.BSDismemberSkinInstance | None

    class BSDismemberSkinInstance:
        partitions: list[NifFormat.BodyPartList]

    class BodyPartList:
        body_part: int
