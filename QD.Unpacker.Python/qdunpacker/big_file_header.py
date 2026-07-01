"""Port of FileSystem/Package/BigFileHeader.cs."""

from dataclasses import dataclass


@dataclass
class BigFileHeader:
    magic: str = ""  # QUANTICDREAMTABINDEX
    version: int = 0  # 13 - Heavy Rain, 17 - BEYOND Two Souls, 18 - Detroit: Become Human
    unknown: int = 0  # 13 = 65535, 17 = 0, 18 = 11548767
    sub_magic: str = ""  # ZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEPZEP
    total_files: int = 0


@dataclass
class BigFileDebugHeader:
    magic: str = ""  # QUANTICDREAMTABINDEX
    version: int = 0  # 13 - Heavy Rain, 17 - BEYOND Two Souls
    total_files: int = 0
