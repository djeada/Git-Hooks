from typing import Tuple

from src.docstring_physician.filters.docstrings_validators.validator_base import (
    ValidatorBase,
)


class PublicClassDocstringValidator(ValidatorBase):
    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
        """
        Checks if all public classes in the content parameter have docstrings
        immediately below their definition.

        :param content: Text of Python script.
        :param verbosity: Whether to display a message before returning False.
        :return: True if all public classes have docstrings, else False.
        """
        for i, line in enumerate(content):
            if line.strip().startswith("class"):
                original_i = i + 1
                class_name = line.split()[1]
                if not class_name.startswith("_"):
                    # Class is public
                    next_line = content.index(line) + 1
                    if next_line < len(content) and content[
                        next_line
                    ].strip().startswith('"""'):
                        # Public class has a docstring
                        continue
                    else:
                        # Public class is missing docstring
                        if verbosity:
                            print(
                                f"{original_i}: The public class {class_name} is missing a docstring."
                            )
                        return False
        return True
