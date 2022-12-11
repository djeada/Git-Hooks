from src.correct_docstrings.utils.config import TypeHintFormatterConfig
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
