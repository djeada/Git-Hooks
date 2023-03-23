import copy
import re
from typing import List, Tuple

from src.docstring_physician.parsers.param_parser.data import ParameterData


class ParametersExtractor:
    def __init__(self, content: List[str]):
        self.content = self._extract_first_function(content)

    def _extract_first_function(self, content: List[str]) -> List[str]:
        content_str = "".join(content)

        # Locate the first function definition
        function_match = re.search(r"\bdef\b\s+\w+\s*\(", content_str)
        if not function_match:
            return []

        # Locate the end of the first function definition
        open_brackets = 1
        end_index = function_match.end()
        while open_brackets > 0 and end_index < len(content_str):
            if content_str[end_index] == "(":
                open_brackets += 1
            elif content_str[end_index] == ")":
                open_brackets -= 1
            end_index += 1

        first_function_str = content_str[function_match.start() : end_index]
        return first_function_str.split("\n")

    def extract_parameters(
        self,
        ignored_parameters=["cls", "self", "__class__"],
    ) -> List[ParameterData]:

        content_str = "".join(self.content).replace("\n", " ")

        # Extract the parameter string
        parameter_start = content_str.find("(") + 1
        parameter_end = content_str.find(")")
        parameters_text = content_str[parameter_start:parameter_end]

        # A regex pattern to correctly handle parameters with and without type hints
        pattern = re.compile(
            r"\s*(?P<name>\w+)\s*(?::\s*(?P<type>(?:(?:[^\s,=]+\[.*?\])|(?:[^\s,=]+)))\s*)?(?:=\s*(?P<default>[^,]+))?\s*(?:,|$)"
        )

        parameters = []
        for match in pattern.finditer(parameters_text):
            name, type_hint, default_value = match.groups()
            if type_hint is None:
                type_hint = ""
            if default_value is None:
                default_value = ""
            parameters.append(ParameterData(name, type_hint, default_value))

        parameters = [
            parameter
            for parameter in parameters
            if parameter.name not in ignored_parameters
        ]

        return parameters

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
