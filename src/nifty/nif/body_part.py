__all__ = (
    "filter_skin_instances",
    "list_body_parts",
    "list_skin_instances",
    "replace_body_parts",
    "set_body_parts",
)

import logging
import re
from collections.abc import Iterator

from pyffi.formats.nif import NifFormat

log = logging.getLogger(__name__)


def list_skin_instances(
    data: NifFormat.Data,
) -> Iterator[tuple[NifFormat.NiGeometry, NifFormat.BSDismemberSkinInstance]]:
    for parent in data.get_global_iterator():
        if isinstance(parent, NifFormat.NiGeometry):
            if isinstance(parent.skin_instance, NifFormat.BSDismemberSkinInstance):
                yield parent, parent.skin_instance


def filter_skin_instances(
    data: NifFormat.Data, name_pattern: re.Pattern[bytes] | None = None
) -> Iterator[tuple[NifFormat.NiGeometry, NifFormat.BSDismemberSkinInstance]]:
    for parent, skin_instance in list_skin_instances(data):
        if not name_pattern or name_pattern.search(parent.name):
            yield parent, skin_instance


def list_body_parts(
    data: NifFormat.Data, name_pattern: re.Pattern[bytes] | None = None
) -> Iterator[tuple[bytes, int, int]]:
    for parent, skin_instance in filter_skin_instances(data):
        for i, partition in enumerate(skin_instance.partitions, 1):
            yield parent.name, i, partition.body_part


def set_body_parts(
    data: NifFormat.Data, body_part: int, name_pattern: re.Pattern[bytes] | None = None
) -> None:
    for parent, skin_instance in filter_skin_instances(data, name_pattern):
        for i, partition in enumerate(skin_instance.partitions, 1):
            old_body_part = partition.body_part
            partition.body_part = body_part

            log.info(
                "Set %r partition %d body part: %s -> %s",
                parent.name,
                i,
                old_body_part,
                body_part,
            )


def replace_body_parts(
    data: NifFormat.Data,
    old_body_part: int,
    new_body_part: int,
    name_pattern: re.Pattern[bytes] | None = None,
) -> None:
    for parent, skin_instance in filter_skin_instances(data, name_pattern):
        for i, partition in enumerate(skin_instance.partitions, 1):
            if partition.body_part == old_body_part:
                partition.body_part = new_body_part

                log.info(
                    "Set %r partition %d body part: %s -> %s",
                    parent.name,
                    i,
                    old_body_part,
                    new_body_part,
                )
