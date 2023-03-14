from src.docstring_physician.config.config import DocstringFormatterConfig


def test_read_write_json(tmpdir):
    config = DocstringFormatterConfig()
    file_name = tmpdir.join("test.json")

    config.to_json(file_name)

    config2 = DocstringFormatterConfig.from_json(file_name)

    assert config == config2
