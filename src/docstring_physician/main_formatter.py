import difflib
import sys
from pathlib import Path

from src.docstring_physician.filters.docstrings_filters.docstrings_filter_pipeline import (
    DocstringFilterPipeline,
)
from src.docstring_physician.filters.docstrings_validators.docstring_validator_pipeline import (
    DocstringValidatorPipeline,
)
from src.docstring_physician.parsers.docstring_localizer.docstrings_localizer import (
    DocstringsLocalizer,
)


class Formatter:
    def __init__(
        self,
        validator_pipeline: DocstringValidatorPipeline,
        filter_pipeline: DocstringFilterPipeline,
        in_place: bool = True,
        print_diff: bool = True,
    ):
        self.validator_pipeline = validator_pipeline
        self.filter_pipeline = filter_pipeline
        self.in_place = in_place
        self.print_diff = print_diff

    def __call__(self, path: Path) -> bool:
        file_content = path.read_text().split("\n")

        # validators

        if not self.validator_pipeline.check(file_content):
            print("Docstrings are missing or incorrect in the file :(")
            sys.exit(1)

        # docstring filters

        formatted_file_content = file_content.copy()
        localizer = DocstringsLocalizer(formatted_file_content)
        start_index, end_index = localizer.find_next_docstring(0)

        while start_index != -1:
            docstring = formatted_file_content[start_index : end_index + 1]
            formatted_docstring = self.filter_pipeline.format(docstring)
            formatted_file_content[start_index : end_index + 1] = formatted_docstring
            start_index, end_index = DocstringsLocalizer(
                formatted_file_content
            ).find_next_docstring(start_index + len(formatted_docstring) + 1)

        if self.print_diff:
            print(f"printing diff for {path}")
            # create temporary file to see the differences
            differences = list(
                difflib.Differ().compare(file_content, formatted_file_content)
            )
            print("\n".join(differences))

        if self.in_place:
            path.write_text("\n".join(formatted_file_content))
