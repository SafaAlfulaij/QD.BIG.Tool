"""Port of Program.cs, extended with a `pack` mode."""

import os
import sys

from . import big_file_debug, big_file_pack, big_file_unpack, utils

_TITLE = "Quantic Dream BigFile Unpacker"

_COLOR_GREEN = "\033[92m"
_COLOR_WHITE = "\033[97m"
_COLOR_YELLOW = "\033[93m"
_COLOR_RESET = "\033[0m"


def _print_usage() -> None:
    print(f"{_COLOR_WHITE}[Usage]")
    print("    QD.Unpacker unpack <IndexFile> <Directory>")
    print("    QD.Unpacker pack <IndexFile> <SourceDirectory> <OutputDirectory>\n")
    print("    IndexFile - Source of IDX file")
    print("    Directory - Destination directory for unpacked resources")
    print("    SourceDirectory - Directory with (optionally modified) unpacked resources")
    print(f"    OutputDirectory - Destination directory for the repacked IDX/DAT files\n{_COLOR_RESET}")
    print(f"{_COLOR_YELLOW}[Examples]")
    print(r"    QD.Unpacker unpack E:\Games\BEYOND Two Souls\BigFile_PC.idx D:\Unpacked")
    print(r"    QD.Unpacker unpack E:\Games\Detroit Become Human\BigFile_PC.idx D:\Unpacked")
    print(r"    QD.Unpacker pack E:\Games\HEAVY RAIN\Resources\BigFile_WIN.idx D:\Unpacked D:\Repacked")
    print(f"{_COLOR_RESET}", end="")


def main() -> int:
    args = sys.argv[1:]

    print(f"{_COLOR_GREEN}{_TITLE}")
    print(f"(c) 2022 Ekey (h4x0r) / v{utils.get_application_version()}\n{_COLOR_RESET}")

    mode = args[0] if args else None

    if mode == "unpack" and len(args) == 3:
        return _run_unpack(args[1], args[2])

    if mode == "pack" and len(args) == 4:
        return _run_pack(args[1], args[2], args[3])

    _print_usage()
    return 0


def _run_unpack(index_arg: str, directory_arg: str) -> int:
    try:
        index_file = utils.check_index_file(index_arg)
        output = utils.check_arguments_path(directory_arg)
        debug_file = utils.debug_file(index_arg)

        if not os.path.isfile(index_file):
            utils.set_error(f"[ERROR]: Input index file -> {index_file} <- does not exist")
            return 1

        if os.path.isfile(debug_file):
            big_file_debug.load(debug_file)

        big_file_unpack.do_it(index_file, output)
    except Exception as exc:
        utils.set_error(str(exc))
        return 1

    return 0


def _run_pack(index_arg: str, src_directory_arg: str, dst_directory_arg: str) -> int:
    try:
        index_file = utils.check_index_file(index_arg)
        src_folder = utils.check_arguments_path(src_directory_arg)
        dst_folder = utils.check_arguments_path(dst_directory_arg)
        debug_file = utils.debug_file(index_arg)

        if not os.path.isfile(index_file):
            utils.set_error(f"[ERROR]: Input index file -> {index_file} <- does not exist")
            return 1

        if not os.path.isdir(src_folder):
            utils.set_error(f"[ERROR]: Source directory -> {src_folder} <- does not exist")
            return 1

        if os.path.isfile(debug_file):
            big_file_debug.load(debug_file)

        big_file_pack.do_it(index_file, src_folder, dst_folder)
    except Exception as exc:
        utils.set_error(str(exc))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
