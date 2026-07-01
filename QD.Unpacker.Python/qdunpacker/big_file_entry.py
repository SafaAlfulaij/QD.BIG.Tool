"""Port of FileSystem/Package/BigFileEntry.cs."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BigFileEntry:
    resource_type_id: int = 0
    flag: int = 0  # 1 (???)
    file_id: int = 0
    offset: int = 0
    size: int = 0
    padded_size: int = 0  # ???
    package_id: int = 0
    archive_file: Optional[str] = None
    resource_type: Optional[str] = None
    resource_name: Optional[str] = None  # Only if debug file are present


@dataclass
class BigFileDebugEntryV13:
    resource_type_id: int = 0
    flag: int = 0  # 1 (???)
    file_id: int = 0
    resource_name_length: int = 0
    offset: int = 0
    size: int = 0
    padded_size: int = 0
    unknown1: int = 0  # (???)
    unknown2: int = 0  # (???)
    unknown3: int = 0  # (???)
    archive_file: Optional[str] = None
    resource_type: Optional[str] = None
    resource_name: Optional[str] = None


@dataclass
class BigFileDebugEntryV17:
    resource_type_id: int = 0
    flag: int = 0  # 1 (???)
    file_id: int = 0
    unknown1: int = 0
    unknown2: int = 0  # Hash ???
    resource_name_length: int = 0
    offset: int = 0
    size: int = 0
    padded_size: int = 0
    unknown3: int = 0
    unknown4: int = 0
    unknown5: int = 0
    archive_file: Optional[str] = None
    resource_type: Optional[str] = None
    resource_name: Optional[str] = None
