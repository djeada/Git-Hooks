from src.docstring_physician.filters.docstrings_validators.class_init_parameter_match_validator import (
    ClassInitParameterMatchValidator,
)
from src.docstring_physician.filters.docstrings_validators.module_docstring_validator import (
    ModuleDocstringValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_class_docstring_validator import (
    PublicClassDocstringValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_function_docstring_validator import (
    PublicFunctionDocstringValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_function_parameter_match_validator import (
    PublicFunctionParameterMatchValidator,
)
from src.docstring_physician.filters.docstrings_validators.public_function_parameter_presence_validator import (
    PublicFunctionParameterPresenceValidator,
)


def test_module_docstring_filter():
    # Correct docstring: first non-empty line is a module docstring
    docstring = [
        '"""',
        "This is a module docstring.",
        '"""',
        "class MyClass:",
        "    pass",
    ]
    expected = True
    filter = ModuleDocstringValidator()

    result = filter.check(docstring)
    assert result == expected

    docstring = [
        "",
        '"""',
        "This is a module docstring.",
        '"""',
        "class MyClass:",
        "    pass",
    ]
    expected = True
    filter = ModuleDocstringValidator()

    result = filter.check(docstring)
    assert result == expected

    # Incorrect docstring: first non-empty line is not a module docstring
    docstring = [
        "class MyClass:",
        "    pass",
    ]
    expected = False

    result = filter.check(docstring)
    assert result == expected


def test_public_class_docstring_filter():
    # Correct docstring: all public classes have docstrings
    docstring = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "class PublicClass:",
        '    """Public class docstring"""',
        "    pass",
        "",
        "class _PrivateClass:",
        "    pass",
    ]
    expected = True
    filter = PublicClassDocstringValidator()

    result = filter.check(docstring)
    assert result == expected

    # Incorrect docstring: a public class is missing a docstring
    docstring = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "class PublicClass:",
        "    pass",
        "",
        "class _PrivateClass:",
        '    """Private class docstring"""',
        "    pass",
    ]
    expected = False

    result = filter.check(docstring)
    assert result == expected


def test_public_function_docstring_filter():
    # Correct docstring: all public functions have docstrings
    docstring = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "def public_function():",
        '    """Public function docstring"""',
        "    pass",
        "",
        "def _private_function():",
        "    pass",
    ]
    expected = True
    filter = PublicFunctionDocstringValidator()

    result = filter.check(docstring)
    assert result == expected

    # Correct docstring: all public functions have docstrings
    docstring = '''
    @staticmethod
    def calculate_scale_vector(
        ref_volume: float, block: blocks.VtkBlock
    ) -> utility.Vector3D:
        """
        Calculates the scale vector from a block and a reference volume.

        :param ref_volume: Reference volume.
        :param block: Block.
        :return: Scale vector.
        """
        min_, max_ = snaplib.blocks.extractors.BoundingBoxExtractor().extract(block)
        bb_volume = float(np.prod(np.array(max_) - np.array(min_)))

        scale_factor = float(np.cbrt(ref_volume / bb_volume))
        scale_vector = (scale_factor, scale_factor, scale_factor)
        return scale_vector'''.split(
        "\n"
    )

    expected = True
    result = filter.check(docstring)
    assert result == expected

    # Incorrect docstring: a public function is missing a docstring
    docstring = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "def public_function():",
        "    pass",
        "",
        "def _private_function():",
        '    """Private function docstring"""',
        "    pass",
    ]
    expected = False

    result = filter.check(docstring)
    assert result == expected


def test_public_function_parameter_docstring_filter():
    # Correct docstring: all public functions have parameter descriptions
    docstring = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "def public_function(param1: int, param2: str) -> bool:",
        '    """',
        "    Public function docstring",
        "",
        "    :param param1: Description for param1",
        "    :param param2: Description for param2",
        "    :return: Description for return value",
        '    """',
        "    pass",
        "",
        "def _private_function():",
        "    pass",
    ]
    expected = True
    filter = PublicFunctionParameterMatchValidator()

    result = filter.check(docstring)
    assert result == expected

    # Incorrect docstring: a public function is missing a parameter description
    docstring = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "def public_function(param1: int, param2: str) -> bool:",
        '    """',
        "    Public function docstring",
        "",
        "    :param param1: Description for param1",
        "    :return: Description for return value",
        '    """',
        "    pass",
        "",
        "def _private_function():",
        "    pass",
    ]
    expected = False

    result = filter.check(docstring)
    assert result == expected


def test_public_function_parameter_mismatch_filter():
    filter = PublicFunctionParameterPresenceValidator()

    # Test with function that has correct parameter descriptions
    content = '''
        def public_function(param1: int, param2: str) -> None:
            """
            Function description.

            :param param1: Description for param1.
            :param param2: Description for param2.
            """
            pass
    '''.split(
        "\n"
    )
    assert filter.check(content)

    # Test with function that has incorrect parameter descriptions
    content = '''
        def public_function(param1: int, param2: str) -> None:
            """
            Function description.

            :param param1: Incorrect description for param1.
            :param param2: Description for param2.
            :param param3: Description for param3.
            """
            pass
    '''.split(
        "\n"
    )
    assert not filter.check(content)

    # Test with function that has missing parameter descriptions
    content = '''
        def public_function(param1: int, param2: str) -> None:
            """
            Function description.

            :param param1: Description for param1.
            """
            pass
    '''.split(
        "\n"
    )
    assert filter.check(content)

    # Test with private function that should be ignored
    content = '''
        def _private_function(param1: int, param2: str) -> None:
            """
            Function description.

            :param param1: Description for param1.
            :param param2: Description for param2.
            """
            pass
    '''.split(
        "\n"
    )
    assert filter.check(content)


def test_class_init_parameter_docstring_validator():
    # Correct docstring: all class __init__ methods have parameter descriptions
    content = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "class ExampleClass:",
        '    """',
        "    ExampleClass docstring",
        "",
        "    :param param1: Description for param1",
        "    :param param2: Description for param2",
        '    """',
        "",
        "    def __init__(self, param1: int, param2: str):",
        "        pass",
        "",
        "class AnotherClass:",
        '    """',
        "    AnotherClass docstring",
        "",
        "    :param param_a: Description for param_a",
        "    :param param_b: Description for param_b",
        '    """',
        "",
        "    def __init__(self, param_a: int, param_b: str):",
        "        pass",
    ]
    expected = True
    validator = ClassInitParameterMatchValidator()

    result = validator.check(content)
    if result != expected:
        print("Expected: ", expected)
        print("Actual: ", result)
        print("Content: ", content)
    assert result == expected

    # Incorrect docstring: a class __init__ method is missing a parameter description
    content = [
        '"""',
        "Module docstring",
        '"""',
        "",
        "class ExampleClass:",
        '    """',
        "    ExampleClass docstring",
        "",
        "    :param param1: Description for param1",
        '    """',
        "",
        "    def __init__(self, param1: int, param2: str):",
        "        pass",
        "",
        "class AnotherClass:",
        '    """',
        "    AnotherClass docstring",
        "",
        "    :param param_a: Description for param_a",
        "    :param param_b: Description for param_b",
        '    """',
        "",
        "    def __init__(self, param_a: int, param_b: str):",
        "        pass",
    ]
    expected = False

    result = validator.check(content)
    if result != expected:
        print("Expected: ", expected)
        print("Actual: ", result)
        print("Content: ", content)
    assert result == expected
