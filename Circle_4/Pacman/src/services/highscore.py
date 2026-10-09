"""Persistent highscore management."""

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from src.exceptions import HighscoreError


@dataclass(frozen=True)
class HighscoreEntry:
    """Represent one highscore entry."""

    name: str
    score: int


class HighscoreService:
    """Load, validate and save highscore entries."""

    MAX_ENTRIES = 10
    MAX_NAME_LENGTH = 10

    def __init__(self, filename: str) -> None:
        """Initialise the highscore service."""

        self.path = Path(filename)
        self.entries: list[HighscoreEntry] = []

    def load(self) -> list[HighscoreEntry]:
        """Load valid highscores from disk."""

        if not self.path.exists():
            self.entries = []
            return self.entries.copy()

        try:
            content = self.path.read_text(encoding="utf-8")
            decoded = json.loads(content)
        except (OSError, json.JSONDecodeError):
            self.entries = []
            return self.entries.copy()

        if not isinstance(decoded, list):
            self.entries = []
            return self.entries.copy()

        loaded_entries: list[HighscoreEntry] = []

        for raw_entry in decoded:
            entry = self._parse_entry(raw_entry)

            if entry is not None:
                loaded_entries.append(entry)

        self.entries = self._sort_and_limit(loaded_entries)
        return self.entries.copy()

    def add(
        self,
        name: str,
        score: int,
    ) -> HighscoreEntry:
        """Add and save a new highscore entry."""

        cleaned_name = self.validate_name(name)
        cleaned_score = self.validate_score(score)

        entry = HighscoreEntry(
            name=cleaned_name,
            score=cleaned_score,
        )

        self.entries.append(entry)
        self.entries = self._sort_and_limit(self.entries)
        self.save()

        return entry

    def save(self) -> None:
        """Save the current highscores to disk."""

        serialised_entries = [
            asdict(entry)
            for entry in self.entries
        ]

        try:
            self.path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
            self.path.write_text(
                json.dumps(
                    serialised_entries,
                    indent=4,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
        except OSError as error:
            raise HighscoreError(
                f"Unable to save highscores: {error}"
            ) from error

    def validate_name(self, name: str) -> str:
        """Validate and return a player name."""

        cleaned_name = name.strip()

        if not cleaned_name:
            raise HighscoreError(
                "The player name cannot be empty."
            )

        if len(cleaned_name) > self.MAX_NAME_LENGTH:
            raise HighscoreError(
                "The player name cannot exceed "
                f"{self.MAX_NAME_LENGTH} characters."
            )

        if not all(
            character.isalnum() or character == " "
            for character in cleaned_name
        ):
            raise HighscoreError(
                "The player name may only contain "
                "letters, numbers and spaces."
            )

        return cleaned_name

    def validate_score(self, score: int) -> int:
        """Validate and return a player score."""

        if isinstance(score, bool) or not isinstance(score, int):
            raise HighscoreError(
                "The score must be an integer."
            )

        if score < 0:
            raise HighscoreError(
                "The score cannot be negative."
            )

        return score

    def _parse_entry(
        self,
        raw_entry: Any,
    ) -> HighscoreEntry | None:
        """Convert one raw entry when valid."""

        if not isinstance(raw_entry, dict):
            return None

        name = raw_entry.get("name")
        score = raw_entry.get("score")

        if not isinstance(name, str):
            return None

        if isinstance(score, bool) or not isinstance(score, int):
            return None

        try:
            valid_name = self.validate_name(name)
            valid_score = self.validate_score(score)
        except HighscoreError:
            return None

        return HighscoreEntry(
            name=valid_name,
            score=valid_score,
        )

    def _sort_and_limit(
        self,
        entries: list[HighscoreEntry],
    ) -> list[HighscoreEntry]:
        """Sort entries and keep only the ten best."""

        return sorted(
            entries,
            key=lambda entry: entry.score,
            reverse=True,
        )[:self.MAX_ENTRIES]
