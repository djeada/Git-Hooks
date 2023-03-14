from typing import List, Tuple

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class DocstringFilterPipeline:
    """
    Gathers the docstring filters and applies them to the docstring
    when the format method is called.

    :param docstring_filters: list of docstring filters.
    """

    def __init__(self, docstring_filters: Tuple[DocstringFilterBase]):
        self.filters = docstring_filters

    def format(self, docstring: List[str]) -> List[str]:
        """
        Formats the docstring using the specified filters.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for docstring_filter in self.filters:
            docstring = docstring_filter.format(docstring)

        return docstring
