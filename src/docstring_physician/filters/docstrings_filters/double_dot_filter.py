from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class DoubleDotFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that there is an empty line
    above each line starting with double dots (..). If there are already more than
    one empty line above, they are removed to only have a single empty line above.
    Additionally, it adds a newline after a line within the section below ".."
    starting with a colon followed by a word.
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

        import re

        fixed_docstring = []
        dot_line_indention = -1
        dot_line_index = -1
        prev_line_was_empty = False
        colon_line = re.compile(r":\w+:")

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

                # Add newline after a line with :word: within the section below ".."
                if dot_line_indention != -1 and colon_line.search(line):
                    if i < len(docstring) - 1 and colon_line.search(docstring[i + 1]):
                        continue
                    fixed_docstring.append("")

        return fixed_docstring
