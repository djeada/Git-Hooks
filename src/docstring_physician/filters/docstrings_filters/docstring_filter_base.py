from abc import ABC, abstractmethod
from typing import Tuple


class DocstringFilterBase(ABC):
    """
    Base class for docstring filters.
    """

    @abstractmethod
    def format(self, content: Tuple[str]) -> Tuple[str]:
        """
        Formats the content.

        :param content: list of lines in the docstring.
        :return: formatted list of lines in the docstring.
        """
        pass
