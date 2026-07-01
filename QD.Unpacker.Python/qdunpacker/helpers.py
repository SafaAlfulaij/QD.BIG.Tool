"""Binary stream/byte-array reading helpers (port of FileSystem/Other/Helpers.cs)."""

import struct
from typing import BinaryIO, List, Optional


def read_bytes(stream: BinaryIO, count: Optional[int] = None) -> bytes:
    if count is None:
        return stream.read()

    result = bytearray()
    while len(result) < count:
        chunk = stream.read(count - len(result))
        if not chunk:
            raise IOError("Unexpected end of stream")
        result.extend(chunk)
    return bytes(result)


def read_int16(stream: BinaryIO, big_endian: bool = False) -> int:
    return struct.unpack(">h" if big_endian else "<h", read_bytes(stream, 2))[0]


def read_int32(stream: BinaryIO, big_endian: bool = False) -> int:
    return struct.unpack(">i" if big_endian else "<i", read_bytes(stream, 4))[0]


def read_int64(stream: BinaryIO, big_endian: bool = False) -> int:
    return struct.unpack(">q" if big_endian else "<q", read_bytes(stream, 8))[0]


def read_uint16(stream: BinaryIO, big_endian: bool = False) -> int:
    return struct.unpack(">H" if big_endian else "<H", read_bytes(stream, 2))[0]


def read_uint32(stream: BinaryIO, big_endian: bool = False) -> int:
    return struct.unpack(">I" if big_endian else "<I", read_bytes(stream, 4))[0]


def read_uint64(stream: BinaryIO, big_endian: bool = False) -> int:
    return struct.unpack(">Q" if big_endian else "<Q", read_bytes(stream, 8))[0]


def read_single(stream: BinaryIO, big_endian: bool = False) -> float:
    return struct.unpack(">f" if big_endian else "<f", read_bytes(stream, 4))[0]


def read_string_unicode_length(stream: BinaryIO, length: int) -> str:
    return read_bytes(stream, length * 2).decode("utf-16")


def read_string_length(stream: BinaryIO) -> str:
    length = read_int32(stream)
    return read_bytes(stream, length).decode("ascii")


def read_string(stream: BinaryIO, length: Optional[int] = None, encoding: str = "ascii", trim: bool = True) -> str:
    if length is not None:
        result = read_bytes(stream, length).decode(encoding)
        return result.strip() if trim else result

    data = bytearray()
    while True:
        byte = stream.read(1)
        if not byte:
            raise IOError("Unexpected end of stream")
        value = byte[0]
        if value == 0:
            break
        data.append(value)

    result = data.decode(encoding)
    return result.strip() if trim else result


def read_string_by_offset(stream: BinaryIO, offset: int, encoding: str = "ascii", trim: bool = True) -> str:
    stream.seek(offset)
    return read_string(stream, encoding=encoding, trim=trim)


def read_string_list(stream: BinaryIO, encoding: str = "ascii", trim: bool = True) -> List[str]:
    stream.seek(0, 2)
    length = stream.tell()

    stream.seek(0)
    result = []
    while stream.tell() < length:
        result.append(read_string(stream, encoding=encoding, trim=trim))
    return result


def copy_to(source: BinaryIO, target: BinaryIO) -> None:
    buffer_size = 32768
    while True:
        chunk = source.read(buffer_size)
        if not chunk:
            break
        target.write(chunk)


# --- byte-array based helpers (port of ByteArrayExtensions) ---

def bytes_read_bytes(data: bytes, count: int, start_index: int = 0) -> bytes:
    return data[start_index:start_index + count]


def bytes_read_int16(data: bytes, start_index: int = 0) -> int:
    return struct.unpack_from("<h", data, start_index)[0]


def bytes_read_int32(data: bytes, start_index: int = 0) -> int:
    return struct.unpack_from("<i", data, start_index)[0]


def bytes_read_uint16(data: bytes, start_index: int = 0) -> int:
    return struct.unpack_from("<H", data, start_index)[0]


def bytes_read_uint32(data: bytes, start_index: int = 0) -> int:
    return struct.unpack_from("<I", data, start_index)[0]


def bytes_read_uint64(data: bytes, start_index: int = 0) -> int:
    return struct.unpack_from("<Q", data, start_index)[0]


def bytes_read_single(data: bytes, start_index: int = 0) -> float:
    return struct.unpack_from("<f", data, start_index)[0]


def bytes_read_single_be(data: bytes, start_index: int = 0) -> float:
    return struct.unpack_from(">f", data, start_index)[0]


def _read_string_internal(data: bytes, start_index: int, encoding: str, trim: bool):
    i = start_index
    while i < len(data) and data[i] != 0:
        i += 1

    result = data[start_index:i].decode(encoding)
    next_index = i + 1
    return (result.strip() if trim else result), next_index


def bytes_read_string(data: bytes, start_index: int = 0, encoding: str = "ascii", trim: bool = True) -> str:
    result, _ = _read_string_internal(data, start_index, encoding, trim)
    return result


def bytes_read_string_list(data: bytes, start_index: int = 0, encoding: str = "ascii", trim: bool = True) -> List[str]:
    result = []
    while start_index < len(data):
        value, start_index = _read_string_internal(data, start_index, encoding, trim)
        result.append(value)
    return result


def is_text(data: bytes) -> bool:
    for b in data:
        c = chr(b)
        if b != 0 and not (c.isalnum() or c.isspace() or _is_punctuation(c) or _is_separator(c)):
            return False
    return True


def _is_punctuation(c: str) -> bool:
    import unicodedata
    return unicodedata.category(c).startswith("P")


def _is_separator(c: str) -> bool:
    import unicodedata
    return unicodedata.category(c).startswith("Z")
