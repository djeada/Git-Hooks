from src.correct_sphinx_docstrings import assert_empty_line_between_description_and_param_list, \
    assert_no_unnecessary_prefixes, assert_single_whitespace_after_second_semicolon, \
    correct_sphinx_docstrings, find_next_docstring


def test_assert_empty_line_between_description_and_param_list():
    # correct docstring: function shouldn't change anything
    docstring = ['   """', '    Description', '', '    :param param1: description of param1',
                 '    :param param2: description of param2', '    :return: description of return value', '    """']
    expected = docstring
    result = assert_empty_line_between_description_and_param_list(docstring)
    assert result == expected

    # missing empty line between description and param list
    docstring = ['   """', '    Description', '    :param param1: description of param1',
                 '    :param param2: description of param2', '    :return: description of return value', '    """']
    expected = ['   """', '    Description', '', '    :param param1: description of param1',
                '    :param param2: description of param2', '    :return: description of return value', '    """']
    result = assert_empty_line_between_description_and_param_list(docstring)
    assert result == expected

    # multiple empty lines between description and param list
    docstring = ['   """', '    Description', '', '', '', '    :param param1: description of param1',
                 '    :param param2: description of param2', '    :return: description of return value', '    """']
    expected = ['   """', '    Description', '', '    :param param1: description of param1',
                '    :param param2: description of param2', '    :return: description of return value', '    """']
    result = assert_empty_line_between_description_and_param_list(docstring)
    assert result == expected


def test_assert_no_unnecessary_prefixes():
    docstring = ['   """', '    Description', '', ' ., :param param1: description of param1',
                 '    :param param2: description of param2', '    :return: description of return value', '    """']
    expected = ['   """', '    Description', '', '    :param param1: description of param1',
                '    :param param2: description of param2', '    :return: description of return value', '    """']

    result = assert_no_unnecessary_prefixes(docstring)
    assert result == expected


def test_assert_single_whitespace_after_second_semicolon():
    docstring = ['   """', '    Description', '', '    :param param1:   description of param1',
                 '    :param param2: description of param2', '    :return: description of return value', '    """']
    expected = ['   """', '    Description', '', '    :param param1: Description of param1',
                '    :param param2: Description of param2', '    :return: Description of return value', '    """']

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

    file_path = tmpdir.join('test.py')
    file_path.write(file_content)

    correct_sphinx_docstrings(file_path.strpath)

    with open(file_path.strpath, 'r') as f:
        result = f.read()

    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()
