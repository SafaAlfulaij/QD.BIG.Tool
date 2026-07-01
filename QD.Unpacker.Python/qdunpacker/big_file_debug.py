"""Port of FileSystem/Package/BigFileDebug.cs."""

from typing import Dict, Optional

from . import big_file_types, helpers
from .big_file_entry import BigFileDebugEntryV13, BigFileDebugEntryV17
from .big_file_header import BigFileDebugHeader

debug_file_loaded = False
_debug_table: Dict[str, str] = {}


def load(debug_file: str) -> None:
    global debug_file_loaded

    with open(debug_file, "rb") as stream:
        header = BigFileDebugHeader()
        header.magic = helpers.read_bytes(stream, 20).decode("ascii")
        header.version = helpers.read_int32(stream, True)
        header.total_files = helpers.read_int32(stream, True)

        if header.magic != "QUANTICDREAMTABINDEX":
            raise Exception("[ERROR]: Invalid magic of debug file!")

        if header.version != 13 and header.version != 17:
            raise Exception("[ERROR]: Invalid version of debug file!")

        if header.version == 17:
            header.total_files = helpers.read_int32(stream, True)

        _debug_table.clear()
        for _ in range(header.total_files):
            if header.version == 13:
                _load_v13_entry(stream)
            elif header.version == 17:
                _load_v17_entry(stream)

    debug_file_loaded = True


def _load_v13_entry(stream) -> None:
    resource_type_id = helpers.read_int32(stream, True)
    flag = helpers.read_int32(stream, True)
    file_id = helpers.read_int32(stream, True)
    resource_name_length = helpers.read_int32(stream, True)
    resource_name = helpers.read_bytes(stream, resource_name_length).decode("ascii")
    offset = helpers.read_uint32(stream, True)
    size = helpers.read_int32(stream, True)
    padded_size = helpers.read_int32(stream, True)
    unknown1 = helpers.read_int32(stream, True)
    unknown2 = helpers.read_int32(stream, True)
    unknown3 = helpers.read_int32(stream, True)

    resource_type = big_file_types.get_resource_type(resource_type_id)

    entry = BigFileDebugEntryV13(
        resource_type_id=resource_type_id,
        flag=flag,
        file_id=file_id,
        resource_name_length=resource_name_length,
        offset=offset,
        size=size,
        padded_size=padded_size,
        unknown1=unknown1,
        unknown2=unknown2,
        unknown3=unknown3,
        resource_type=resource_type,
        resource_name=resource_name,
    )

    unique_id = f"{entry.resource_type_id}_{entry.file_id}_{entry.size}"

    if entry.padded_size != 0 or entry.size != 0:
        _debug_table[unique_id] = entry.resource_name


def _load_v17_entry(stream) -> None:
    resource_type_id = helpers.read_int32(stream, True)
    flag = helpers.read_int32(stream, True)
    file_id = helpers.read_int32(stream, True)
    unknown1 = helpers.read_int32(stream, True)
    unknown2 = helpers.read_uint32(stream, True)
    resource_name_length = helpers.read_int32(stream, True)
    resource_name = helpers.read_bytes(stream, resource_name_length).decode("ascii")
    offset = helpers.read_uint32(stream, True)
    size = helpers.read_int32(stream, True)
    padded_size = helpers.read_int32(stream, True)
    unknown3 = helpers.read_int32(stream, True)
    unknown4 = helpers.read_int32(stream, True)
    unknown5 = helpers.read_int32(stream, True)

    resource_type = big_file_types.get_resource_type(resource_type_id)

    entry = BigFileDebugEntryV17(
        resource_type_id=resource_type_id,
        flag=flag,
        file_id=file_id,
        unknown1=unknown1,
        unknown2=unknown2,
        resource_name_length=resource_name_length,
        offset=offset,
        size=size,
        padded_size=padded_size,
        unknown3=unknown3,
        unknown4=unknown4,
        unknown5=unknown5,
        resource_type=resource_type,
        resource_name=resource_name,
    )

    unique_id = f"{entry.resource_type_id}_{entry.file_id}_{entry.size}"

    if entry.padded_size != 0 or entry.size != 0:
        _debug_table[unique_id] = entry.resource_name


def get_debug_resource_name(resource_type_id: int, file_id: int, size: int) -> Optional[str]:
    unique_id = f"{resource_type_id}_{file_id}_{size}"
    return _debug_table.get(unique_id)
