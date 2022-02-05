from src.correct_file_names import correct_file_name
import subprocess
import sys
import pytest
from pathlib import Path

temp_dir = 'temp'
temp_names_to_correct = {'file NAME 1':'file_name_1', 'FILE NAME 2':'file_name_2', 'file name3':'file_name3'}

def test_correct_file_name(tmpdir):
    # create a temp dir and temp files in it
    # correct file names and check if they are correct
    tmpdir.mkdir(temp_dir)
    for file in temp_names_to_correct.keys():
        tmpdir.join(temp_dir, file).write(file)
    for file in tmpdir.join(temp_dir).listdir():
        correct_file_name(file)
        new_file_name = temp_names_to_correct[file.basename]
        new_file = tmpdir.join(temp_dir, new_file_name)
        assert not file.exists()
        assert new_file.exists()

@pytest.mark.skipif(sys.platform == "win32", reason="bash script only available on Linux")
def test_correct_file_name_bash(tmpdir):
    # create a temp dir and temp files in it
    # correct file names and check if they are correct
    tmpdir.mkdir(temp_dir)
    for file in temp_names_to_correct.keys():
        tmpdir.join(temp_dir, file).write(file)
    for file in tmpdir.join(temp_dir).listdir():
        subprocess.run(['bash', 'src/correct_file_names.sh', file.strpath])
        new_file_name = temp_names_to_correct[file.basename]
        new_file = tmpdir.join(temp_dir, new_file_name)
        assert not file.exists()
        assert new_file.exists()
