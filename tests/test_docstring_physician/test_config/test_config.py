from pathlib import Path

from src.docstring_physician.config.config import MainFormatterConfig


def test_json_methods(tmpdir):
    # Create a test instance of MainFormatterConfig
    config = MainFormatterConfig()

    # Save the instance to a temporary JSON file
    json_path = Path(tmpdir / "test_config.json")
    config.to_json(json_path)

    # Load the instance back from the JSON file
    loaded_config = MainFormatterConfig.from_json(json_path)

    # Compare the original and loaded instances
    assert config == loaded_config, "The original and loaded instances are not equal"
