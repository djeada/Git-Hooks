from src.correct_docstrings.utils.formatting_conditions import (
    ModuleDocstringFilter,
    PublicClassDocstringFilter,
    PublicFunctionDocstringFilter,
    PublicFunctionParameterDocstringFilter,
    PublicFunctionParameterMismatchFilter,
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
    filter = ModuleDocstringFilter()

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
    filter = PublicClassDocstringFilter()

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
    filter = PublicFunctionDocstringFilter()

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
    filter = PublicFunctionDocstringFilter()

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
    filter = PublicFunctionParameterDocstringFilter()

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
    filter = PublicFunctionParameterMismatchFilter()

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
