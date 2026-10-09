"""Tests for configuration loading."""

from pathlib import Path

from src.config import load_config


def test_load_valid_configuration(
    tmp_path: Path,
) -> None:
    """Test loading a valid configuration file."""

    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        # Test configuration
        {
            "lives": 5,
            "seed": 123,
            "level_max_time": 120,
            "levels": [
                {
                    "width": 21,
                    "height": 21
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = load_config(str(config_file))

    assert config.lives == 5
    assert config.seed == 123
    assert config.level_max_time == 120
    assert len(config.levels) >= 10


def test_invalid_values_use_safe_defaults(
    tmp_path: Path,
) -> None:
    """Test invalid configuration value handling."""

    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        {
            "lives": "invalid",
            "level_max_time": -50,
            "levels": "invalid"
        }
        """,
        encoding="utf-8",
    )

    config = load_config(str(config_file))

    assert config.lives == 3
    assert config.level_max_time == 10
    assert len(config.levels) == 10


def test_even_dimensions_become_odd(
    tmp_path: Path,
) -> None:
    """Test automatic odd maze dimensions."""

    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        {
            "levels": [
                {
                    "width": 20,
                    "height": 22
                }
            ]
        }
        """,
        encoding="utf-8",
    )

    config = load_config(str(config_file))

    assert config.levels[0].width == 21
    assert config.levels[0].height == 23
