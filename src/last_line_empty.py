import pathlib
import sys


def make_sure_last_line_is_empty(file_name: str) -> None:
    # read file contents
    with open(file_name, "r", encoding="utf-8") as file:
        contents = file.read()

    # make sure last line is empty
    if contents[-1] != "\n":
        contents += "\n"

    # leave single trailing newline
    while contents[-2:] == "\n\n":
        contents = contents[:-1]

    # write file contents
    with open(file_name, "wb") as file:
        file.write(bytes(contents, "UTF-8"))


if __name__ == "__main__":
    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python last_line_empty.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not pathlib.Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and make sure last line is empty
    for file in pathlib.Path(file_name).glob("**/*"):
        if file.is_file():
            make_sure_last_line_is_empty(file)
