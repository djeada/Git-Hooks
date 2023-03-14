from typing import Tuple

from src.docstring_physician.filters.docstrings_validators.validator_base import (
    ValidatorBase,
)


class ModuleDocstringValidator(ValidatorBase):
    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
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
