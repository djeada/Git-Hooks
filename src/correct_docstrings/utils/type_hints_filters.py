from typing import List

from src.correct_docstrings.utils.config import TypeHintFormatterConfig
from src.correct_docstrings.utils.helpers import ParameterData
from src.correct_docstrings.utils.script_filters import ParametersExtractor


class TypeHintsFormatter:
    """
    Responsible for formatting type hints.
    """

    def __init__(self, config: TypeHintFormatterConfig):
        self.content = config.content

    def optional_type_hints(self) -> List[str]:
        """
        Finds parameters with default value None and add Optional[type] to them.

        :return: list of lines in file
        """

        i = 0
        content = self.content.split("\n").copy()
        while i < len(content) - 1:
            line = content[i].strip()

            if line.startswith("def"):
                end_index = i
                while not line.endswith(":"):
                    end_index += 1
                    line = content[end_index].strip()

                extractor = ParametersExtractor(content)
                parameters = extractor.extract_parameters(i, end_index)

                # find the parameters with default value None
                # add Optional[type] to parameters with default value None
                for parameter in parameters:
                    if (
                        parameter.default_value == "None"
                        and not parameter.type_hint.startswith("Optional")
                    ):
                        parameter.type_hint = "Optional[" + parameter.type_hint + "]"

                # replace the parameters in the file

                content = extractor.replace_parameters(parameters, i, end_index)

            i += 1

        return content
