from typing import Tuple, List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class NoRepeatedWhitespacesFilter(DocstringFilterBase):
    """
    Docstring filter that removes repeated whitespaces from the docstring.

    :param prefixes: list of prefixes that indicate a docstring keyword.

    Example:
        :param _:     some description
        :return: some description

    will be changed to:
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
        Removes repeated whitespaces from the docstring.

        :param docstring: list of lines in docstring
        :return: list of lines in docstring
        """
        for i, line in enumerate(docstring):
            for prefix in self.prefixes:
                index = line.find(prefix)
                if index != -1:
                    index_of_second_semicolon = line.find(":", index + len(prefix))
                    if index_of_second_semicolon != -1:
                        line_after_second_semicolon = line[
                            index_of_second_semicolon + 1 :
                        ]

                        while line_after_second_semicolon.startswith(" "):
                            line_after_second_semicolon = line_after_second_semicolon[
                                1:
                            ]

                        if len(line_after_second_semicolon) > 1:
                            line_after_second_semicolon = (
                                " "
                                + line_after_second_semicolon[0]
                                + line_after_second_semicolon[1:]
                            )

                        docstring[i] = (
                            line[: index_of_second_semicolon + 1]
                            + line_after_second_semicolon
                        )

        return docstring
