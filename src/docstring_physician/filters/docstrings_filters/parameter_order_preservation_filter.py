from typing import List

from src.docstring_physician.filters.docstrings_filters.docstring_filter_base import (
    DocstringFilterBase,
)
from src.docstring_physician.parsers.docstring_localizer.docstrings_localizer import (
    DocstringsLocalizer,
)
from src.docstring_physician.parsers.param_parser.param_parser import (
    ParametersExtractor,
)


class EnforceParameterOrderFilter(DocstringFilterBase):
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
