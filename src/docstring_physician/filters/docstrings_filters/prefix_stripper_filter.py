from typing import Tuple, List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class PrefixStripperFilter(DocstringFilterBase):
    """
    Docstring filter that removes unwanted prefixes from the docstring.

    :param prefixes: list of prefixes that indicate a docstring keyword.

    Example:
     .. :param _: some description
        ,:return: some description

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
        Removes unwanted prefixes from the docstring.

        :param docstring: list of lines in docstring
        :return: list of lines in docstring
        """
        for i, line in enumerate(docstring):
            # check if one prefixes is in line
            for prefix in self.prefixes:
                index = line.find(prefix)
                if index != -1:
                    # make sure there is only whitespace before prefix
                    # replace all characters before prefix with whitespace
                    docstring[i] = " " * index + line[index:]
                    break

        return docstring
