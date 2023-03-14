import difflib
import argparse
import sys
from pathlib import Path

from src.correct_docstrings.utils.formatting_conditions import (
    FormattingConditionValidator,
    ModuleDocstringFilter,
    PublicClassDocstringFilter,
    PublicFunctionDocstringFilter,
    PublicFunctionParameterDocstringFilter,
    PublicFunctionParameterMismatchFilter,
)
from utils.docstring_filters import DocstringFormatter
from utils.config import DocstringFormatterConfig, ensure_config_file_exists
from utils.script_filters import ScriptFormatter


CONFIG_PATH = Path(__file__).parent / "correct_docstrings_config.json"


class ScriptArguments(argparse.ArgumentParser):
    """
    Class for parsing arguments.
    """

    def __init__(self):
        super().__init__()
        self.add_argument("file_name", help="File name or directory name")
        self.add_argument("-v", "--verbose", help="Verbose mode", action="store_true")
        self.add_argument(
            "-c", "--check", help="Check if any changes are needed", action="store_true"
        )
        self.add_argument(
            "-d",
            "--diff",
            help="Only print diffs, without applying changes",
            action="store_true",
        )
        self.add_argument(
            "-i", "--ignore", help="Ignore files or directories", nargs="+"
        )


class Formatter:
    def __init__(
        self,
        validator: FormattingConditionValidator,
        script_formatter: ScriptFormatter,
        in_place: bool = True,
        print_diff: bool = True,
    ):
        self.validator = validator
        self.script_formatter = script_formatter
        self.in_place = in_place
        self.print_diff = print_diff

    def __call__(self, path: Path) -> bool:
        file_content = path.read_text().split("\n")

        if not self.validator.check(file_content):
            print("Docstrings are missing or incorrect in the file :(")
            sys.exit(1)

        formatted_file_content = self.script_formatter.format(file_content.copy())

        if self.print_diff:
            print(f"printing diff for {path}")
            # create temporary file to see the differences
            differences = list(
                difflib.Differ().compare(file_content, formatted_file_content)
            )
            print("\n".join(differences))

        if self.in_place:
            self.path.write_text("\n".join(self.result))


def main():
    """
    Main module for the script.
    """
    # check if config file exists
    ensure_config_file_exists(CONFIG_PATH)

    # parse args
    args = ScriptArguments().parse_args()

    if not args.file_name:
        print("Usage: python correct_docstrings.py <file_name | dir_name>")
        exit(-1)

    # check if file exists
    file_name = args.file_name
    path = Path(file_name)

    if not path.exists():
        print("Provided path is not valid!")
        exit(-1)

    files_to_check = []

    if path.is_file():
        files_to_check.append(path)

    if path.is_dir():
        files_to_check.extend(path.glob("**/*"))
        files_to_check = [
            path
            for path in files_to_check
            if path.is_file() and path.name.endswith(".py")
        ]

    validator = FormattingConditionValidator(
        [
            ModuleDocstringFilter,
            PublicClassDocstringFilter,
            PublicFunctionDocstringFilter,
            PublicFunctionParameterDocstringFilter,
            PublicFunctionParameterMismatchFilter,
        ]
    )

    config = DocstringFormatterConfig.from_json(CONFIG_PATH)
    docstrings_formatter = DocstringFormatter(config.filters)
    script_formatter = ScriptFormatter(docstrings_formatter)

    formatter = Formatter(validator, script_formatter)

    for path in files_to_check:
        formatter.format(path)

    print("Done.")


if __name__ == "__main__":
    main()
