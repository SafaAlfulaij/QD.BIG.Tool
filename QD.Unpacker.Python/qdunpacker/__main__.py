"""Port of Program.cs."""

import os
import sys

from . import big_file_debug, big_file_unpack, utils

_TITLE = "Quantic Dream BigFile Unpacker"

_COLOR_GREEN = "\033[92m"
_COLOR_WHITE = "\033[97m"
_COLOR_YELLOW = "\033[93m"
_COLOR_RESET = "\033[0m"


def main() -> int:
    args = sys.argv[1:]

    print(f"{_COLOR_GREEN}{_TITLE}")
    print(f"(c) 2022 Ekey (h4x0r) / v{utils.get_application_version()}\n{_COLOR_RESET}")

    if len(args) != 2:
        print(f"{_COLOR_WHITE}[Usage]")
        print("    QD.Unpacker <m_File> <m_Directory>\n")
        print("    m_File - Source of IDX file")
        print(f"    m_Directory - Destination directory\n{_COLOR_RESET}")
        print(f"{_COLOR_YELLOW}[Examples]")
        print(r"    QD.Unpacker E:\Games\BEYOND Two Souls\BigFile_PC.idx D:\Unpacked")
        print(r"    QD.Unpacker E:\Games\Detroit Become Human\BigFile_PC.idx D:\Unpacked")
        print(f"    QD.Unpacker E:\\Games\\HEAVY RAIN\\Resources\\BigFile_WIN.idx D:\\Unpacked{_COLOR_RESET}")
        return 0

    try:
        index_file = utils.check_index_file(args[0])
        output = utils.check_arguments_path(args[1])
        debug_file = utils.debug_file(args[0])

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


if __name__ == "__main__":
    sys.exit(main())
