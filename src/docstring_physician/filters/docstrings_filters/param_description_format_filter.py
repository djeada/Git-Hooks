from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)


class ParamDescriptionFormatFilter(DocstringFilterBase):
    """
    Docstring filter that is responsible for ensuring that each parameter description
    starts with ':param <param_name>:'.

    Example:
        :param _ some description
        :return: some description

    will be changed to:
        :param _: some description
        :return: some description
    """

    def __init__(self, prefixes=[":param", ":return", ":raises"]):
        self.prefixes = prefixes

    def format(self, docstring: List[str]) -> List[str]:
        """
        Makes sure that each parameter description starts with ':param <param_name>:'.
        :param docstring: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """

        for i, line in enumerate(docstring):
            if not line:
                continue

            if line.strip().startswith(":param") and (
                line.count(":") == 1 or len(line.strip().split(":")[1].split(" ")) != 2
            ):
                j = line.index(":")
                # find the second word in the line after j and add a colon after it
                j += line[j + 1 :].index(" ") + 1
                j += line[j + 1 :].index(" ") + 1
                docstring[i] = line[:j] + line[j:].replace(" ", ": ", 1)

            for prefix in self.prefixes:
                if docstring[i].strip().startswith(prefix):
                    while "::" in docstring[i]:
                        docstring[i] = docstring[i].replace("::", ":")

        return docstring
