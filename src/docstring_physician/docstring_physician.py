import argparse
from pathlib import Path
from src.docstring_physician.config.config import (
    DocstringFormatterConfig,
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


def main():
    """
    Main module for the script.
    """
    # check if config file exists
    ensure_config_file_exists(CONFIG_PATH)

    # parse args
    args = ScriptArguments().parse_args()

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

    validators = [
        ModuleDocstringValidator(),
        PublicClassDocstringValidator(),
        PublicFunctionDocstringValidator(),
        PublicFunctionParameterMatchValidator(),
        PublicFunctionParameterPresenceValidator(),
    ]

    validator_pipeline = DocstringValidatorPipeline(validators)

    config = DocstringFormatterConfig.from_json(CONFIG_PATH)
    filter_pipeline = DocstringFilterPipeline(config.filters)

    formatter = Formatter(validator_pipeline, filter_pipeline)

    for path in files_to_check:
        formatter(path)

    print("Done.")


if __name__ == "__main__":
    main()
