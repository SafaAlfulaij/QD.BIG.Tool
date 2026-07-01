"""Port of FileSystem/Package/BigFileUnpack.cs."""

import os

from . import big_file_index, helpers, utils


def do_it(index_file: str, dst_folder: str) -> None:
    _, entries = big_file_index.read_index(index_file)

    for entry in entries:
        if entry.padded_size == 0 and entry.size == 0:
            continue

        if not os.path.isfile(entry.archive_file):
            utils.set_error(f"[ERROR]: Input archive -> {entry.archive_file} <- does not exist")
            return

        file_name = entry.resource_name
        full_path = dst_folder + file_name

        utils.set_info(f"[UNPACKING]: {file_name}")
        utils.create_directory(full_path)

        with open(entry.archive_file, "rb") as archive_stream:
            archive_stream.seek(entry.offset, os.SEEK_SET)

            read_size = entry.padded_size if entry.padded_size > entry.size else entry.size
            buffer = helpers.read_bytes(archive_stream, read_size)

            with open(full_path, "wb") as out_file:
                out_file.write(buffer)
