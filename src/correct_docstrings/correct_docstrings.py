"""
Main module for the script.
"""
import difflib
import sys
import argparse
from pathlib import Path
from utils.script_filters import ScriptFormatter

# TODO:
# 1. add ignored verbs


class ScriptArguments(argparse.ArgumentParser):
    """
    Class for parsing arguments.
    """
    def __init__(self):
        super().__init__()
        self.add_argument("file_name", help="File name or directory name")
        self.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")
        self.add_argument("-d", "--diff", help="Only print diffs, without applying changes", action="store_true")
        self.add_argument("-i", "--ignore", help="Ignore files or directories", nargs="+")

def apply_formatting(path: Path, in_place=True) -> None:
    """
    Applies formatting to the file.

    :param path: path to the file.
    """
    file_content = path.read_text().splitlines()
    formatter = ScriptFormatter()
    result = formatter.format(file_content)

    if in_place:
        path.write_text("\n".join(result))
    else:
        # print diff
        print("printing diff")
        for line in difflib.unified_diff(file_content, result, fromfile=path.name, tofile=path.name):
            print(line)


def main():
    args = ScriptArguments().parse_args()

    if not args.file_name:
        print("Usage: python correct_docstrings.py <file_name | dir_name>")
        exit()


    # check if file exists
    file_name = args.file_name
    path = Path(file_name)

    if not path.exists():
        print("Provided path is not valid!")
        exit()

    # if it's a file, apply formatting to it
    if path.is_file():
        apply_formatting(path, in_place=not args.diff)
        return

    # if it's a directory, apply formatting to all files in it
    for current_file in path.glob("**/*"):
        if not current_file.is_file() or not current_file.name.endswith(".py"):
            continue
        apply_formatting(current_file, in_place=not args.diff)


if __name__ == "__main__":
    main()
