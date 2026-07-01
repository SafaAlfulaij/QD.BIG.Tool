"""General utilities (port of FileSystem/Other/Utils.cs)."""

import os
import sys

__version__ = "0.0.1"

_COLOR_WHITE = "\033[97m"
_COLOR_RED = "\033[91m"
_COLOR_YELLOW = "\033[93m"
_COLOR_RESET = "\033[0m"


def get_application_path() -> str:
    return os.path.dirname(os.path.abspath(sys.argv[0]))


def get_application_version() -> str:
    return __version__


def set_info(message: str) -> None:
    print(f"{_COLOR_WHITE}{message}{_COLOR_RESET}")


def set_error(message: str) -> None:
    print(f"{_COLOR_RED}{message}!{_COLOR_RESET}")


def set_warning(message: str) -> None:
    print(f"{_COLOR_YELLOW}{message}!{_COLOR_RESET}")


def check_arguments_path(arg: str) -> str:
    if not arg.endswith(os.sep):
        arg = arg + os.sep
    return arg


def check_index_file(arg: str) -> str:
    if os.path.splitext(arg)[1] != ".idx":
        raise Exception("[ERROR]: You must select BigFile_PC.idx file!")
    return arg


def debug_file(arg: str) -> str:
    directory = os.path.dirname(arg)
    name_without_ext = os.path.splitext(os.path.basename(arg))[0]
    return os.path.join(directory, name_without_ext + ".dbg")


def create_directory(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
