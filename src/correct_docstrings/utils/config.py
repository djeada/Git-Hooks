"""
Classes responsible for storing configuration for the script formatter.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class DocstringFormatterConfig:
    """
    Configuration for the docstring formatter.
    """

    docstring: Tuple[str] = tuple()


@dataclass
class TypeHintFormatterConfig:
    """
    Configuration for the type hint formatter.
    """

    content: str = ""


@dataclass
class ScriptFormatterConfig:
    """
    Configuration for the script formatter.
    """

    path: Path
    print_diff: bool = False
    in_place: bool = True
    docstring_formatter_config: DocstringFormatterConfig = DocstringFormatterConfig()


class ScriptFormatterConfigFactory:
    @staticmethod
    def from_json(json_str: str) -> ScriptFormatterConfig:
        """
        Create a ScriptFormatterConfig from a JSON string.
        """
        pass

    @staticmethod
    def from_args(args: List[str]) -> ScriptFormatterConfig:
        """
        Create a ScriptFormatterConfig from command line arguments.
        """
        pass
