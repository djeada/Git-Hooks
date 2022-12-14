from src.correct_docstrings.utils.docstring_filters import (
    DocstringFormatter,
    EmptyLineBetweenDescriptionAndParams,
    NoRepeatedWhitespaces,
    RemoveUnwantedPrefixes,
    EndOfSentencePunctuation,
    EnsureColonInParamDescription,
    IndentMultilineParamDescription,
    SentenceCapitalization,
)
from src.correct_docstrings.utils.script_filters import (
    ScriptFormatter,
    AddMissingDocstrings,
    PreserveParameterOrder,
)


def test_add_missing_docstring():
    file_content = """import os
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
    """.split(
        "\n"
    )

    expected = '''"""
    """
    
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
    '''.split(
        "\n"
    )
    formatter = AddMissingDocstrings()
    result = formatter.format(file_content)

    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()

    # test class docstring
    file_content = """import os
    import sys

    class SomeClass:
        def __init__(self, param_a: int, param_b: str = "default"):
            self.param_a = param_a
            self.param_b = param_b

        def some_function(self, param_a: int, param_b: str = "default"):
            return param_a + param_b

        def some_other_function(
                                self,
                                param_a,
                                param_b,
                                param_c
                                ):
            return param_a + param_b + param_c

    if __name__ == '__main__':
        
        sc = SomeClass(1, 2)
        sc.some_function(1, 2)
        sc.some_other_function(1, 2, 3)

    """.split(
        "\n"
    )

    expected = '''"""
    """

    import os
    import sys

    class SomeClass:
        """
        Description of class

        :param param_a:
        :param param_b:
        """
        def __init__(self, param_a: int, param_b: str = "default"):
            self.param_a = param_a
            self.param_b = param_b

        def some_function(self, param_a: int, param_b: str = "default"):
            """
            Description of function

            :param param_a:
            :param param_b:
            :return:
            """
            return param_a + param_b

        def some_other_function(
                                self,
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

        sc = SomeClass(1, 2)
        sc.some_function(1, 2)
        sc.some_other_function(1, 2, 3)

    '''.split(
        "\n"
    )

    formatter = AddMissingDocstrings()
    result = formatter.format(file_content)

    for line_result, line_expected in zip(result, expected):
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


def test_script_formatter_config(tmpdir):
    file_content = '''import os
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

    '''.split(
        "\n"
    )

    expected = '''"""
    """
    
    import os
    import sys

    def some_function():
        """
        Description.

        :param param1: Description of param1.
        :param param2: Description of param2
          is multiline.
        :param param3: Description of param 3.
        :return: Description of return value.
        """
        return

    def some_other_function():
        """
        Description.

        :param param1: Description of param1.
        :param param2: Description of param2.
        :return: Description of return value.
        """
        return

    if __name__ == '__main__':
        some_function()
        some_other_function()

    '''.split(
        "\n"
    )

    file_path = tmpdir.join("test.py")
    file_path.write(file_content)
    docstring_filters = [
        EmptyLineBetweenDescriptionAndParams(),
        NoRepeatedWhitespaces(),
        RemoveUnwantedPrefixes(),
        EndOfSentencePunctuation(),
        EnsureColonInParamDescription(),
        IndentMultilineParamDescription(),
        SentenceCapitalization(),
    ]
    docstring_formatter = DocstringFormatter(docstring_filters)
    script_formatter = ScriptFormatter(docstring_formatter)
    result = script_formatter.format(file_content)
    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()
