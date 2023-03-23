from typing import Type, Tuple

from src.docstring_physician.filters.docstrings_validators.validator_base import (
    DocstringValidatorBase,
)


class DocstringValidatorPipeline:
    """
    Gathers the formatting condition filters and applies them to the content
    when the check method is called.

    :param filters: list of formatting condition filters.
    """

    def __init__(self, validators: Tuple[DocstringValidatorBase]):
        self.validators = validators

    def clear(self):
        self.validators.clear()

    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
        """
        Applies the formatting condition filters to the content and returns True
        if everything passes, else False.

        :param content: list of content in the content.
        :param verbosity: verbosity flag.
        :return: True if everything passes, else False.
        """

        error_list = list()

        flag = True
        for validator in self.validators:
            if verbosity:
                print(f"Starting checks using {validator}...")
            if not validator.check(content, error_list, verbosity=verbosity):
                flag = False

        for error in sorted(error_list):
            print(error)

        return flag
