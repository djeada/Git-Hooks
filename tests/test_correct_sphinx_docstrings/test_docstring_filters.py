from pathlib import Path

from src.correct_docstrings.utils.config import DocstringFormatterConfig, ScriptFormatterConfig, TypeHintFormatterConfig
from src.correct_docstrings.utils.docstring_filters import DocstringFormatter, ThirdPersonConverter, \
    EmptyLineBetweenDescriptionAndParams, RemoveUnwantedPrefixes, NoRepeatedWhitespaces, EndOfSentencePunctuation, \
    EnsureColonInParamDescription, IndentMultilineParamDescription


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
    formatter = EmptyLineBetweenDescriptionAndParams()

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
    formatter = EmptyLineBetweenDescriptionAndParams()

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
    formatter = EmptyLineBetweenDescriptionAndParams()

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
    formatter = RemoveUnwantedPrefixes()
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
        "    :param param1: Description of param1",
        "    :param param2: Multiline description ",
        "      of param2",
        "    :param param3: Description of param3",
        "    :return: Description of return value",
        '    """',
    ]
    formatter = NoRepeatedWhitespaces()
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
    expected = docstring
    converter = ThirdPersonConverter()
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
    converter = ThirdPersonConverter()
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
    converter = EndOfSentencePunctuation()
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
    converter = EnsureColonInParamDescription()
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
    converter = EnsureColonInParamDescription()
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
    converter = IndentMultilineParamDescription()
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
    converter = IndentMultilineParamDescription()
    result = converter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line


def test_docstring_formatter():

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
    formatter = DocstringFormatter()
    result = formatter.format(docstring)
    for expected_line, result_line in zip(result, expected):
        assert expected_line == result_line
