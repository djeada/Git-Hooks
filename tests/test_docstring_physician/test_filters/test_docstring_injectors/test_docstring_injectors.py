from src.docstring_physician.filters.docstring_injectors.docstring_injector_base import (
    AddMissingDocstrings,
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
