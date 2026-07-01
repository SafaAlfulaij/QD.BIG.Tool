"""Shared BigFile .idx parsing, used by both the unpacker and the packer."""

import os
from typing import List, Tuple

from . import big_file_debug, big_file_types, helpers
from .big_file_entry import BigFileEntry
from .big_file_header import BigFileHeader

MAGIC = "QUANTICDREAMTABINDEX"
SUB_MAGIC = "ZEP" * 24


def archive_file_path(base_file: str, package_id: int) -> str:
    if package_id == 0:
        return base_file + ".dat"
    return base_file + ".d" + f"{package_id:02d}"


def read_index(index_file: str) -> Tuple[BigFileHeader, List[BigFileEntry]]:
    entries: List[BigFileEntry] = []

    with open(index_file, "rb") as stream:
        header = BigFileHeader()
        header.magic = helpers.read_bytes(stream, 20).decode("ascii")
        header.version = helpers.read_int32(stream, True)
        header.unknown = helpers.read_int32(stream, True)

        if header.version in (13, 17):
            header.sub_magic = helpers.read_bytes(stream, 72).decode("ascii")
        elif header.version == 18:
            header.sub_magic = helpers.read_bytes(stream, 72).decode("ascii")
            stream.seek(1, os.SEEK_CUR)
        else:
            raise Exception("[ERROR]: Invalid version of index file!")

        header.total_files = helpers.read_int32(stream, True)

        if header.magic != MAGIC:
            raise Exception("[ERROR]: Invalid magic of index file!")

        if header.sub_magic != SUB_MAGIC:
            raise Exception("[ERROR]: Invalid sub magic of index file!")

        base_file = os.path.join(os.path.dirname(index_file), os.path.splitext(os.path.basename(index_file))[0])

        for _ in range(header.total_files):
            resource_type_id = helpers.read_int32(stream, True)
            flag = helpers.read_int32(stream, True)
            file_id = helpers.read_int32(stream, True)
            offset = helpers.read_uint32(stream, True)
            size = helpers.read_int32(stream, True)
            padded_size = helpers.read_int32(stream, True)
            package_id = helpers.read_int32(stream, True)

            archive_file = archive_file_path(base_file, package_id)
            resource_type = big_file_types.get_resource_type(resource_type_id)

            if big_file_debug.debug_file_loaded:
                debug_name = big_file_debug.get_debug_resource_name(resource_type_id, file_id, size)
                resource_name = resource_type + os.sep + (debug_name or "")
            else:
                resource_name = resource_type + os.sep + str(file_id)

            entries.append(BigFileEntry(
                resource_type_id=resource_type_id,
                flag=flag,
                file_id=file_id,
                offset=offset,
                size=size,
                padded_size=padded_size,
                package_id=package_id,
                archive_file=archive_file,
                resource_type=resource_type,
                resource_name=resource_name,
            ))

    return header, entries
