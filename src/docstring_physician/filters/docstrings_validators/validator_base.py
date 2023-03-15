from abc import ABC
from typing import Tuple


class DocstringValidatorBase(ABC):
    """
    Base class for formatting condition filters.
    """

    def check(self, content: Tuple[str], verbosity: bool = True) -> bool:
        """
        Checks the content.

        :param content: list of content in the docstring.
        :param verbosity:
        :return: True if everything is fine, else otherwise.
        """
        pass

    def __str__(self):
        return f"{self.__class__.__name__}"
