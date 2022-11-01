from src.remove_diacritics import remove_diacritics
import subprocess
import sys
import pytest
from git_root import git_root

original_content = (
    "Chwale nami soplicą wyciągała krucze podano. \n"
    "Niewesoły uczciwość przeleciała śladach ochłonął postrzałem kawę przez ubrać \n"
    "grosz dwadzieścia niewidziano architektury żali pokrewieństwem sokołowi. \n"
    "Potem zawalić natenczas zbiegły plan zaszczepki miał. Szczerbcem swej siedzieli \n"
    "liczna mury nazywać trafia. Przeskoczyć porządek zapytać trafia dotknieniem \n"
    "głównym idą gdzieniegdzie tęsknię."
)

expected_content = (
    "Chwale nami soplica wyciagala krucze podano. \n"
    "Niewesoly uczciwosc przeleciala sladach ochlonal postrzalem kawe przez ubrac \n"
    "grosz dwadziescia niewidziano architektury zali pokrewienstwem sokolowi. \n"
    "Potem zawalic natenczas zbiegly plan zaszczepki mial. Szczerbcem swej siedzieli \n"
    "liczna mury nazywac trafia. Przeskoczyc porzadek zapytac trafia dotknieniem \n"
    "glownym ida gdzieniegdzie tesknie."
)


def test_remove_diacritics(tmpdir):
    # create a temporary text file with diacritics.
    # test if remove_diacritics() removes the diacritics from the file.
    assert original_content != expected_content
    file_name = tmpdir.join("test_remove_diacritics.txt")
    file_name.write_text(original_content, encoding="utf-8")
    remove_diacritics(file_name)

    for result_line, expected_line in zip(
        file_name.read().split("\n"), expected_content.split("\n")
    ):
        assert result_line == expected_line


@pytest.mark.skipif(
    sys.platform == "win32", reason="bash script only available on Linux"
)
def test_remove_diacritics_bash(tmpdir):
    # create a temporary text file with diacritics.
    # test if remove_diacritics() removes the diacritics from the file.
    assert original_content != expected_content
    file_name = tmpdir.join("test_remove_diacritics.txt")
    file_name.write_text(original_content, encoding="utf-8")

    # run bash script
    # ../src/remove_diacritics.sh test_remove_diacritics.txt

    subprocess.check_output([f"{git_root()}/src/remove_diacritics.sh", file_name])
    for result_line, expected_line in zip(
        file_name.read().split("\n"), expected_content.split("\n")
    ):
        assert result_line == expected_line
