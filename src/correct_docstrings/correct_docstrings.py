"""
Main module for the script.
"""
import difflib
import argparse
from pathlib import Path
from utils.script_filters import ScriptFormatter


class ScriptArguments(argparse.ArgumentParser):
    """
    Class for parsing arguments.
    """

    def __init__(self):
        super().__init__()
        self.add_argument("file_name", help="File name or directory name")
        self.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")
        self.add_argument(
            "-c", "--check", help="Check if any changes are needed", action="store_true"
        )
        self.add_argument(
            "-d",
            "--diff",
            help="Only print diffs, without applying changes",
            action="store_true",
        )
        self.add_argument(
            "-i", "--ignore", help="Ignore files or directories", nargs="+"
        )


def apply_formatting(path: Path, in_place=True) -> bool:
    """
    Applies formatting to the file.

    :param path: path to the file.
    :param in_place: if True, changes are applied to the file, otherwise only diff is printed.
    :return: True if the file needed changes, False otherwise.
    """
    file_content = path.read_text().splitlines()
    formatter = ScriptFormatter()
    result = formatter.format(file_content.copy())

    if in_place:
        path.write_text("\n".join(result))
    else:
        # print diff
        print("printing diff")
        # create temporary file
        differences = list(difflib.Differ().compare(file_content, result))
        print("\n".join(differences))

    return result != file_content


def main():
    args = ScriptArguments().parse_args()

    if not args.file_name:
        print("Usage: python correct_docstrings.py <file_name | dir_name>")
        exit(-1)

    # check if file exists
    file_name = args.file_name
    path = Path(file_name)

    if not path.exists():
        print("Provided path is not valid!")
        exit(-1)

    changes_needed_flag = False

    # if it's a file, apply formatting to it
    if path.is_file():
        changes_needed_flag = changes_needed_flag or apply_formatting(
            path, in_place=not args.diff
        )
        return

    # if it's a directory, apply formatting to all files in it
    for current_file in path.glob("**/*"):
        if not current_file.is_file() or not current_file.name.endswith(".py"):
            continue
        changes_needed_flag = changes_needed_flag or apply_formatting(
            current_file, in_place=not args.diff
        )

    if args.check:
        exit(1 if changes_needed_flag else 0)


if __name__ == "__main__":
    main()
