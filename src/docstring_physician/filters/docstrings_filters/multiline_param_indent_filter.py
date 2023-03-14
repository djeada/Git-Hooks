from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class MultilineParamIndentFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for indenting multiline parameter descriptions.
    :param indentation: indentation to be used.
    Example:
        :param _: some description
        that spans multiple lines
        :return: some description
    will be changed to:
        :param _: some description
          that spans multiple lines
        :return: some description
    """

    def __init__(self, indentation: str = " " * 2):
        self.indentation = indentation

    def format(self, docstring: List[str]) -> List[str]:
        """
        Indents multiline parameter descriptions.
        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            if not line:
                continue

            next_line = docstring[i + 1] if i + 1 < len(docstring) else None
            if not next_line:
                continue

            j = 0
            while line.strip().startswith(":param") and not (
                next_line.strip().startswith(":") or next_line.strip() == ""
            ):
                j += 1
                next_line = docstring[i + j] if i + j < len(docstring) else None

                if not next_line or next_line.strip().startswith(":"):
                    j -= 1
                    break

            default_indentation = " " * (len(line) - len(line.lstrip()))
            for k in range(j):
                index = i + k + 1
                if index >= len(docstring):
                    break
                if docstring[index].strip().startswith('"""'):
                    break
                docstring[index] = (
                    default_indentation + self.indentation + docstring[index].lstrip()
                )

        return docstring
