import argparse
from pathlib import Path
from src.docstring_physician.config.config import (
    MainFormatterConfig,
    ensure_config_file_exists,
)
from src.docstring_physician.filters.docstrings_filters.docstrings_filter_pipeline import (
    DocstringFilterPipeline,
)
from src.docstring_physician.filters.docstrings_validators.docstring_validator_pipeline import (
    DocstringValidatorPipeline,
)
from src.docstring_physician.filters.docstrings_validators.module_docstring_validator import (
    ModuleDocstringValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_class_docstring_validator import (
    PublicClassDocstringValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_function_docstring_validator import (
    PublicFunctionDocstringValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_function_parameter_match_validator import (
    PublicFunctionParameterMatchValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_function_parameter_presence_validator import (
    PublicFunctionParameterPresenceValidator,
)
from src.docstring_physician.main_formatter import Formatter

CONFIG_PATH = Path(__file__).parent / "correct_docstrings_config.json"


class CustomArgumentParser(argparse.ArgumentParser):
    """
    Command line argument parser for python scripts.

    :param file_name: Name of the file or directory to process.
    :param verbose: Enable verbose mode.
    :param check: Check if python script contains necessary docstrings with essential elements.
    :param format: Format the python script by correcting mistakes in docstrings.
    :param diff: Only print diffs, without applying changes.
    :param ignore: Ignore files or directories. Takes one or more arguments.
    """

    def __init__(self):
        super().__init__(description=self.__doc__)
        self.add_argument("file_name", help="Name of the file or directory to process")
        self.add_argument(
            "-v", "--verbose", help="Enable verbose mode", action="store_true"
        )
        self.add_argument(
            "-c",
            "--check",
            help="Check if python script contains necessary docstrings with essential elements",
            action="store_false",
        )
        self.add_argument(
            "-f",
            "--format",
            help="Format the python script by correcting mistakes in docstrings",
            action="store_false",
        )
        self.add_argument(
            "-d",
            "--diff",
            help="Only print diffs, without applying changes",
            action="store_true",
        )
        self.add_argument(
            "-i",
            "--ignore",
            help="Ignore files or directories. Takes one or more arguments",
            nargs="+",
        )


def main():
    """
    Main module for the script.
    """
    # check if config file exists
    ensure_config_file_exists(CONFIG_PATH)

    # parse args
    args = CustomArgumentParser().parse_args()

    if not args.file_name:
        print("Usage: python docstring_physician.py <file_name | dir_name>")
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

    config = MainFormatterConfig.from_json(CONFIG_PATH)

    validator_pipeline = DocstringValidatorPipeline(config.validators)
    filter_pipeline = DocstringFilterPipeline(config.filters)

    if not args.check:
        validator_pipeline.clear()

    if not args.format:
        filter_pipeline.clear()

    formatter = Formatter(validator_pipeline, filter_pipeline)

    for path in files_to_check:
        formatter(path)

    print("Done.")


if __name__ == "__main__":
    main()
