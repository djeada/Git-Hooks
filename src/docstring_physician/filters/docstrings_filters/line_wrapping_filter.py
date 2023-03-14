from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class LineWrappingFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for wrapping lines at a given maximum length.

    :param max_length: maximum length of each line.
    """

    def __init__(
        self,
        max_length: int = 120,
    ):
        self.max_length = max_length

    def format(self, docstring: List[str]) -> List[str]:
        """
        Wraps lines at a given maximum length.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """
        result = []
        for line in docstring:
            if len(line) > self.max_length:
                sublines = self._break_down_line(line, indent=self._get_indent(line))
                result.extend(sublines)
            else:
                result.append(line)
        return result

    def _break_down_line(self, line: str, indent: str) -> List[str]:
        """
        Recursively breaks down a line longer than max_length
        to smaller lines, until it is no longer than max_length.

        :param line: the line to be broken down.
        :param indent: the original indentation of the line.
        :return: a list of smaller lines.
        """
        if len(line) <= self.max_length:
            return [line]

        last_space_index = line.rfind(" ", 0, self.max_length)
        if last_space_index != -1:
            return [line[:last_space_index]] + self._break_down_line(
                indent + line[last_space_index + 1 :], indent=indent
            )

        return [line[: self.max_length]] + self._break_down_line(
            indent + line[self.max_length :], indent=indent
        )

    def _get_indent(self, line: str) -> str:
        """
        Gets the indentation of a line.

        :param line: the line to get the indentation of.
        :return: the indentation of the line.
        """
        return line[: len(line) - len(line.lstrip())]
