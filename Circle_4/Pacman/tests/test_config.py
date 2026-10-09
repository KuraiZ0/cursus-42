"""Tests for configuration loading."""

from pathlib import Path

import pytest

from src.config import load_config
from src.exceptions import ConfigError


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


def test_dimensions_are_clamped(
    tmp_path: Path,
) -> None:
    """Test that out-of-range maze sizes are clamped."""

    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
        {
            "levels": [
                {"width": 2, "height": 1000},
                {"width": 20, "height": 14}
            ]
        }
        """,
        encoding="utf-8",
    )

    config = load_config(str(config_file))

    assert config.levels[0].width == 5
    assert config.levels[0].height == 30
    assert config.levels[1].width == 20
    assert config.levels[1].height == 14


def test_comment_styles_and_any_file_name(
    tmp_path: Path,
) -> None:
    """Test '#' and '//' comments, and a file without extension."""

    config_file = tmp_path / "settings"
    config_file.write_text(
        """
        # hash comment
        // slash comment
        {"lives": 4, "unknown_key": true}
        """,
        encoding="utf-8",
    )

    config = load_config(str(config_file))

    assert config.lives == 4


def test_seed_zero_is_replaced(
    tmp_path: Path,
) -> None:
    """Test that seed 0 (random for the generator) is not accepted."""

    config_file = tmp_path / "config.json"
    config_file.write_text('{"seed": 0}', encoding="utf-8")

    assert load_config(str(config_file)).seed == 1


def test_missing_file_raises_config_error() -> None:
    """Test the error raised for a missing configuration file."""

    with pytest.raises(ConfigError):
        load_config("does_not_exist.json")


def test_invalid_json_uses_defaults(
    tmp_path: Path,
) -> None:
    """Test that malformed JSON falls back to the defaults."""

    config_file = tmp_path / "config.json"
    config_file.write_text("{ not json", encoding="utf-8")

    config = load_config(str(config_file))

    assert config.lives == 3
    assert len(config.levels) == 10
