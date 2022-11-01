from git_root import git_root

from src.correct_file_names import correct_file_name
import subprocess
import sys
import pytest
from pathlib import Path

temp_dir = "temp"
temp_names_to_correct = {
    "file NAME 1": "file_name_1",
    "FILE NAME 2": "file_name_2",
    "file name3": "file_name3",
}


def test_correct_file_name(tmpdir):
    # create a temp dir and temp files in it
    # correct file names and check if they are correct
    temp_dir_path = tmpdir.mkdir(temp_dir)
    for file_name in temp_names_to_correct.keys():
        (temp_dir_path / file_name).write("temp")
    for file in temp_dir_path.listdir():
        correct_file_name(file)
        new_file_name = temp_names_to_correct[file.basename]
        new_file = temp_dir_path / new_file_name
        assert not file.exists()
        assert new_file.exists()


@pytest.mark.skipif(
    sys.platform == "win32", reason="bash script only available on Linux"
)
def test_correct_file_name_bash(tmpdir):
    # create a temp dir and temp files in it
    # correct file names and check if they are correct
    temp_dir_path = tmpdir.mkdir(temp_dir)
    for file_name in temp_names_to_correct.keys():
        (temp_dir_path / file_name).write("temp")
    for file in tmpdir.join(temp_dir).listdir():
        result = subprocess.run(
            ["bash", f"{git_root()}/src/correct_file_names.sh", f"{file.strpath}"]
        )
        print(result)
        new_file_name = temp_names_to_correct[file.basename]
        new_file = temp_dir_path / new_file_name
        assert not file.exists()
        assert new_file.exists()
