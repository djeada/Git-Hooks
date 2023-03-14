from typing import Tuple, List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class ParameterSectionSeparatorFilter(DocstringFilterBase):
    """
    Docstring filter that makes sure that there is an empty line between description and params.

    :param prefixes: list of prefixes that indicate a docstring keyword.

    Example:
        Description of the function.
        :param _: some description
        :return: some description

    will be changed to:
        Description of the function.

        :param _: some description
        :return: some description
    """

    def __init__(self, prefixes: Tuple[str] = (":param", ":return", ":raises")):
        """
        :param prefixes: list of prefixes that indicate the start of the param list.
        """
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that there is an empty line between description and params.

        :param docstring: list of lines in docstring
        :return: list of lines in docstring
        """
        start_of_param_list = -1
        docstring = docstring.copy()

        for i, line in enumerate(docstring):
            line = line.strip()
            # check if it starts with prefix
            for prefix in self.prefixes:
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
