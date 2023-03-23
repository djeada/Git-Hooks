from typing import Tuple, List

from src.docstring_physician.filters.docstrings_validators.error_data import ErrorData
from src.docstring_physician.filters.docstrings_validators.validator_base import (
    DocstringValidatorBase,
)


class ModuleDocstringValidator(DocstringValidatorBase):
    def check(
        self,
        content: Tuple[str],
        error_list: List[ErrorData] = [],
        verbosity: bool = True,
    ) -> bool:
        """
        Checks if the first non-empty line of the content parameter
        is a module docstring that starts with either \"\"\" or '''.

        :param content: Text of Python script.
        :param verbosity: Whether to display a message before returning False.
        :return: True if module docstring is present, else False.
        """
        for line in content:
            if line.strip() != "":
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    return True
                else:
                    if verbosity:
                        print("Module docstring is missing or improperly formatted.")
                    return False
        if verbosity:
            print("Module docstring is missing.")
        return False
