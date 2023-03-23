from typing import Tuple, List

from src.docstring_physician.filters.docstrings_validators.error_data import ErrorData
from src.docstring_physician.filters.docstrings_validators.validator_base import (
    DocstringValidatorBase,
)


class PublicClassDocstringValidator(DocstringValidatorBase):
    def check(
        self,
        content: Tuple[str],
        error_list: List[ErrorData] = [],
        verbosity: bool = True,
    ) -> bool:
        """
        Checks if all public classes in the content parameter have docstrings
        immediately below their definition.

        :param content: Text of Python script.
        :param error_list: List of ErrorData objects to store any errors found.
        :param verbosity: Whether to display a message before returning False.
        :return: True if all public classes have docstrings, else False.
        """
        error_found = False

        for i, line in enumerate(content):
            if line.strip().startswith("class"):
                original_i = i + 1
                class_name = line.split()[1]
                if not class_name.startswith("_"):
                    # Class is public
                    next_line = i + 1
                    if next_line < len(content) and content[
                        next_line
                    ].strip().startswith('"""'):
                        # Public class has a docstring
                        continue
                    else:
                        # Public class is missing docstring
                        if verbosity:
                            message = (
                                f"The public class {class_name} is missing a docstring."
                            )
                            error_list.append(ErrorData(original_i, message))
                            error_found = True

        if error_found:
            if verbosity:
                print("Errors found while checking docstrings.")
            return False
        else:
            return True
