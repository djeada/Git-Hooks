import re
import sys
from pathlib import Path
from typing import List, Tuple

"""
TODO:
- print a message when line is being changed
- make sure that : is last char in :param param_name:
"""


def correct_sphinx_docstrings(file_name: str) -> bool:
    """
    Corrects Sphinx docstrings in file_name.

    :param file_name: name of file to correct
    :return: True if file was changed, False otherwise
    """
    # read file contents
    contents = Path(file_name).read_text()

    content_as_list = add_missing_docstring(contents.split("\n").copy())
    contents = "\n".join(content_as_list)

    next_docstring_pos = find_next_docstring(contents.split("\n"), 0)
    while next_docstring_pos != (-1, -1):
        start_pos, end_pos = next_docstring_pos
        docstring = contents.split("\n")[start_pos : end_pos + 1]
        docstring = assert_empty_line_between_description_and_param_list(
            docstring.copy()
        )
        docstring = assert_no_unnecessary_prefixes(docstring.copy())
        docstring = assert_single_whitespace_after_second_semicolon(docstring.copy())
        docstring = convert_to_third_person(docstring.copy())
        contents_list_of_lines = contents.split("\n")
        contents_list_of_lines = (
            contents_list_of_lines[:start_pos]
            + docstring
            + contents_list_of_lines[end_pos + 1 :]
        )
        contents = "\n".join(contents_list_of_lines)

        next_docstring_pos = find_next_docstring(
            contents.split("\n"), start_pos + len(docstring) + 1
        )

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
                    line_after_second_semicolon = line[index_of_second_semicolon + 1 :]

                    while line_after_second_semicolon.startswith(" "):
                        line_after_second_semicolon = line_after_second_semicolon[1:]

                    if len(line_after_second_semicolon) > 1:
                        line_after_second_semicolon = (
                            " "
                            + line_after_second_semicolon[0].upper()
                            + line_after_second_semicolon[1:]
                        )

                    docstring[i] = (
                        line[: index_of_second_semicolon + 1]
                        + line_after_second_semicolon
                    )

    return docstring


def assert_empty_line_between_description_and_param_list(
    docstring: List[str]
) -> List[str]:
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


def convert_to_third_person(docstring: List[str]) -> List[str]:
    """
    Convert docstring to third person form

    :param docstring: list of lines in docstring
    :return: list of lines in docstring
    """
    # check which line starts with ":"
    end_index = -1
    for i in range(len(docstring)):
        line = docstring[i].strip()
        if line.startswith(":"):
            end_index = i
            break

    if end_index == -1:
        return docstring

    def split_word_punctuation(word: str) -> Tuple[str, str]:
        """
        Split word into two parts: word and punctuation

        :param word: word to split
        :return: word and punctuation
        """
        letters = ""

        end_index = -1
        for i, letter in enumerate(word):
            if not letter.isalpha():
                end_index = i
                break
            letters += letter

        punctuation = word[end_index:] if end_index != -1 else ""

        return letters, punctuation

    def is_verb(word: str) -> bool:
        """
        Check if word is a verb

        :param word: word to check
        :return: True if word is a verb, False otherwise
        """
        # open resources/verbs.txt
        # each line in that file is a verb
        # check if word is in that file

        contents = Path(__file__).parent.joinpath("../resources/verbs.txt").read_text()

        verbs = contents.split("\n")
        return word.lower().strip() in verbs

    blocking_previous_words = [
        "to",
        "a",
        "an",
        "the",
        "for",
        "in",
        "of",
        "and",
        "or",
        "as",
        "if",
        "but",
        "nor",
        "so",
        "yet",
        "at",
        "by",
        "from",
        "into",
        "like",
        "over",
        "after",
        "before",
        "between",
        "into",
        "through",
        "with",
        "without",
        "during",
        "without",
        "until",
        "up",
        "upon",
        "about",
        "above",
        "across",
        "after",
        "against",
        "along",
        "amid",
        "among",
        "anti",
        "around",
        "as",
        "at",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "besides",
        "between",
        "beyond",
        "concerning",
        "considering",
        "despite",
        "down",
        "during",
        "except",
        "excepting",
        "excluding",
        "following",
        "for",
        "from",
        "in",
        "inside",
        "into",
        "like",
        "minus",
        "near",
        "of",
        "off",
        "on",
        "onto",
        "opposite",
        "outside",
        "over",
        "past",
        "per",
        "plus",
        "regarding",
        "round",
        "save",
        "since",
        "than",
        "through",
        "to",
        "toward",
        "towards",
        "under",
        "underneath",
        "unlike",
        "until",
        "up",
        "upon",
        "versus",
        "via",
        "with",
        "within",
        "without",
    ]

    for i in range(1, end_index):
        line = docstring[i]
        leading_whitespaces = len(line) - len(line.lstrip())
        new_line = " " * leading_whitespaces
        previous_word = ""
        for word in line.split():
            word, punctuation = split_word_punctuation(word)
            if previous_word not in blocking_previous_words:
                if is_verb(word) and not word.endswith("s"):
                    word += "s"
            new_line += word + punctuation + " "
            previous_word = word

        docstring[i] = new_line.rstrip()

    return docstring


def find_next_docstring(contents: List[str], index: int) -> Tuple[int, int]:
    """
    Finds next docstring in contents starting from index. Returns (-1, -1) if no docstring found.

    :param contents: list of lines in file
    :param index: index to start looking for docstring
    :return: start and end position of docstring
    """
    possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]
    corresponding_docstring_end = {
        '"""': '"""',
        "'''": "'''",
        'r"""': '"""',
        "r'''": "'''",
    }

    for i in range(index, len(contents)):
        line = contents[i].strip()
        if line in possible_docstring_start:
            for j in range(i + 1, len(contents)):
                next_line = contents[j].strip()
                if next_line == corresponding_docstring_end[line]:
                    return i, j

    return -1, -1


def add_missing_docstring(contents: List[str]) -> List[str]:
    """
    Add docstring to file.

    :param contents: list of lines in file
    :return: list of lines in file
    """

    possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

    i = 0
    while i < len(contents) - 1:
        line = contents[i].strip()
        indentation = len(contents[i]) - len(contents[i].lstrip())
        if line.startswith("def"):
            if contents[i + 1].strip() not in possible_docstring_start:
                # find the parameters of the function between ()
                parameters = re.findall(r"\((.*?)\)", line)
                # add docstring
                contents.insert(i + 1, f'{" " * indentation}"""')
                contents.insert(i + 2, f'{" " * indentation}Description of function \n')
                # add parameters
                i += 3
                for parameter in parameters[0].split(","):
                    contents.insert(
                        i, f'{" " * indentation}:param {parameter.strip()}:'
                    )
                    i += 1
                # add return
                contents.insert(i, f'{" " * indentation}:return:')
                contents.insert(i + 1, f'{" " * indentation}"""')
        i += 1

    return contents


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
