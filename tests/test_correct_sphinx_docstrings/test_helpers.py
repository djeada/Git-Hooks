from pathlib import Path

from src.correct_docstrings.utils.config import DocstringFormatterConfig, ScriptFormatterConfig, TypeHintFormatterConfig
from src.correct_docstrings.utils.docstring_filters import DocstringFormatter, ThirdPersonConverter, \
    EmptyLineBetweenDescriptionAndParams, RemoveUnwantedPrefixes, NoRepeatedWhitespaces
from src.correct_docstrings.utils.helpers import ParametersExtractor, ParameterData
from src.correct_docstrings.utils.script_filters import ScriptFormatter, AddMissingDocstrings, PreserveParameterOrder, \
    DocstringsLocalizer
from src.correct_docstrings.utils.type_hints_filters import TypeHintsFormatter


def test_find_next_docstring():
    file_content = '''
    import os
    import sys

    def some_function():
        """
        Description
        :param param1: description of param1
        :param param2: multiline description
          of param2
        :param param3: description of param3
        :return: description of return value
        """
        return

    def some_other_function(
            param1: int = object(),
            param2: float = 1.52,
        ):
        """
        Description
        :param param1:      description of param1
     .  :param param2: description of param2
        :return: description of return value
        """
        return

    if __name__ == '__main__':
        some_function()
        some_other_function()

    '''
    localizer = DocstringsLocalizer(file_content.split("\n"))

    expected = (5, 12)
    result = localizer.find_next_docstring(0)
    assert result == expected

    expected = (19, 24)
    result = localizer.find_next_docstring(13)
    assert result == expected

def test_parameter_extractor():
    # all parameters in a single line

    function_in_code = """
    def some_function(param_a: int, param_b: str = None):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"    
        return param_a + param_b
    """.split("\n")

    extractor = ParametersExtractor(function_in_code)
    parameters = extractor.extract_parameters()

    expected = [ParameterData("param_a", "int"), ParameterData("param_b", "str")]

    # compare elem by elem
    for param, expected_param in zip(parameters, expected):
        assert param.name == expected_param.name
        assert param.type_hint == expected_param.type_hint

    # parameters in multiple lines

    function_in_code = """
    def some_other_function(
                            param_a: int,
                            param_b: str = None,
                            param_c: int = None
                            ):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b + param_c

    """.split("\n")

    extractor = ParametersExtractor(function_in_code)
    parameters = extractor.extract_parameters()

    expected = [
        ParameterData("param_a", "int"),
        ParameterData("param_b", "str"),
        ParameterData("param_c", "int"),
    ]

    # compare elem by elem
    for param, expected_param in zip(parameters, expected):
        assert param.name == expected_param.name
        assert param.type_hint == expected_param.type_hint

    # multiple functions in text, should return only the first one

    function_in_code = """
    def some_other_function(
                            param_a: int,
                            param_b: str = None,
                            param_c: int = None

                            ):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b + param_c

    def some_other_function2(
                            param_a: int,
                            param_b: str = None,
                            param_c: int = None
                            ):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b + param_c

    """.split("\n")

    extractor = ParametersExtractor(function_in_code)
    parameters = extractor.extract_parameters()

    expected = [
        ParameterData("param_a", "int"),
        ParameterData("param_b", "str"),
        ParameterData("param_c", "int"),
    ]

    # compare elem by elem
    for param, expected_param in zip(parameters, expected):
        assert param.name == expected_param.name
        assert param.type_hint == expected_param.type_hint


def test_replace_parameters():
    # single line
    file_content = """
    def some_function(param_a: int, param_b: str = None):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b
    """.split("\n")

    expected = """
    def some_function(param_1: int, param_2: str = "default"):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b
    """.split("\n")

    new_parameters = [ParameterData("param_1", "int"), ParameterData("param_2", "str", '"default"')]
    formatter = ParametersExtractor(file_content)

    result = formatter.replace_parameters(new_parameters)

    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()

    # multiple lines
    file_content = """
    def some_other_function(
                            param_a: int,
                            param_b: str = None,
                            param_c: int = None
                            ):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b + param_c
    """.split("\n")

    expected = """
    def some_other_function(
                            param_1: int,
                            param_2: str = "default",
                            param_3: int = 1
                            ):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b + param_c
    """.split("\n")

    new_parameters = [
        ParameterData("param_1", "int"),
        ParameterData("param_2", "str", '"default"'),
        ParameterData("param_3", "int", "1"),
    ]

    formatter = ParametersExtractor(file_content)

    result = formatter.replace_parameters(new_parameters)

    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()
