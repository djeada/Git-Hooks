import sys
from abc import ABC
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

from src.correct_docstrings.utils.config import (DocstringFormatterConfig,
                                                 ScriptFormatterConfig,
                                                 TypeHintFormatterConfig)
from src.correct_docstrings.utils.docstring_filters import DocstringFormatter
from src.correct_docstrings.utils.script_filters import extract_parameters


def main():
    # check if user provided file name
    if len(sys.argv) != 2:
        print("Usage: python correct_docstrings.py <dir_name>")
        exit()

    # check if file exists
    file_name = sys.argv[1]

    if not Path(file_name).is_dir():
        print("Dir does not exist")
        exit()

    # find all files in directory and make sure last line is empty
    for file in Path(file_name).glob("**/*"):
        if not file.is_file():
            continue
        config = ScriptFormatterConfig(file)
        ScriptFormatter(config)


if __name__ == "__main__":
    main()
