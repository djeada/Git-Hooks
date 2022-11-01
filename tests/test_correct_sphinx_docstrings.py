from pathlib import Path

from src.correct_docstrings import (
    ScriptFormatter,
    ScriptFormatterConfig,
    TypeHintsFormatter,
    TypeHintFormatterConfig,
    ThirdPersonConverter,
    DocstringFormatter,
    DocstringFormatterConfig,
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
    formatter = DocstringFormatter(DocstringFormatterConfig(docstring))

    result = formatter.empty_line_between_description_and_param_list()
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
    formatter = DocstringFormatter(DocstringFormatterConfig(docstring))

    result = formatter.empty_line_between_description_and_param_list()
    assert result == expected

    # multiple empty lines between description and param list
    docstring = [
        '   """',
        "    Description",
        "",
        "",
        "",
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
    formatter = DocstringFormatter(DocstringFormatterConfig(docstring))

    result = formatter.empty_line_between_description_and_param_list()
    assert result == expected


def test_assert_no_unnecessary_prefixes():
    docstring = [
        '   """',
        "    Description",
        "",
        " ., :param param1: description of param1",
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
    formatter = DocstringFormatter(DocstringFormatterConfig(docstring))
    result = formatter.no_unnecessary_prefixes()
    assert result == expected


def test_assert_single_whitespace_after_second_semicolon():
    docstring = [
        '   """',
        "    Description",
        "",
        "    :param param1:   description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    Description",
        "",
        "    :param param1: Description of param1",
        "    :param param2: Description of param2",
        "    :return: Description of return value",
        '    """',
    ]
    formatter = DocstringFormatter(DocstringFormatterConfig(docstring))
    result = formatter.single_whitespace_after_second_semicolon()
    assert result == expected


def test_find_next_docstring():
    file_content = '''
    import os
    import sys

    def some_function():
        """
        Description
        :param param1: description of param1
        :param param2: description of param2
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
    formatter = ScriptFormatter(ScriptFormatterConfig(Path()))
    formatter.content = file_content

    expected = (5, 10)
    result = formatter.find_next_docstring(0)
    assert result == expected

    expected = (17, 22)
    result = formatter.find_next_docstring(11)
    assert result == expected


def test_convert_to_third_person():
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
    converter = ThirdPersonConverter(docstring)
    result = converter.convert()
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
    converter = ThirdPersonConverter(docstring)
    result = converter.convert()
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
    formatter = ScriptFormatter(ScriptFormatterConfig(Path()))
    formatter.content = file_content
    content_as_list = formatter.add_missing_docstrings()

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
        :param param_a: description a
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
        
        :param param_a: description a
        :param param_b: description b
        :param param_c: description c
        :return:
        \"\"\"
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    """
    formatter = ScriptFormatter(ScriptFormatterConfig(Path()))
    formatter.content = file_content
    content_as_list = formatter.preserve_parameter_order()

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
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
