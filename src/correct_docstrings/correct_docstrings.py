"""
Main module for the script.
"""
import sys
from pathlib import Path
from utils.script_filters import ScriptFormatter


def apply_formatting(path: Path) -> None:
    """
    Applies formatting to the file.

    :param path: path to the file.
    """
    file_content = path.read_text().splitlines()
    formatter = ScriptFormatter()
    result = formatter.format(file_content)
    path.write_text("\n".join(result))


def main():
    # check if user provided file name
    if len(sys.argv) != 2:
        # you can provide either dir name or file name
        print("Usage: python correct_docstrings.py <file_name | dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]
    path = Path(file_name)

    if not path.exists():
        print("Provided path is not valid!")
        exit()

    # if it's a file, apply formatting to it
    if path.is_file():
        apply_formatting(path)
        return

    # if it's a directory, apply formatting to all files in it
    for current_file in path.glob("**/*"):
        if not current_file.is_file() or not current_file.name.endswith(".py"):
            continue
        apply_formatting(current_file)


if __name__ == "__main__":
    main()
