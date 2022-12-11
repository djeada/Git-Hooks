from pathlib import Path

from src.correct_docstrings.utils.config import DocstringFormatterConfig, ScriptFormatterConfig, TypeHintFormatterConfig
from src.correct_docstrings.utils.docstring_filters import DocstringFormatter, ThirdPersonConverter, \
    EmptyLineBetweenDescriptionAndParams, RemoveUnwantedPrefixes, NoRepeatedWhitespaces
from src.correct_docstrings.utils.helpers import ParametersExtractor, ParameterData
from src.correct_docstrings.utils.script_filters import ScriptFormatter, AddMissingDocstrings, PreserveParameterOrder, \
    DocstringsLocalizer
from src.correct_docstrings.utils.type_hints_filters import TypeHintsFormatter


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


def test_add_missing_docstring():
    file_content = """
    import os
    import sys

    def some_function(param_a: int, param_b: str = "default"):
        return param_a + param_b
    
    def some_other_function(
                            param_a, 
                            param_b, 
                            param_c
                            ):
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    """

    expected = '''
    import os
    import sys

    def some_function(param_a: int, param_b: str = "default"):
        """
        Description of function
        
        :param param_a:
        :param param_b:
        :return:
        """
        return param_a + param_b
    
    def some_other_function(
                            param_a, 
                            param_b, 
                            param_c
                            ):
        """
        Description of function
        
        :param param_a:
        :param param_b:
        :param param_c:
        :return:
        """
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    '''
    formatter = AddMissingDocstrings()
    content_as_list = formatter.format(file_content.split("\n"))

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()


def test_assert_optional_type_hints():
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
        return param_a + param_b + param_c
    
    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
     """

    expected = """
    import os
    import sys

    def some_function(param_a: int, param_b: Optional[str] = None):
        return param_a + param_b
    
    def some_other_function(
                            param_a: int, 
                            param_b: Optional[str] = None, 
                            param_c: Optional[int] = None
                            ):
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    """

    formatter = TypeHintsFormatter(TypeHintFormatterConfig(file_content))
    content_as_list = formatter.optional_type_hints()

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()


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
    formatter = PreserveParameterOrder()
    content_as_list = formatter.format(file_content.split("\n"))

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()


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
        



def test_script_formatter_config(tmpdir):
    file_content = '''
    import os
    import sys

    def some_function():
        """
        Description
        :param param1: description of param1
        :param param2: description of param2
          is multiline.
        :param param3: description of param 3
        :return: description of return value
        """
        return

    def some_other_function():
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

    expected = '''
    import os
    import sys

    def some_function():
        """
        Description

        :param param1: Description of param1
        :param param2: Description of param2
          is multiline.
        :param param3: Description of param 3
        :return: Description of return value
        """
        return

    def some_other_function():
        """
        Description

        :param param1: Description of param1
        :param param2: Description of param2
        :return: Description of return value
        """
        return

    if __name__ == '__main__':
        some_function()
        some_other_function()

    '''

    file_path = tmpdir.join("test.py")
    file_path.write(file_content)

    config = ScriptFormatterConfig(Path(file_path))
    ScriptFormatter(config)

    with open(file_path.strpath, "r") as f:
        result = f.read()

    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()
