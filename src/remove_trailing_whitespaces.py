import pathlib
import sys


def remove_trailing_whitespaces(file_name: str) -> None:
    # read file contents
    with open(file_name, "r", encoding="utf-8") as file:
        contents = file.read()

    # check each line for trailing whitespaces
    contents = [line.rstrip() for line in contents.splitlines()]

    # write file contents
    with open(file_name, "w", encoding="utf-8") as file:
        file.write("\n".join(contents))


if __name__ == "__main__":

    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python remove_trailing_whitespaces.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not pathlib.Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and remove diacritics
    for file in pathlib.Path(file_name).glob("**/*"):
        if file.is_file():
            remove_trailing_whitespaces(file)
