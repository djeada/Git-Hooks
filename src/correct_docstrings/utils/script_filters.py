"""
Global filters, applied to the whole script (text file) as opposed to a single docstring.
"""
from abc import ABC
from typing import List, Tuple

from src.correct_docstrings.utils.config import (DocstringFormatterConfig,
                                                 ScriptFormatterConfig)
from src.correct_docstrings.utils.docstring_filters import DocstringFormatter


class ScriptFilterBase(ABC):
    def format(self, content: List[str]) -> List[str]:
        """
        Formats the content.

        :param content: list of lines in the file.
        :return: formatted list of lines in the file.
        """
        pass


class AddMissingDocstrings(ScriptFilterBase):
    def format(self, content: List[str]) -> List[str]:
        """
        Add docstring to file.
        :return: list of lines in file
        """

        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

        i = 0
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


class PreserveParameterOrder(ScriptFilterBase):
    def format(self, content) -> List[str]:
        """ """
        localizer = DocstringsLocalizer(content)
        start_index, end_index = localizer.find_next_docstring(0)

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

        docstring = content[start_index : end_index + 1]
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
                            (
                                parameters_from_docstring[j],
                                parameters_from_docstring[i],
                            ) = (
                                parameters_from_docstring[i],
                                parameters_from_docstring[j],
                            )
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

        content[start_index : end_index + 1] = docstring
        return content


class ScriptFormatter:
    def __init__(self, config: ScriptFormatterConfig):
        if not config.path.is_file():
            return

        self.content = config.path.read_text()

        initial_filters = [AddMissingDocstrings()]

        content_as_list = self.content.split("\n")

        for script_filter in initial_filters:
            content_as_list = script_filter.format(content_as_list)

        # find_all_docstrings and apply  DocstringFormatter.format(docstring) to each docstring
        # replace the indices from content_as_list with the formatted docstrings

        formatter = DocstringFormatter()
        localizer = DocstringsLocalizer(content_as_list)
        start_index, end_index = localizer.find_next_docstring(0)

        while start_index != -1:
            docstring = content_as_list[start_index : end_index + 1]
            formatted_docstring = formatter.format(docstring)
            content_as_list[start_index : end_index + 1] = formatted_docstring
            start_index, end_index = DocstringsLocalizer(
                content_as_list
            ).find_next_docstring(start_index + len(formatted_docstring) + 1)

        config.path.write_text("\n".join(content_as_list))


class DocstringsLocalizer:
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
        next_docstring_pos = self.find_next_docstring(self.content, 0)
        while next_docstring_pos != (-1, -1):
            docstrings.append(next_docstring_pos)
            next_docstring_pos = self.find_next_docstring(
                self.content, next_docstring_pos[1] + 1
            )

        return docstrings


def extract_parameters(
    content: List[str], start_index: int, end_index: int
) -> List[str]:
    """ """
    parameters_text = "".join(content[start_index : end_index + 1]).replace("\n", " ")
    parameters_text = parameters_text[
        parameters_text.find("(") + 1 : parameters_text.rfind(")")
    ]
    parameters = [
        param.strip()
        for param in parameters_text.split(",")
        if param.strip() and not param.strip().endswith("]")
    ]
    return parameters
