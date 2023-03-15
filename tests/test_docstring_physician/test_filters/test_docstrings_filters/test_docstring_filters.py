from src.docstring_physician.config.config import MainFormatterConfig
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
from src.docstring_physician.filters.docstrings_filters.parameter_order_preservation_filter import (
    EnforceParameterOrderFilter,
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
from src.docstring_physician.filters.docstrings_filters.third_person_filter import (
    ThirdPersonFilter,
)


def test_assert_empty_line_between_description_and_param_list():
    # correct docstring: function shouldn't change anything
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    expected = docstring
    formatter = ParameterSectionSeparatorFilter()

    result = formatter.format(docstring)
    assert result == expected

    # missing empty line between description and param list
    docstring = [
        '   """',
        "    Description",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    formatter = ParameterSectionSeparatorFilter()

    result = formatter.format(docstring)
    assert result == expected

    # multiple empty lines between description and param list
    docstring = [
        '   """',
        "    Description",
        "",
        "",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    formatter = ParameterSectionSeparatorFilter()

    result = formatter.format(docstring)
    assert result == expected

    # no params in docstring
    docstring = [
        '"""',
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        '"""',
    ]
    expected = [
        '"""',
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        '"""',
    ]
    formatter = ParameterSectionSeparatorFilter()

    result = formatter.format(docstring)
    assert result == expected


def test_assert_no_unnecessary_prefixes():
    docstring = [
        '   """',
        "    Description",
        "",
        " ., :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    formatter = PrefixStripperFilter()
    result = formatter.format(docstring)
    assert result == expected


def test_assert_single_whitespace_after_second_semicolon():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1:   description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    formatter = NoRepeatedWhitespacesFilter()
    result = formatter.format(docstring)
    assert result == expected


def test_assert_line_wrapping():
    docstring = [
        '   """',
        "    This function takes in a dataset of customer information and generates a report that summarizes key metrics and insights about the data. The report includes information about customer demographics, purchasing behavior, and overall satisfaction with the company's products and services.",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2 that is too long to fit on one line and should be wrapped",
        "    :param param3: description of param3",
        "    :return: description of return value that is also too long to fit on one line and should be wrapped",
        '    """',
    ]
    expected = [
        '   """',
        "    This function takes in a dataset of customer",
        "    information and generates a report that summarizes key",
        "    metrics and insights about the data. The report",
        "    includes information about customer demographics,",
        "    purchasing behavior, and overall satisfaction with the",
        "    company's products and services.",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2 that is too long",
        "    to fit on one line and should be wrapped",
        "    :param param3: description of param3",
        "    :return: description of return value that is also too",
        "    long to fit on one line and should be wrapped",
        '    """',
    ]
    formatter = LineWrappingFilter(max_length=60)
    result = formatter.format(docstring)
    assert result == expected


def test_convert_to_third_person():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]

    config = MainFormatterConfig()
    converter = ThirdPersonFilter(
        config.docstring_filters_config.third_person_config.blocking_words,
        config.docstring_filters_config.third_person_config.modals,
        config.docstring_filters_config.third_person_config.verbs,
    )

    expected = docstring
    result = converter.format(docstring)
    assert result == expected

    docstring = [
        '   """',
        "    use unlimited option of giving a better life.",
        "   Can do some more specific calculations",
        "",
        "    :param param1: can do many things",
        "    :param param2: is usually employed for taxes",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    uses unlimited option of giving a better life.",
        "   Can do some more specific calculations",
        "",
        "    :param param1: can do many things",
        "    :param param2: is usually employed for taxes",
        "    :return: description of return value",
        '    """',
    ]
    config = MainFormatterConfig()
    converter = ThirdPersonFilter(
        config.docstring_filters_config.third_person_config.blocking_words,
        config.docstring_filters_config.third_person_config.modals,
        config.docstring_filters_config.third_person_config.verbs,
    )

    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_end_of_sentence_punctuation():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1?",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3.",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description.",
        "",
        "    :param param1: description of param1?",
        "    :param param2: multiline description ",
        "      of param2.",
        "    :param param3: description of param3.",
        "    :return: description of return value.",
        '    """',
    ]
    converter = SentencePunctuationFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_ensure_colon_in_param_description():
    # everything fine

    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    converter = ParamDescriptionFormatFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    # missing colon
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1 description of param1",
        "    :param param2 multiline: description ",
        "      of param2",
        "    :param param3::: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline: description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    converter = ParamDescriptionFormatFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_indent_multiline_param_description():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    converter = MultilineParamIndentFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "   of param2",
        "    :param param3: description of param3 ",
        "    spanning 1",
        "    spanning 2",
        "    spanning 3 lines!!!",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3 ",
        "      spanning 1",
        "      spanning 2",
        "      spanning 3 lines!!!",
        "    :return: description of return value",
        '    """',
    ]
    converter = MultilineParamIndentFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        '    """',
    ]
    converter = MultilineParamIndentFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line

    docstring = [
        '   """',
        "        Create an instance.",
        "",
        "    :param reflection_plane: Reflection plane defined by :class:`ReflectionPlane`",
        "      enum.",
        '    """',
    ]

    expected = [
        '   """',
        "        Create an instance.",
        "",
        "    :param reflection_plane: Reflection plane defined by :class:`ReflectionPlane`",
        "      enum.",
        '    """',
    ]
    converter = MultilineParamIndentFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_double_dot_filter():
    docstring = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "    .. note::",
        "        Some note",
        "        Some note",
        "    Some more text",
        "",
        "    :return: Return value",
        '"""',
    ]
    expected = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "",
        "    .. note::",
        "        Some note",
        "        Some note",
        "",
        "    Some more text",
        "",
        "    :return: Return value",
        '"""',
    ]
    filter_ = DoubleDotFilter()
    result = filter_.format(docstring)
    assert result == expected

    docstring = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "    .. note::",
        "        Some note",
        "        Some note",
        "",
        "    :return: Return value",
        '"""',
    ]
    expected = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "",
        "    .. note::",
        "        Some note",
        "        Some note",
        "",
        "    :return: Return value",
        '"""',
    ]
    filter_ = DoubleDotFilter()
    result = filter_.format(docstring)
    assert result == expected

    docstring = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "    .. note::",
        "        Some note",
        "        Some note",
        '"""',
    ]
    expected = [
        '"""',
        "    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "",
        "    .. note::",
        "        Some note",
        "        Some note",
        '"""',
    ]
    filter_ = DoubleDotFilter()
    result = filter_.format(docstring)
    assert result == expected


