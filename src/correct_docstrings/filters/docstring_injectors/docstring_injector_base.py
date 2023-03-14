from abc import ABC, abstractmethod
from typing import List, Tuple

class ScriptFilterBase(ABC):
    """
    Base class for script filters.
    """

    @abstractmethod
    def format(self, content: List[str]) -> List[str]:
        """
        Formats the content.

        :param content: list of lines in the file.
        :return: formatted list of lines in the file.
        """
        pass


class AddMissingDocstrings(ScriptFilterBase):
    """
    Script filter that adds missing docstrings to the script.
    """

    def __init__(self):
        self.ignored_parameters = ["self", "cls"]

    def format(self, content: List[str]) -> List[str]:
        """
        Adds docstring to file.

        :return: list of lines in file
        """
        internal_filters = [
            self.add_docstrings_to_module,
            self.add_docstrings_to_functions,
            self.add_docstrings_to_classes,
        ]

        for internal_filter in internal_filters:
            content = internal_filter(content)

        return content

    def add_docstrings_to_module(self, content: List[str]) -> List[str]:
        """
        Adds docstring to module.

        :param content: list of lines in the file.
        :return: formatted list of lines in file
        """
        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

        # check if there is module docstring at the beginning of the file
        if content[0].strip() not in possible_docstring_start:
            content.insert(0, '"""')
            # content.insert(1, 'Description of the module is missing...')
            content.insert(1, '"""')

        # check if next line is empty if not add empty line
        if content[2].strip() != "":
            content.insert(2, "")

        return content

    def add_docstrings_to_functions(self, content: List[str]) -> List[str]:
        """
        Adds docstring to functions.

        :param content: list of lines in the file.
        :return: formatted list of lines in file
        """
        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

        i = 0
        while i < len(content) - 1:
            line = content[i].strip()
            indentation = len(content[i]) - len(content[i].lstrip()) + 4
            if line.startswith("def"):
                # if function name starts with __ it is a private function and we don't need to add docstring
                if line.split("def")[1].strip().startswith("__"):
                    i += 1
                    continue

                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                if content[end_index + 1].strip() not in possible_docstring_start:
                    # find the parameters of the function between ()

                    extractor = ParametersExtractor(content)
                    parameters = extractor.extract_parameter_names(i, end_index)

                    # add docstring
                    content.insert(end_index + 1, f'{" " * indentation}"""')
                    content.insert(
                        end_index + 2, f'{" " * indentation}Description of function'
                    )
                    content.insert(end_index + 3, "")
                    # add parameters
                    end_index += 4
                    for parameter in parameters:
                        if parameter in self.ignored_parameters:
                            continue
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

    def add_docstrings_to_classes(self, content: List[str]) -> List[str]:
        """
        Adds docstring to classes.

        :param content: list of lines in the file.
        :return: formatted list of lines in file
        """
        possible_docstring_start = ['"""', "'''", 'r"""', "r'''"]

        i = 0
        while i < len(content) - 1:
            line = content[i].strip()
            indentation = len(content[i]) - len(content[i].lstrip()) + 4
            if line.startswith("class"):
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                if content[end_index + 1].strip() not in possible_docstring_start:
                    # find the parameters of the function between ()

                    extractor = ParametersExtractor(content)
                    parameters = extractor.extract_parameter_names(i, end_index)

                    # add docstring
                    content.insert(end_index + 1, f'{" " * indentation}"""')
                    content.insert(
                        end_index + 2, f'{" " * indentation}Description of class'
                    )
                    content.insert(end_index + 3, "")
                    end_index += 4
                    # add parameters from __init__ method
                    j = i + 1
                    parameters = None
                    while j < len(content) - 1:
                        if content[j].strip().startswith("class"):
                            break
                        if "def __init__" in content[j]:
                            k = j
                            while "):" not in content[k] and ") ->" not in content[k]:
                                k += 1
                                if k >= len(content):
                                    break
                            parameters = extractor.extract_parameter_names(j, k)
                            break
                        j += 1

                    if parameters is not None:
                        for parameter in parameters:
                            if parameter in self.ignored_parameters:
                                continue
                            parameter = parameter.split(":")[0]
                            content.insert(
                                end_index,
                                f'{" " * indentation}:param {parameter.strip()}:',
                            )
                            end_index += 1

                    content.insert(end_index, f'{" " * indentation}"""')

            i += 1

        return content
