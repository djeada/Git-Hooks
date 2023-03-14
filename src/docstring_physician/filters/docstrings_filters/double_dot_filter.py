from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class DoubleDotFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that there is an empty line
    above each line starting with double dots (..). If there are already more than
    one empty line above, they are removed to only have a single empty line above.
    """

    def __init__(self):
        super().__init__()

    def format(self, docstring: List[str]) -> List[str]:
        """
        Formats the docstring to ensure that there is an empty line above each line
        starting with double dots (..). If there are already more than one empty line
        above, they are removed to only have a single empty line above.

        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        fixed_docstring = []
        dot_line_indention = -1
        dot_line_index = -1
        prev_line_was_empty = False
        for i, line in enumerate(docstring):
            stripped_line = line.strip()
            current_indention = len(line) - len(line.lstrip())
            if stripped_line in ["", '"""'] and dot_line_indention != -1:
                dot_line_indention = -1
            if (
                current_indention <= dot_line_indention
                and dot_line_indention != -1
                and i != dot_line_index
            ):
                fixed_docstring.append("")
                dot_line_indention = -1
            if stripped_line.startswith(".."):
                if not prev_line_was_empty:
                    fixed_docstring.append("")
                fixed_docstring.append(line)
                prev_line_was_empty = False
                dot_line_indention = len(line) - len(line.lstrip())
                dot_line_index = i

            elif stripped_line == "":
                if not prev_line_was_empty:
                    fixed_docstring.append(line)
                prev_line_was_empty = True
            else:
                fixed_docstring.append(line)
                prev_line_was_empty = False

        return fixed_docstring
