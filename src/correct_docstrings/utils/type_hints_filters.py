from typing import List

from src.correct_docstrings.utils.config import TypeHintFormatterConfig
from src.correct_docstrings.utils.script_filters import extract_parameters


class TypeHintsFormatter:
    def __init__(self, config: TypeHintFormatterConfig):
        self.content = config.content

    def optional_type_hints(self) -> List[str]:
        """
        Find parameters with default value None and add Optional[type] to them.

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

                parameters = extract_parameters(content, i, end_index)

                # find the parameters with default value None
                parameters_with_default_value_none = [
                    parameter for parameter in parameters if "= None" in parameter
                ]
                # add Optional[type] to parameters with default value None
                for parameter in parameters_with_default_value_none:
                    parameter_name = parameter.split(":")[0].strip()
                    parameter_type = parameter.split(":")[1].strip()
                    parameter_type = parameter_type.replace("= None", "").rstrip()
                    for j in range(i, end_index + 1):
                        content[j] = content[j].replace(
                            parameter,
                            f"{parameter_name}: Optional[{parameter_type}] = None",
                        )

            i += 1

        return content
