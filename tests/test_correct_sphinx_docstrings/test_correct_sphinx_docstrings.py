import subprocess
from git_root import git_root


def test_script_formatter_config(tmpdir):
    file_content = '''
    import os
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

    '''

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

    '''
    file_path = tmpdir.join("test.py")
    file_path.write(file_content)

    # call python script 'python correct_docstrings.py file_path' with subprocess and then check if file was changed
    subprocess.run(
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
