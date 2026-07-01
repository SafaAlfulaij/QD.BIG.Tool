"""Repack extracted (and optionally modified) resource files back into a
BigFile .idx/.dat set.

The original .idx is used as a template for entry order and metadata
(resource type, file id, flag, package id). For each entry this looks for
a matching file under `m_SrcFolder` (same relative path that `BigFileUnpack`
produces); if found, its current bytes replace the entry's content. If a
file was not extracted/modified, its original bytes are copied over from the
source archive next to `m_IndexFile` instead, so a full unpack is not
required before repacking.

Archives are rebuilt from scratch, so `dwOffset` is always recalculated. The
real padding scheme behind `dwPaddedSize` is unknown (see BigFileEntry.cs),
so this simply sets it equal to `dwSize` for every entry.
"""

import os
from typing import BinaryIO, Dict

from . import big_file_index, helpers, utils
from .big_file_entry import BigFileEntry
from .big_file_header import BigFileHeader


def do_it(index_file: str, src_folder: str, dst_folder: str) -> None:
    header, entries = big_file_index.read_index(index_file)

    os.makedirs(dst_folder, exist_ok=True)
    base_file = os.path.join(dst_folder, os.path.splitext(os.path.basename(index_file))[0])

    archive_streams: Dict[int, BinaryIO] = {}
    try:
        for entry in entries:
            if entry.padded_size == 0 and entry.size == 0:
                continue

            data = _read_entry_data(entry, src_folder)

            stream = archive_streams.get(entry.package_id)
            if stream is None:
                stream = open(big_file_index.archive_file_path(base_file, entry.package_id), "wb")
                archive_streams[entry.package_id] = stream

            utils.set_info(f"[PACKING]: {entry.resource_name}")

            entry.offset = stream.tell()
            entry.size = len(data)
            entry.padded_size = len(data)
            stream.write(data)
    finally:
        for stream in archive_streams.values():
            stream.close()

    _write_index(header, entries, base_file + ".idx")


def _read_entry_data(entry: BigFileEntry, src_folder: str) -> bytes:
    resource_path = os.path.join(src_folder, entry.resource_name)
    if os.path.isfile(resource_path):
        with open(resource_path, "rb") as stream:
            return stream.read()

    if not os.path.isfile(entry.archive_file):
        raise Exception(
            f"[ERROR]: Resource -> {resource_path} <- not found and original archive "
            f"-> {entry.archive_file} <- does not exist"
        )

    with open(entry.archive_file, "rb") as stream:
        stream.seek(entry.offset, os.SEEK_SET)
        return helpers.read_bytes(stream, entry.size)


def _write_index(header: BigFileHeader, entries, output_index_file: str) -> None:
    with open(output_index_file, "wb") as stream:
        stream.write(big_file_index.MAGIC.encode("ascii"))
        helpers.write_int32(stream, header.version, True)
        helpers.write_int32(stream, header.unknown, True)
        stream.write(big_file_index.SUB_MAGIC.encode("ascii"))

        if header.version == 18:
            stream.write(b"\x00")

        helpers.write_int32(stream, len(entries), True)

        for entry in entries:
            helpers.write_int32(stream, entry.resource_type_id, True)
            helpers.write_int32(stream, entry.flag, True)
            helpers.write_int32(stream, entry.file_id, True)
            helpers.write_uint32(stream, entry.offset, True)
            helpers.write_int32(stream, entry.size, True)
            helpers.write_int32(stream, entry.padded_size, True)
            helpers.write_int32(stream, entry.package_id, True)
