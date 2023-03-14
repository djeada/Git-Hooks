from src.docstring_physician.parsers.docstring_localizer.docstrings_localizer import (
    DocstringsLocalizer,
)


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
