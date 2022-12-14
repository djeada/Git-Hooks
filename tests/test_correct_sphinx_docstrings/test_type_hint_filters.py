from src.correct_docstrings.utils.type_hints_filters import TypeHintsFormatter


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
     """.split(
        "\n"
    )

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
    """.split(
        "\n"
    )

    formatter = TypeHintsFormatter()
    result = formatter.optional_type_hints(file_content)

    for line_result, line_expected in zip(result, expected):
        assert line_result.strip() == line_expected.strip()
