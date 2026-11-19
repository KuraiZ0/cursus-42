"""Tests for the highscore service."""

import json
from pathlib import Path

import pytest

from src.exceptions import HighscoreError
from src.services.highscore import HighscoreService


def test_add_and_load_highscore(
    tmp_path: Path,
) -> None:
    """Test saving and loading one highscore."""

    highscore_file = tmp_path / "scores.json"
    service = HighscoreService(str(highscore_file))

    service.add("WAIL", 4200)

    loaded_entries = service.load()

    assert len(loaded_entries) == 1
    assert loaded_entries[0].name == "WAIL"
    assert loaded_entries[0].score == 4200


def test_keep_only_ten_best_scores(
    tmp_path: Path,
) -> None:
    """Test highscore sorting and limiting."""

    highscore_file = tmp_path / "scores.json"
    service = HighscoreService(str(highscore_file))

    for index in range(15):
        service.add(
            name=f"P{index}",
            score=index * 100,
        )

    entries = service.load()

    assert len(entries) == 10
    assert entries[0].score == 1400
    assert entries[-1].score == 500


def test_invalid_name_is_rejected(
    tmp_path: Path,
) -> None:
    """Test rejection of unsupported characters."""

    service = HighscoreService(
        str(tmp_path / "scores.json")
    )

    with pytest.raises(HighscoreError):
        service.add("BAD!!!", 100)


def test_corrupted_file_returns_empty_list(
    tmp_path: Path,
) -> None:
    """Test corrupted highscore file handling."""

    highscore_file = tmp_path / "scores.json"
    highscore_file.write_text(
        "not valid json",
        encoding="utf-8",
    )

    service = HighscoreService(str(highscore_file))

    assert service.load() == []


def test_saved_file_contains_valid_json(
    tmp_path: Path,
) -> None:
    """Test the generated highscore JSON file."""

    highscore_file = tmp_path / "scores.json"
    service = HighscoreService(str(highscore_file))

    service.add("PAC MAN", 800)

    decoded = json.loads(
        highscore_file.read_text(encoding="utf-8")
    )

    assert decoded == [
        {
            "name": "PAC MAN",
            "score": 800,
        }
    ]
