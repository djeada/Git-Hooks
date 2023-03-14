from typing import List, Tuple

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class SentenceCapitalizationFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each sentence starts
    with a capital letter.

    :param prefixes: prefixes of the lines that should be ignored.

    Example:
        :param _: some description
        :return: some description

    will be changed to:
        :param _: Some description
        :return: Some description
    """

    def __init__(self, prefixes: Tuple[str] = (":param", ":return", ":raises")):
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each sentence starts with a capital letter. If a sentence
        spans multiple lines, the first line of the sentence is the one that starts
        with a capital letter.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
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
                                + line_after_second_semicolon[0].upper()
                                + line_after_second_semicolon[1:]
                            )

                        docstring[i] = (
                            line[: index_of_second_semicolon + 1]
                            + line_after_second_semicolon
                        )

        return docstring
