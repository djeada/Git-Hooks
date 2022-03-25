import sys
from pathlib import Path
from typing import List, Tuple


def correct_sphinx_docstrings(file_name: str) -> bool:
    """
    Corrects Sphinx docstrings in file_name.

    :param file_name: name of file to correct
    :return: True if file was changed, False otherwise
    """
    # read file contents
    contents = Path(file_name).read_text()

    next_docstring_pos = find_next_docstring(contents.split("\n"), 0)
    while next_docstring_pos != (-1, -1):
        start_pos, end_pos = next_docstring_pos
        docstring = contents.split("\n")[start_pos:end_pos + 1]
        docstring = assert_empty_line_between_description_and_param_list(docstring)
        docstring = assert_no_unnecessary_prefixes(docstring)
        docstring = assert_single_whitespace_after_second_semicolon(docstring)
        contents_list_of_lines = contents.split("\n")
        contents_list_of_lines = contents_list_of_lines[:start_pos] + docstring + contents_list_of_lines[end_pos + 1:]
        contents = "\n".join(contents_list_of_lines)

        next_docstring_pos = find_next_docstring(contents.split("\n"), start_pos + len(docstring) + 1)

    flag = Path(file_name).read_text() != contents

    # write file contents
    Path(file_name).write_text(contents)

    return flag
        

def assert_single_whitespace_after_second_semicolon(docstring: List[str]) -> List[str]:
    """
    Find the lines conaining prefixes = [":param", ":return", ":raises"].
    For those lines make sure that there is only one whitespace after the second semicolon.

    :param docstring: list of lines in docstring
    :return: list of lines in docstring
    """
    prefixes = [":param", ":return", ":raises"]
    for i in range(len(docstring)):
        line = docstring[i]
        for prefix in prefixes:
            index = line.find(prefix)
            if index != -1:
                index_of_second_semicolon = line.find(":", index + len(prefix))
                if index_of_second_semicolon != -1:
                    line_after_second_semicolon = line[index_of_second_semicolon + 1:]

                    while line_after_second_semicolon.startswith(" "):
                        line_after_second_semicolon = line_after_second_semicolon[1:]

                    if len(line_after_second_semicolon) > 1:
                        line_after_second_semicolon = " " + line_after_second_semicolon[0].upper() + line_after_second_semicolon[1:]

                    docstring[i] = line[:index_of_second_semicolon + 1] + line_after_second_semicolon

    return docstring


def assert_empty_line_between_description_and_param_list(docstring: List[str]) -> List[str]:
    """
    make sure empty line between description and list of params
    find first param in docstring and check if there is description above it
    if so, make sure that there is empty line between description and param list
    
    :param docstring: list of lines in docstring
    :return: list of lines in docstring
    """
    prefixes = [":param", ":return", ":raises"]
    start_of_param_list = -1

    for i in range(len(docstring)):
        line = docstring[i].strip()
        # check if it starts with prefix
        for prefix in prefixes:
            if line.startswith(prefix) and i > 1:
                start_of_param_list = i
                break

        if start_of_param_list != -1:
            break


    if start_of_param_list == -1:
        return docstring

    # remove all empty lines before param list and enter a single empty line before param list
    while docstring[start_of_param_list - 1].strip() == "":
        docstring.pop(start_of_param_list - 1)
        start_of_param_list -= 1

    docstring.insert(start_of_param_list, "")

    return docstring


def assert_no_unnecessary_prefixes(docstring: List[str]) -> List[str]:
    """
    Make sure that lines that contain :param or :return or :raises are prefixed with ": "
    and there are no unnecessary prefixes, only whitespace is allowed before the prefix

    :param docstring: list of lines in docstring
    :return: list of lines in docstring
    """
    prefixes = [":param", ":return", ":raises"]
    for i in range(len(docstring)):
        line = docstring[i]
        # check if one prefixes is in line
        for prefix in prefixes:
            index = line.find(prefix)
            if index != -1:
                # make sure there is only whitespace before prefix
                # replace all characters before prefix with whitespace
                docstring[i] = " " * index + line[index:]
                break

    return docstring


def find_next_docstring(contents: List[str], index: int) -> Tuple[int, int]:
    """
    Finds next docstring in contents starting from index. Returns (-1, -1) if no docstring found.

    :param contents: list of lines in file
    :param index: index to start looking for docstring
    :return: start and end position of docstring
    """
    possible_docstring_start = ["\"\"\"", "'''", "r\"\"\"", "r'''"]
    corresponding_docstring_end = {"\"\"\"": "\"\"\"", "'''": "'''", "r\"\"\"": "\"\"\"", "r'''": "'''"}

    for i in range(index, len(contents)):
        line = contents[i].strip()
        if line in possible_docstring_start:
            for j in range(i + 1, len(contents)):
                next_line = contents[j].strip()
                if next_line == corresponding_docstring_end[line]:
                    return i, j

    return -1, -1


if __name__ == "__main__":

    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python correct_sphinx_docstrings.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and make sure last line is empty
    for file in Path(file_name).glob("**/*"):
        if file.is_file():
            correct_sphinx_docstrings(file)