def test_preserve_parameter_order():
    file_content = """
    import os
    import sys

    def some_function(param_a: int, param_b: str = None):
        return param_a + param_b

    def some_other_function(
                            param_a: int, 
                            param_b: str = None, 
                            param_c: int = None
                            ):
        \"\"\"
        Description

        :param param_c: description c
        :param param_a: description a spanning across
          multiple lines.
        :param param_b: description b
        :return:
        \"\"\"
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
     """

    expected = """
    import os
    import sys

    def some_function(param_a: int, param_b: str = None):
        return param_a + param_b

    def some_other_function(
                            param_a: int, 
                            param_b: str = None, 
                            param_c: int = None
                            ):
        \"\"\"
        Description

        :param param_a: description a spanning across
          multiple lines.
        :param param_b: description b
        :param param_c: description c
        :return:
        \"\"\"
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    """
    formatter = EnforceParameterOrderFilter()
    content_as_list = formatter.format(file_content.split("\n"))

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()


def test_sentence_capitalization():
    docstring = [
        '   """',
        "    Description.",
        "",
        "    :param param1: description of param1.",
        "    :param param2: multiline description ",
        "      of param2.",
        "    :param param3: Description of param3.",
        "    :return: description of return value.",
        '    """',
    ]
    expected = [
        '   """',
        "    Description.",
        "",
        "    :param param1: Description of param1.",
        "    :param param2: Multiline description ",
        "      of param2.",
        "    :param param3: Description of param3.",
        "    :return: Description of return value.",
        '    """',
    ]
    converter = SentenceCapitalizationFilter()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_docstring_filter_pipeline():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1: description of param1",
        "    :param param2: multiline description ",
        "      of param2",
        "    :param param3: description of param3",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description.",
        "",
        "    :param param1: Description of param1.",
        "    :param param2: Multiline description ",
        "      of param2.",
        "    :param param3: Description of param3.",
        "    :return: Description of return value.",
        '    """',
    ]
    docstring_filters = [
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
    pipeline = DocstringFilterPipeline(docstring_filters)
    result = pipeline.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line
