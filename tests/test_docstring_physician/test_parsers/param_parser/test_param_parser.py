from src.docstring_physician.parsers.param_parser.data import ParameterData
from src.docstring_physician.parsers.param_parser.param_parser import (
    ParametersExtractor,
)


def test_parameter_extractor():
    # all parameters in a single line

    function_in_code = """
    def some_function(param_a: int, param_b: str = None):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"    
        return param_a + param_b
    """.split(
        "\n"
    )

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

    """.split(
        "\n"
    )

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

    """.split(
        "\n"
    )

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
    """.split(
        "\n"
    )

    expected = """
    def some_function(param_1: int, param_2: str = "default"):
        \"\"\"
        Docstrings shouldn't be touched.
        \"\"\"
        return param_a + param_b
    """.split(
        "\n"
    )

    new_parameters = [
        ParameterData("param_1", "int"),
        ParameterData("param_2", "str", '"default"'),
    ]
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
    """.split(
        "\n"
    )

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
    """.split(
        "\n"
    )

    new_parameters = [
        ParameterData("param_1", "int"),
        ParameterData("param_2", "str", '"default"'),
        ParameterData("param_3", "int", "1"),
    ]

    formatter = ParametersExtractor(file_content)

    result = formatter.replace_parameters(new_parameters)

    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()
