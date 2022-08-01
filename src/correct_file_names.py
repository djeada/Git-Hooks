import pathlib
import sys


def correct_file_name(file_name: str) -> None:

    path = pathlib.Path(file_name)
    correct_file_name = path.name.replace(" ", "_").lower()

    if correct_file_name != path.name:
        path.rename(path.absolute().parent / correct_file_name)


if __name__ == "__main__":

    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python correct_file_names.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not pathlib.Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and make sure last line is empty
    for file in pathlib.Path(file_name).glob("**/*"):
        if file.is_file() or file.is_dir():
            correct_file_name(file)
