import string
from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class SentencePunctuationFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each sentence ends
    with a punctuation mark.

    :param punctuation: punctuation mark to be used.

    Example:
        :param _: some description
        :return: some description

    will be changed to:
        :param _: some description.
        :return: some description.
    """

    def __init__(self, punctuation: str = "."):
        self.punctuation = punctuation

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each sentence ends with a punctuation mark. If a sentence
        spans multiple lines, the last line of the sentence is the one that ends
        with a punctuation mark.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            line = line.strip()
            if not line:
                continue

            if line.endswith(self.punctuation):
                continue

            if not any(char.isalpha() for char in line):
                continue

            if line[-1] in string.punctuation:
                continue

            if i + 1 >= len(docstring):
                docstring[i] = docstring[i].rstrip() + self.punctuation
                continue

            j = i + 1
            next_line = docstring[j].strip()

            while not next_line and j < len(docstring):
                next_line = docstring[j].strip()
                j += 1

            if next_line.startswith(":") or j + 1 >= len(docstring):
                docstring[i] = docstring[i].rstrip() + self.punctuation

        return docstring
