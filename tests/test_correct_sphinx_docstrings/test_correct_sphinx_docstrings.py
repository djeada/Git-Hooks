import subprocess
from git_root import git_root


def test_script_formatter_config(tmpdir):
    file_content = '''
"""
This module contains a simple class and a main function to demonstrate its use.

.. moduleauthor: Your Name <your.email@example.com>
"""

class Rectangle:
    """
    A class representing a rectangle.

    :ivar length: The length of the rectangle.
    :ivar width: The width of the rectangle.
    """

    def __init__(self, length: float, width: float) -> None:
        """
        Initializes a new Rectangle instance.

        :param length: The length of the rectangle.
        :param width: The width of the rectangle.
          """
        self.length = length
        self.width = width

    def area(self) -> float:
        """
        Calculates the area of the rectangle.

        :return: The area of the rectangle.
        :rtype: float.
        """
        return self.length * self.width

def main() -> None:
    """
    Creates a Rectangle instance, calculates its area, and prints the result.
    """
    rectangle = Rectangle(5, 10)
    area = rectangle.area()
    print(f"The area of the rectangle is {area}.")

if __name__ == '__main__':
    main()
    '''

    expected = '''
"""
This module contains a simple class and a main function to demonstrate its use.

.. moduleauthor: Your Name <your.email@example.com>
"""

class Rectangle:
    """
    A class representing a rectangle.

    :ivar length: The length of the rectangle.
    :ivar width: The width of the rectangle.
    """

    def __init__(self, length: float, width: float) -> None:
        """
        Initializes a new Rectangle instance.

        :param length: The length of the rectangle.
        :param width: The width of the rectangle.
          """
        self.length = length
        self.width = width

    def area(self) -> float:
        """
        Calculates the area of the rectangle.

        :return: The area of the rectangle.
        :rtype: float.
        """
        return self.length * self.width

def main() -> None:
    """
    Creates a Rectangle instance, calculates its area, and prints the result.
    """
    rectangle = Rectangle(5, 10)
    area = rectangle.area()
    print(f"The area of the rectangle is {area}.")

if __name__ == '__main__':
    main()
    '''
    file_path = tmpdir.join("test.py")
    file_path.write(file_content)

    # call python script 'python correct_docstrings.py file_path' with subprocess and then check if file was changed
    result = subprocess.run(
        [
            "python",
            f"{git_root()}/src/correct_docstrings/correct_docstrings.py",
            file_path.strpath,
        ]
    )

    with open(file_path.strpath, "r") as f:
        result = f.read()

    for line_result, line_expected in zip(result.split("\n"), expected.split("\n")):
        assert line_result.strip() == line_expected.strip()
