"""Port of FileSystem/Package/BigFileUnpack.cs."""

import os

from . import big_file_debug, big_file_types, helpers, utils
from .big_file_entry import BigFileEntry
from .big_file_header import BigFileHeader

_SUB_MAGIC = "ZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEP"


def do_it(index_file: str, dst_folder: str) -> None:
    entry_table = []

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

        if header.magic != "QUANTICDREAMTABINDEX":
            raise Exception("[ERROR]: Invalid magic of index file!")

        if header.sub_magic != _SUB_MAGIC:
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

            if package_id == 0:
                archive_file = base_file + ".dat"
            else:
                archive_file = base_file + ".d" + f"{package_id:02d}"

            resource_type = big_file_types.get_resource_type(resource_type_id)

            if big_file_debug.debug_file_loaded:
                resource_name = resource_type + os.sep + str(
                    big_file_debug.get_debug_resource_name(resource_type_id, file_id, size)
                )
            else:
                resource_name = resource_type + os.sep + str(file_id)

            entry = BigFileEntry(
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
            )

            if entry.padded_size != 0 or entry.size != 0:
                entry_table.append(entry)

    for entry in entry_table:
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
