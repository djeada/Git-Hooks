from pathlib import Path

from src.docstring_physician.filters.docstrings_filters.docstrings_filter_pipeline import (
    DocstringFilterPipeline,
)
from src.docstring_physician.filters.docstrings_filters.double_dot_filter import (
    DoubleDotFilter,
)
from src.docstring_physician.filters.docstrings_filters.line_wrapping_filter import (
    LineWrappingFilter,
)
from src.docstring_physician.filters.docstrings_filters.multiline_param_indent_filter import (
    MultilineParamIndentFilter,
)
from src.docstring_physician.filters.docstrings_filters.no_repeated_whitespaces_filter import (
    NoRepeatedWhitespacesFilter,
)
from src.docstring_physician.filters.docstrings_filters.param_description_format_filter import (
    ParamDescriptionFormatFilter,
)
from src.docstring_physician.filters.docstrings_filters.parameter_section_separator_filter import (
    ParameterSectionSeparatorFilter,
)
from src.docstring_physician.filters.docstrings_filters.prefix_stripper_filter import (
    PrefixStripperFilter,
)
from src.docstring_physician.filters.docstrings_filters.sentence_capitalization_filter import (
    SentenceCapitalizationFilter,
)
from src.docstring_physician.filters.docstrings_filters.sentence_punctuation_filter import (
    SentencePunctuationFilter,
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


def test_main_formatter(tmpdir):
    file_content = '''
    """
    This module contains a simple class and a main function to demonstrate its use.

    .. moduleauthor: Your Name <your.email@example.com>
    """

    class Rectangle:
        """
        A class representing a rectangle.

        :ivar length: The length of the rectangle.
        :ivar width: The width of the rectangle.
        """

        def __init__(self, length: float, width: float) -> None:
            """
            Initializes a new Rectangle instance.

            :param length: The length of the rectangle.
            :param width: The width of the rectangle.
              """
            self.length = length
            self.width = width

        def area(self) -> float:
            """
            Calculates the area of the rectangle.

            :return: The area of the rectangle.
            :rtype: float.
            """
            return self.length * self.width

    def main() -> None:
        """
        Creates a Rectangle instance, calculates its area, and prints the result.
        """
        rectangle = Rectangle(5, 10)
        area = rectangle.area()
        print(f"The area of the rectangle is {area}.")

    if __name__ == '__main__':
        main()
        '''.split(
        "\n"
    )

    expected = '''
    """
    This module contains a simple class and a main function to demonstrate its use.

    .. moduleauthor: Your Name <your.email@example.com>
    """

    class Rectangle:
        """
        A class representing a rectangle.

        :ivar length: The length of the rectangle.
        :ivar width: The width of the rectangle.
        """

        def __init__(self, length: float, width: float) -> None:
            """
            Initializes a new Rectangle instance.

            :param length: The length of the rectangle.
            :param width: The width of the rectangle.
              """
            self.length = length
            self.width = width

        def area(self) -> float:
            """
            Calculates the area of the rectangle.

            :return: The area of the rectangle.
            :rtype: float.
            """
            return self.length * self.width

    def main() -> None:
        """
        Creates a Rectangle instance, calculates its area, and prints the result.
        """
        rectangle = Rectangle(5, 10)
        area = rectangle.area()
        print(f"The area of the rectangle is {area}.")

    if __name__ == '__main__':
        main()
        '''.split(
        "\n"
    )
    file_path = Path(tmpdir.join("test.py"))
    file_path.write_text("\n".join(file_content))

    validators = [
        ModuleDocstringValidator(),
        PublicClassDocstringValidator(),
        PublicFunctionDocstringValidator(),
        PublicFunctionParameterMatchValidator(),
        PublicFunctionParameterPresenceValidator(),
    ]

    validator_pipeline = DocstringValidatorPipeline(validators)

    filters = [
        DoubleDotFilter(),
        LineWrappingFilter(),
        MultilineParamIndentFilter(),
        NoRepeatedWhitespacesFilter(),
        ParamDescriptionFormatFilter(),
        ParameterSectionSeparatorFilter(),
        PrefixStripperFilter(),
        SentencePunctuationFilter(),
        SentenceCapitalizationFilter(),
    ]

    filter_pipeline = DocstringFilterPipeline(filters)

    formatter = Formatter(validator_pipeline, filter_pipeline)
    formatter(file_path)

    result = file_path.read_text().split("\n")

    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()
