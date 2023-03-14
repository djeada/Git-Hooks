"""
Global filters, applied to the whole script (text file) as opposed to a single docstring.
"""
from abc import ABC, abstractmethod
from typing import List, Tuple

from .docstring_filters import DocstringFormatter
from .helpers import (
    DocstringsLocalizer,
    ParametersExtractor,
)



class PreserveParameterOrder(ScriptFilterBase):
    """
    Script filter that preserves the order of parameters in the docstring.
    """

    def format(self, content: List[str]) -> List[str]:
        """
        Sorts the parameters in the docstring to match the order of the parameters in the function.

        :param content: list of lines in the file.
        """
        localizer = DocstringsLocalizer(content)
        docstring_start_index, docstring_end_index = localizer.find_next_docstring(0)

        if docstring_start_index == -1:
            return content

        # find the index of first 'def' above start_index
        i = docstring_start_index - 1
        while i >= 0:
            line = content[i].strip()
            if line.startswith("def"):
                break
            i -= 1

        if i == -1:
            return content

        extractor = ParametersExtractor(content)
        extracted_parameters = extractor.extract_parameter_names(
            i, docstring_start_index
        )

        docstring = content[docstring_start_index : docstring_end_index + 1]
        parameters_to_descriptions = {}

        # find where paramers descriptions start and end
        param_description_start = -1
        param_description_end = -1

        i = 0
        while i < len(docstring):
            line = docstring[i].strip()
            if line.startswith(":param"):
                if param_description_start == -1:
                    param_description_start = i
                param_description_end = i
                while not docstring[param_description_end + 1].strip().startswith(":"):
                    param_description_end += 1
            i += 1

        if param_description_start == -1 or param_description_end == -1:
            return content

        for i, line in enumerate(docstring):
            if line.strip().startswith(":param"):
                start_index = i
                next_line = docstring[i + 1].strip() if i + 1 < len(docstring) else ""
                while next_line and not next_line.startswith(":"):
                    i += 1
                    next_line = (
                        docstring[i + 1].strip() if i + 1 < len(docstring) else ""
                    )
                end_index = i if next_line else i
                param_description = docstring[start_index : end_index + 1]
                param_name = param_description[0].split(":")[1].split(" ")[-1]
                parameters_to_descriptions[param_name] = param_description

        # order of parameters in docstring must match the order of parameters in parameters
        docstring[param_description_start : param_description_end + 1] = [
            "\n".join(parameters_to_descriptions[parameter])
            for parameter in extracted_parameters
        ]
        content[docstring_start_index : docstring_end_index + 1] = docstring

        return content


class ScriptFormatter:
    """
    Formats the script using selected script filters.

    :param initial_filters: list of script filters to be applied before formatting docstrings.
    """

    def __init__(
        self,
        docstring_formatter,
        initial_filters: List[ScriptFilterBase] = [],
    ):
        self.initial_filters = initial_filters
        self.docstring_formatter = docstring_formatter

    def format(self, content: List[str]) -> List[str]:
        """
        Formats the content.

        :param content: list of lines in the file.
        :return: formatted list of lines in the file.
        """

        for script_filter in self.initial_filters:
            content = script_filter.format(content)

        localizer = DocstringsLocalizer(content)
        start_index, end_index = localizer.find_next_docstring(0)

        while start_index != -1:
            docstring = content[start_index : end_index + 1]
            formatted_docstring = self.docstring_formatter.format(docstring)
            content[start_index : end_index + 1] = formatted_docstring
            start_index, end_index = DocstringsLocalizer(content).find_next_docstring(
                start_index + len(formatted_docstring) + 1
            )

        return content
