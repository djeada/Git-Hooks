from dataclasses import dataclass
import sys
from pathlib import Path
from typing import List, Tuple


@dataclass
class DocstringFormatterConfig:
    """
    Configuration for the docstring formatter.
    """
    docstring: Tuple[str] = tuple()


@dataclass
class TypeHintFormatterConfig:
    """
    Configuration for the type hint formatter.
    """
    content: str = ""


@dataclass
class ScriptFormatterConfig:
    """
    Configuration for the script formatter.
    """
    path: Path
    print_diff: bool = False
    in_place: bool = False
    docstring_formatter_config: DocstringFormatterConfig = DocstringFormatterConfig()


class ScriptFormatterConfigFactory:

    @staticmethod
    def from_json(json_str: str) -> ScriptFormatterConfig:
        """
        Create a ScriptFormatterConfig from a JSON string.
        """
        pass

    @staticmethod
    def from_args(args: List[str]) -> ScriptFormatterConfig:
        """
        Create a ScriptFormatterConfig from command line arguments.
        """
        pass


class ScriptFormatter:
    def __init__(self, config: ScriptFormatterConfig):
        if not config.path.is_file():
            return

        self.content = config.path.read_text()

        content_as_list = self.add_missing_docstrings()
        # content_as_list = assert_optional_type_hints(content_as_list.copy())
        content = "\n".join(content_as_list)

        next_docstring_pos = self.find_next_docstring(0)
        while next_docstring_pos != (-1, -1):
            start_pos, end_pos = next_docstring_pos
            docstring = content.split("\n")[start_pos: end_pos + 1]
            docstring = DocstringFormatter(DocstringFormatterConfig(docstring)).format()
            content_list_of_lines = content.split("\n")
            content_list_of_lines = (
                    content_list_of_lines[:start_pos]
                    + docstring
                    + content_list_of_lines[end_pos + 1:]
            )
            content = "\n".join(content_list_of_lines)

            next_docstring_pos = self.find_next_docstring(start_pos + len(docstring) + 1
                                                          )

        config.path.write_text(content)

    def add_missing_docstrings(self) -> List[str]:
        """
        Add docstring to file.
        :return: list of lines in file
        """

        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

        i = 0
        content = self.content.split("\n").copy()
        while i < len(content) - 1:
            line = content[i].strip()
            indentation = len(content[i]) - len(content[i].lstrip()) + 4
            if line.startswith("def"):
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                if content[end_index + 1].strip() not in possible_docstring_start:
                    # find the parameters of the function between ()

                    parameters = extract_parameters(content, i, end_index)

                    # add docstring
                    content.insert(end_index + 1, f'{" " * indentation}"""')
                    content.insert(
                        end_index + 2, f'{" " * indentation}Description of function \n'
                    )
                    # add parameters
                    end_index += 3
                    for parameter in parameters:
                        parameter = parameter.split(":")[0]
                        content.insert(
                            end_index, f'{" " * indentation}:param {parameter.strip()}:'
                        )
                        end_index += 1
                    # add return
                    content.insert(end_index, f'{" " * indentation}:return:')
                    content.insert(end_index + 1, f'{" " * indentation}"""')
            i += 1

        return content

    def find_next_docstring(self, index: int) -> Tuple[int, int]:
        """
        Finds next docstring in content starting from index. Returns (-1, -1) if no docstring found.

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

        content = self.content.split("\n")
        for i in range(index, len(content)):
            line = content[i].strip()
            if line in possible_docstring_start:
                for j in range(i + 1, len(content)):
                    next_line = content[j].strip()
                    if next_line == corresponding_docstring_end[line]:
                        return i, j

        return -1, -1

    def preserve_parameter_order(self) -> List[str]:
        """
        """
        content = self.content.split("\n").copy()
        start_index, end_index = self.find_next_docstring(0)

        if start_index == -1:
            return content

        # find the index of first 'def' above start_index
        i = start_index - 1
        while i >= 0:
            line = content[i].strip()
            if line.startswith("def"):
                break
            i -= 1

        if i == -1:
            return content

        parameters_from_function = extract_parameters(content, i, start_index)

        docstring = content[start_index: end_index + 1]
        parameters_from_docstring = []

        for line in docstring:
            if line.strip().startswith(":param"):
                parameters_from_docstring.append(line)

        # order of parameters in docstring must match the order of parameters in parameters
        for i, parameter in enumerate(parameters_from_function):
            parameter_name = parameter.split(":")[0].strip()
            # find in which line the parameter in parameters_from_docstring is
            flag = False
            for j, line in enumerate(parameters_from_docstring):
                if f":param {parameter_name}" in line:
                    if i != j:
                        # swap j and i if i < len(parameters_from_docstring)
                        if i < len(parameters_from_docstring):
                            parameters_from_docstring[j], parameters_from_docstring[i] = parameters_from_docstring[i], \
                                                                                         parameters_from_docstring[j]
                        else:
                            flag = True
                    break
            if flag:
                # add parameter to docstring if it is not in docstring
                parameters_from_docstring.insert(i, f":param {parameter_name}:")

        # remove all lines starting with :param from docstring
        for i, line in reversed(list(enumerate(docstring.copy()))):
            if line.strip().startswith(":param"):
                docstring.pop(i)

        # remove the last line of docstring if it starts with :return:
        n = len(docstring) - 1
        if n > 0 and docstring[n - 1].strip().startswith(":return"):
            n -= 1
        if n < 0:
            n = 0

        # append parameters from parameters_from_docstring to docstring
        for parameter in parameters_from_docstring:
            docstring.insert(n, parameter)
            n += 1

        content[start_index: end_index + 1] = docstring
        return content


class TypeHintsFormatter:
    def __init__(self, config: TypeHintFormatterConfig):
        self.content = config.content

    def optional_type_hints(self) -> List[str]:
        """
        Find parameters with default value None and add Optional[type] to them.

        :return: list of lines in file
        """

        i = 0
        content = self.content.split("\n").copy()
        while i < len(content) - 1:
            line = content[i].strip()

            if line.startswith("def"):
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                parameters = extract_parameters(content, i, end_index)

                # find the parameters with default value None
                parameters_with_default_value_none = [
                    parameter for parameter in parameters if "= None" in parameter
                ]
                # add Optional[type] to parameters with default value None
                for parameter in parameters_with_default_value_none:
                    parameter_name = parameter.split(":")[0].strip()
                    parameter_type = parameter.split(":")[1].strip()
                    parameter_type = parameter_type.replace("= None", "").rstrip()
                    for j in range(i, end_index + 1):
                        content[j] = content[j].replace(
                            parameter,
                            f"{parameter_name}: Optional[{parameter_type}] = None",
                        )

            i += 1

        return content


class DocstringFormatter:
    def __init__(self, config: DocstringFormatterConfig):
        self.docstring = config.docstring

    def format(self) -> str:
        self.docstring = self.empty_line_between_description_and_param_list()
        self.docstring = self.no_unnecessary_prefixes()
        self.docstring = self.single_whitespace_after_second_semicolon()
        # docstring = convert_to_third_person(docstring.copy())
        return self.docstring

    def single_whitespace_after_second_semicolon(self) -> List[str]:
        """
        Find the lines containing prefixes = [":param", ":return", ":raises"].
        For those lines make sure that there is only one whitespace after the second semicolon.

        :return: list of lines in docstring
        """
        prefixes = [":param", ":return", ":raises"]
        docstring = self.docstring.copy()
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

    def empty_line_between_description_and_param_list(self,

                                                      ) -> List[str]:
        """
        make sure empty line between description and list of params
        find first param in docstring and check if there is description above it
        if so, make sure that there is empty line between description and param list

        :return: list of lines in docstring
        """
        prefixes = [":param", ":return", ":raises"]
        start_of_param_list = -1
        docstring = self.docstring.copy()

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

        # remove all empty lines before param list and enter a single empty line
        # before param list
        while docstring[start_of_param_list - 1].strip() == "":
            docstring.pop(start_of_param_list - 1)
            start_of_param_list -= 1

        docstring.insert(start_of_param_list, "")

        return docstring

    def no_unnecessary_prefixes(self) -> List[str]:
        """
        Make sure that lines that contain :param or :return or :raises are prefixed with ": "
        and there are no unnecessary prefixes, only whitespace is allowed before the prefix

        :return: list of lines in docstring
        """
        prefixes = [":param", ":return", ":raises"]
        docstring = self.docstring.copy()

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


class ThirdPersonConverter:

    def __init__(self, content: str):
        self.content = content
        self.blocking_previous_words = [
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

    def convert(self):
        # check which line starts with ":"
        end_index = -1
        for i in range(len(self.content)):
            line = self.content[i].strip()
            if line.startswith(":"):
                end_index = i
                break

        if end_index == -1:
            return self.content

        for i in range(1, end_index):
            line = self.content[i]
            leading_whitespaces = len(line) - len(line.lstrip())
            new_line = " " * leading_whitespaces
            previous_word = ""
            for word in line.split():
                word, punctuation = ThirdPersonConverter.split_word_punctuation(word)
                if previous_word not in self.blocking_previous_words:
                    if ThirdPersonConverter.is_verb(word) and not word.endswith("s"):
                        word += "s"
                new_line += word + punctuation + " "
                previous_word = word

            self.content[i] = new_line.rstrip()

        return self.content

    @staticmethod
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

    @staticmethod
    def is_verb(word: str) -> bool:
        """
        Check if word is a verb

        :param word: word to check
        :return: True if word is a verb, False otherwise
        """
        # open resources/verbs.txt
        # each line in that file is a verb
        # check if word is in that file

        content = Path(__file__).parent.joinpath("../resources/verbs.txt").read_text()

        verbs = content.split("\n")
        return word.lower().strip() in verbs


def extract_parameters(content: List[str], start_index: int, end_index: int) -> List[str]:
    """
    """
    parameters_text = "".join(content[start_index: end_index + 1]).replace(
        "\n", " "
    )
    parameters_text = parameters_text[
                      parameters_text.find("(") + 1: parameters_text.rfind(")")
                      ]
    parameters = [
        param.strip()
        for param in parameters_text.split(",")
        if param.strip() and not param.strip().endswith("]")
    ]
    return parameters


def main():
    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python correct_sphinx_docstring.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and make sure last line is empty
    for file in Path(file_name).glob("**/*"):
        if not file.is_file():
            continue
        config = ScriptFormatterConfig(file)
        ScriptFormatter(config)


if __name__ == "__main__":
    main()
