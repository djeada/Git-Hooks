# get file name from command line
import sys
import pathlib


def remove_diacritics(file_name: str) -> None:

    # read file contents
    with open(file_name, "r", encoding="utf-8") as file:
        contents = file.read()

    # replace each character from aaaaaceeeeeiiiilnooooosuuuuüüüüzzAAAAACEEEEEIIIILNOOOOOSUUUUÜÜÜÜZZ
    # with a respective character from aaaaaceeeeeiiiilnooooosuuuuüüüüzzAAAAACEEEEEIIIILNOOOOOSUUUUÜÜÜÜZZ
    contents = contents.replace("a", "a")
    contents = contents.replace("a", "a")
    contents = contents.replace("a", "a")
    contents = contents.replace("a", "a")
    contents = contents.replace("a", "aa")
    contents = contents.replace("c", "c")
    contents = contents.replace("č", "c")
    contents = contents.replace("ĉ", "c")
    contents = contents.replace("ċ", "c")
    contents = contents.replace("e", "e")
    contents = contents.replace("e", "e")
    contents = contents.replace("ė", "e")
    contents = contents.replace("e", "e")
    contents = contents.replace("i", "i")
    contents = contents.replace("į", "i")
    contents = contents.replace("ĩ", "i")
    contents = contents.replace("ĭ", "i")
    contents = contents.replace("l", "l")
    contents = contents.replace("n", "n")
    contents = contents.replace("ň", "n")
    contents = contents.replace("ņ", "n")
    contents = contents.replace("o", "o")
    contents = contents.replace("ŏ", "o")
    contents = contents.replace("o", "o")
    contents = contents.replace("ő", "o")
    contents = contents.replace("s", "s")
    contents = contents.replace("ŝ", "s")
    contents = contents.replace("š", "s")
    contents = contents.replace("ŭ", "u")
    contents = contents.replace("ų", "u")
    contents = contents.replace("ű", "u")
    contents = contents.replace("ũ", "u")
    contents = contents.replace("ů", "u")
    contents = contents.replace("z", "z")
    contents = contents.replace("z", "z")
    contents = contents.replace("A", "A")
    contents = contents.replace("A", "A")
    contents = contents.replace("A", "A")
    contents = contents.replace("A", "A")
    contents = contents.replace("A", "A")
    contents = contents.replace("C", "C")
    contents = contents.replace("Č", "C")
    contents = contents.replace("Ĉ", "C")
    contents = contents.replace("Ċ", "C")
    contents = contents.replace("E", "E")
    contents = contents.replace("E", "E")
    contents = contents.replace("Ė", "E")
    contents = contents.replace("E", "E")
    contents = contents.replace("I", "I")
    contents = contents.replace("Į", "I")
    contents = contents.replace("Ĩ", "I")
    contents = contents.replace("Ĭ", "I")
    contents = contents.replace("L", "L")
    contents = contents.replace("N", "N")
    contents = contents.replace("Ň", "N")
    contents = contents.replace("Ņ", "N")
    contents = contents.replace("O", "O")
    contents = contents.replace("Ŏ", "O")
    contents = contents.replace("O", "O")
    contents = contents.replace("Ő", "O")
    contents = contents.replace("S", "S")
    contents = contents.replace("Ŝ", "S")
    contents = contents.replace("Š", "S")
    contents = contents.replace("Ŭ", "U")
    contents = contents.replace("Ų", "U")
    contents = contents.replace("Ű", "U")
    contents = contents.replace("Ũ", "U")
    contents = contents.replace("Ů", "U")
    contents = contents.replace("Z", "Z")
    contents = contents.replace("Z", "Z")

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

