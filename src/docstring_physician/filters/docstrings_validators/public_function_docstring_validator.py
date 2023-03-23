import re
from typing import Tuple, List

from src.docstring_physician.filters.docstrings_validators.error_data import ErrorData
from src.docstring_physician.filters.docstrings_validators.validator_base import (
    DocstringValidatorBase,
)


class PublicFunctionDocstringValidator(DocstringValidatorBase):
    def check(
        self,
        content: Tuple[str],
        error_list: List[ErrorData] = [],
        verbosity: bool = True,
    ) -> bool:
        """
        Checks if all public functions in the content parameter have docstrings
        immediately below their definition.

        :param content: Text of Python script.
        :param error_list: List of ErrorData objects to store any errors found.
        :param verbosity: Whether to display appropriate message before returning False (default=True).
        :return: True if all public functions have docstrings, else False.
        """

        def is_function_definition(line):
            return line.strip().startswith("def ")

        def get_function_name(line):
            return line.split()[1].split("(")[0]

        error_found = False

        for i, line in enumerate(content):
            if is_function_definition(line):
                original_i = i + 1
                # Check if function definition spans multiple lines

                # Get function name
                func_name = get_function_name(line)

                # Check if function is public
                if func_name.startswith("_") or (
                    i - 1 >= 0 and re.findall(r"@\w+\.(setter|deleter)", content[i - 1])
                ):
                    continue

                while not line.strip().endswith(":"):
                    i += 1
                    line = content[i]

                # Function is public
                next_line = i + 1
                if next_line < len(content) and content[next_line].strip().startswith(
                    '"""'
                ):
                    # Public function has a docstring
                    continue
                else:
                    # Public function is missing docstring
                    if verbosity:
                        message = f"Function {func_name} is missing a docstring."
                        error_list.append(ErrorData(original_i, message))
                        error_found = True

        if error_found:
            if verbosity:
                print("Errors found while checking docstrings.")
            return False
        else:
            return True
