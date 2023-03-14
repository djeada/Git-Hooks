"""
Helper functions for the correct_docstrings package.
"""
import copy
from dataclasses import dataclass
from typing import List, Tuple


class DocstringsLocalizer:
    """
    Finds docstrings in a python file.

    :param content: python file content as a list of lines
    """

    def __init__(self, content: List[str]):
        self.content = content

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

        for i in range(index, len(self.content)):
            line = self.content[i].strip()
            if line in possible_docstring_start:
                for j in range(i + 1, len(self.content)):
                    next_line = self.content[j].strip()
                    if next_line == corresponding_docstring_end[line]:
                        return i, j

        return -1, -1

    def find_all_docstrings(self) -> List[Tuple[int, int]]:
        """
        Finds all docstrings in content. Returns empty list if no docstring found.

        :return: list of start and end position of docstrings
        """
        docstrings = []
        next_docstring_pos = self.find_next_docstring(0)
        while next_docstring_pos != (-1, -1):
            docstrings.append(next_docstring_pos)
            next_docstring_pos = self.find_next_docstring(next_docstring_pos[1] + 1)

        return docstrings


@dataclass
class ParameterData:
    """
    Holds information about a parameter.

    :param name: name of the parameter
    :param type_hint: type hint of the parameter
    :param default_value: default value of the parameter
    :param description: description of the parameter
    """

    name: str
    type_hint: str
    default_value: str = ""
    description: str = ""

    def __str__(self):
        return (
            f"{self.name}: {self.type_hint} = {self.default_value}"
            if self.default_value
            else f"{self.name}: {self.type_hint}"
        )


class ParametersExtractor:
    """
    Extracts parameters from a python function header.

    :param content: python file content as a list of lines
    """

    def __init__(self, content: List[str]):
        self.content = content

    def extract_parameters(
        self,
        start_index: int = 0,
        end_index: int = -1,
        ignored_parameters=["cls", "self", "__class__"],
    ) -> List[ParameterData]:
        """
        Parses the text between start_index and end_index and extracts the parameters if any.

        :param start_index: start index of the text to parse
        :param end_index: end index of the text to parse, if -1 then the end of the content
        :return: list of parameters extracted
        """

        if end_index == -1:
            end_index = len(self.content) - 1

        parameters_text = "".join(self.content[start_index : end_index + 1]).replace(
            "\n", " "
        )
        parameters_text = parameters_text[
            parameters_text.find("(") + 1 : parameters_text.rfind(")")
        ]

        parameters = []
        for parameter in parameters_text.split(","):
            parameter = parameter.strip()
            if parameter:
                parameter_name = parameter.split(":")[0].strip()
                parameter_type = (
                    parameter.split(":")[1].strip()
                    if len(parameter.split(":")) > 1
                    else ""
                )
                default_value = ""
                if "=" in parameter_type:
                    default_value = parameter_type.split("=")[1].strip()
                    parameter_type = parameter_type.split("=")[0].strip()
                parameters.append(
                    ParameterData(parameter_name, parameter_type, default_value)
                )

        parameters = [
            parameter
            for parameter in parameters
            if parameter.name not in ignored_parameters
        ]

        return parameters

    def extract_parameter_names(
        self, start_index: int = 0, end_index: int = -1
    ) -> List[str]:
        """
        Parses the text between start_index and end_index and extracts the names of the parameters if any.

        :param start_index: start index of the text to parse
        :param end_index: end index of the text to parse, if -1 then the end of the content
        :return: list of parameter names extracted
        """
        return [
            parameter.name
            for parameter in self.extract_parameters(start_index, end_index)
        ]

    def replace_parameters(
        self,
        new_parameters: List[ParameterData],
        start_index: int = 0,
        end_index: int = -1,
    ) -> List[str]:
        """
        Replaces the parameters in the text between start_index and end_index with the new parameters.

        :param new_parameters: list of parameters to replace with
        :param start_index: start index of the text to parse
        :param end_index: end index of the text to parse, if -1 then the end of the content
        :return: new content with replaced parameters
        """

        if end_index == -1:
            end_index = len(self.content) - 1

        considered_content = self.content[start_index : end_index + 1]

        def find_range_of_function_header(text: List[str]) -> Tuple[int, int]:
            """
            Finds the range of the function header in the text.

            :param text: text to parse
            :return: start and end index of the function header
            """
            __start_index = 0
            while __start_index < len(text):
                if "def" in text[__start_index]:
                    break
                __start_index += 1
            __end_index = __start_index
            while __end_index < len(text):
                if "):" in text[__end_index] or ") ->" in text[__end_index - 1]:
                    break
                __end_index += 1

            if __start_index > __end_index:
                raise ValueError("Couldn't find the function header in the text")

            return __start_index, __end_index

        start_index_of_header, end_index_of_header = find_range_of_function_header(
            considered_content
        )

        header_content = considered_content[
            start_index_of_header : end_index_of_header + 1
        ]

        new_content = copy.deepcopy(header_content)
        parameters = self.extract_parameters(start_index, end_index)
        for i, parameter in enumerate(parameters):
            for j, line in enumerate(new_content):
                if parameter.name in line:
                    _start_index = line.index(parameter.name)
                    _end_index = _start_index + 1
                    while _end_index < len(line):
                        if line[_end_index] in ",)":
                            break
                        _end_index += 1

                    new_content[j] = (
                        line[:_start_index] + str(new_parameters[i]) + line[_end_index:]
                    )

        considered_content[
            start_index_of_header : end_index_of_header + 1
        ] = new_content
        self.content[start_index : end_index + 1] = considered_content

        return self.content
