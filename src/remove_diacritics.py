# get file name from command line
import sys
import pathlib


def remove_diacritics(file_name: str) -> None:

    # read file contents
    with open(file_name, "r", encoding="utf-8") as file:
        contents = file.read()

    # replace each character from aaaaaceeeeeiiiilnooooosuuuuüüüüzzAAAAACEEEEEIIIILNOOOOOSUUUUÜÜÜÜZZ
    # with a respective character from aaaaaceeeeeiiiilnooooosuuuuüüüüzzAAAAACEEEEEIIIILNOOOOOSUUUUÜÜÜÜZZ

    mapping = {
    "ą": "a",
    "ā": "a",
    "á": "a",
    "ǎ": "a",
    "à": "a",
    "ć": "c",
    "č": "c",
    "ĉ": "c",
    "ċ": "c",
    "ę": "e",
    "ē": "e",
    "ė": "e",
    "ě": "e",
    "ī": "i",
    "į": "i",
    "ĩ": "i",
    "ĭ": "i",
    "ł": "l",
    "ń": "n",
    "ň": "n",
    "ņ": "n",
    "ō": "o",
    "ŏ": "o",
    "ó": "o",
    "ő": "o",
    "ś": "s",
    "ŝ": "s",
    "š": "s",
    "ŭ": "u",
    "ų": "u",
    "ű": "u",
    "ũ": "u",
    "ů": "u",
    "ź": "z",
    "ż": "z",
    "Ą": "A",
    "Ā": "A",
    "Á": "A",
    "Ǎ": "A",
    "À": "A",
    "Ć": "C",
    "Č": "C",
    "Ĉ": "C",
    "Ċ": "C",
    "Ę": "E",
    "Ē": "E",
    "Ė": "E",
    "Ě": "E",
    "Ī": "I",
    "Į": "I",
    "Ĩ": "I",
    "Ĭ": "I",
    "Ł": "L",
    "Ń": "N",
    "Ň": "N",
    "Ņ": "N",
    "Ō": "O",
    "Ŏ": "O",
    "Ó": "O",
    "Ő": "O",
    "Ś": "S",
    "Ŝ": "S",
    "Š": "S",
    "Ŭ": "U",
    "Ų": "U",
    "Ű": "U",
    "Ũ": "U",
    "Ů": "U",
    "Ź": "Z",
    "Ż": "Z",
    }

    for old_value, new_value in mapping.items():
        contents = contents.replace(old_value, new_value)

    # write file contents
    with open(file_name, "wb") as file:
        file.write(bytes(contents, "UTF-8"))


if __name__ == "__main__":

    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python remove_diacritics.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not pathlib.Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and remove diacritics
    for file in pathlib.Path(file_name).glob("**/*"):
        if file.is_file():
            remove_diacritics(file)
