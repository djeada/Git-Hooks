from git_root import git_root

from src.remove_trailing_whitespaces import remove_trailing_whitespaces
import subprocess
import sys
import pytest

original_content = (
    "1.This is a test file \n" "2.This is a test file      \n" "3.This is a test file "
)

expected_content = (
    "1.This is a test file\n" "2.This is a test file\n" "3.This is a test file"
)


# test python script
def test_remove_trailing_whitespaces(tmpdir):
    # create a temporary text file with trailing whitespaces.
    # test if remove_trailing_whitespaces() removes the whitespaces from the file.
    assert original_content != expected_content
    file_name = tmpdir.join("test_remove_trailing_whitespaces.txt")
    file_name.write(original_content)
    remove_trailing_whitespaces(file_name)
    assert file_name.read() == expected_content


# test bash script
@pytest.mark.skipif(
    sys.platform == "win32", reason="bash script only available on Linux"
)
def test_remove_trailing_whitespaces_bash(tmpdir):
    # create a temporary text file with trailing whitespaces.
    # test if remove_trailing_whitespaces() removes the whitespaces from the file.
    assert original_content != expected_content
    file_name = tmpdir.join("test_remove_trailing_whitespaces.txt")
    file_name.write(original_content)

    # run bash script
    # ../src/remove_trailing_whitespaces.sh test_remove_trailing_whitespaces.txt
    subprocess.check_output(
        [f"{git_root()}/src/remove_trailing_whitespaces.sh", file_name]
    )
    assert file_name.read() == expected_content + "\n"
