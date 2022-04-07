from src.correct_sphinx_docstrings import (
    assert_empty_line_between_description_and_param_list,
    assert_no_unnecessary_prefixes,
    assert_single_whitespace_after_second_semicolon,
    correct_sphinx_docstrings,
    find_next_docstring,
    convert_to_third_person,
    add_missing_docstring, assert_optional_type_hints,
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
    result = assert_empty_line_between_description_and_param_list(docstring.copy())
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
    result = assert_empty_line_between_description_and_param_list(docstring)
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
    result = assert_empty_line_between_description_and_param_list(docstring)
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

    result = assert_no_unnecessary_prefixes(docstring)
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

    result = assert_single_whitespace_after_second_semicolon(docstring)
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

    expected = (5, 10)
    result = find_next_docstring(file_content.split("\n"), 0)
    assert result == expected

    expected = (14, 19)
    result = find_next_docstring(file_content.split("\n"), 11)
    assert result == expected


def test_correct_sphinx_docstrings(tmpdir):
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

    correct_sphinx_docstrings(file_path.strpath)

    with open(file_path.strpath, "r") as f:
        result = f.read()

    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()


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
    result = convert_to_third_person(docstring.copy())
    assert result == expected

    docstring = [
        '   """',
        "    use unlimited option",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    expected = [
        '   """',
        "    uses unlimited option",
        "",
        "    :param param1: description of param1",
        "    :param param2: description of param2",
        "    :return: description of return value",
        '    """',
    ]
    result = convert_to_third_person(docstring.copy())
    assert result == expected


def test_add_missing_docstring():
    file_content = """
    import os
    import sys

    def some_function(param_a, param_b):
        return param_a + param_b
    
    def some_other_function(param_a, param_b, param_c):
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    """

    expected = '''
    import os
    import sys

    def some_function(param_a, param_b):
        """
        Description of function
        
        :param param_a:
        :param param_b:
        :return:
        """
        return param_a + param_b
    
    def some_other_function(param_a, param_b, param_c):
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

    content_as_list = file_content.split("\n")
    content_as_list = add_missing_docstring(content_as_list.copy())

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()


def test_assert_optional_type_hints():
    file_content = '''
    import os
    import sys

    def some_function(param_a: int, param_b: str = None):
        return param_a + param_b

    def some_other_function(param_a: int, param_b: str = None, param_c: int = None):
        return param_a + param_b + param_c
    
    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
     '''

    expected = '''
    import os
    import sys

    def some_function(param_a: int, param_b: Optional[str] = None):
        return param_a + param_b
    
    def some_other_function(param_a: int, param_b: Optional[str] = None, param_c: Optional[int] = None):
        return param_a + param_b + param_c

    if __name__ == '__main__':
        some_function(1, 2)
        some_other_function(1, 2, 3)
    '''

    content_as_list = file_content.split("\n")
    content_as_list = assert_optional_type_hints(content_as_list.copy())

    result = "\n".join(content_as_list)
    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()
