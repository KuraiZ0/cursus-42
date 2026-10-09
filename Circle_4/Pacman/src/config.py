"""Configuration loading and validation."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.constants import (
    DEFAULT_GHOST_RESPAWN_TIME,
    DEFAULT_HIGHSCORE_FILENAME,
    DEFAULT_LEVEL_COUNT,
    DEFAULT_LEVEL_HEIGHT,
    DEFAULT_LEVEL_MAX_TIME,
    DEFAULT_LEVEL_WIDTH,
    DEFAULT_LIVES,
    DEFAULT_POINTS_PER_GHOST,
    DEFAULT_POINTS_PER_PACGUM,
    DEFAULT_POINTS_PER_SUPER_PACGUM,
    DEFAULT_SEED,
    DEFAULT_SUPER_PACGUM_DURATION,
    MAX_LEVEL_SIZE,
    MAX_LEVEL_TIME,
    MAX_LIVES,
    MIN_LEVEL_SIZE,
    MIN_LEVEL_TIME,
    MIN_LIVES,
)
from src.exceptions import ConfigError


@dataclass(frozen=True)
class LevelConfig:
    """Configuration of one game level."""

    width: int
    height: int


@dataclass(frozen=True)
class GameConfig:
    """Validated game configuration."""

    highscore_filename: str
    lives: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    super_pacgum_duration: float
    ghost_respawn_time: float
    level_max_time: int
    seed: int
    levels: tuple[LevelConfig, ...]


def _warn(message: str) -> None:
    """Display a configuration warning."""

    print(f"Configuration warning: {message}")


def _default_levels() -> tuple[LevelConfig, ...]:
    """Return the default list of levels."""

    return tuple(
        LevelConfig(
            width=DEFAULT_LEVEL_WIDTH,
            height=DEFAULT_LEVEL_HEIGHT,
        )
        for _ in range(DEFAULT_LEVEL_COUNT)
    )


def default_config() -> GameConfig:
    """Return a complete default configuration."""

    return GameConfig(
        highscore_filename=DEFAULT_HIGHSCORE_FILENAME,
        lives=DEFAULT_LIVES,
        points_per_pacgum=DEFAULT_POINTS_PER_PACGUM,
        points_per_super_pacgum=DEFAULT_POINTS_PER_SUPER_PACGUM,
        points_per_ghost=DEFAULT_POINTS_PER_GHOST,
        super_pacgum_duration=DEFAULT_SUPER_PACGUM_DURATION,
        ghost_respawn_time=DEFAULT_GHOST_RESPAWN_TIME,
        level_max_time=DEFAULT_LEVEL_MAX_TIME,
        seed=DEFAULT_SEED,
        levels=_default_levels(),
    )


def _remove_comment_lines(content: str) -> str:
    """Remove lines beginning with ``#`` or ``//`` (comment lines)."""

    lines = content.splitlines()
    valid_lines = [
        line
        for line in lines
        if not line.lstrip().startswith(("#", "//"))
    ]
    return "\n".join(valid_lines)


def _safe_int(
    value: Any,
    default: int,
    name: str,
    minimum: int = 0,
    maximum: int | None = None,
) -> int:
    """Validate and clamp an integer configuration value."""

    if isinstance(value, bool) or not isinstance(value, int):
        _warn(f"'{name}' is invalid. Using {default}.")
        return default

    result = max(value, minimum)

    if maximum is not None:
        result = min(result, maximum)

    if result != value:
        _warn(f"'{name}' was adjusted to {result}.")

    return result


def _safe_float(
    value: Any,
    default: float,
    name: str,
    minimum: float = 0.0,
) -> float:
    """Validate a floating-point configuration value."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        _warn(f"'{name}' is invalid. Using {default}.")
        return default

    result = float(value)

    if result < minimum:
        _warn(f"'{name}' is invalid. Using {default}.")
        return default

    return result


def _safe_filename(value: Any) -> str:
    """Validate the highscore filename."""

    if not isinstance(value, str) or not value.strip():
        _warn(
            "Invalid highscore filename. "
            f"Using '{DEFAULT_HIGHSCORE_FILENAME}'."
        )
        return DEFAULT_HIGHSCORE_FILENAME

    return value.strip()


def _safe_dimension(value: Any, default: int, name: str) -> int:
    """Validate a maze dimension expressed in cells."""

    dimension = _safe_int(
        value=value,
        default=default,
        name=name,
        minimum=MIN_LEVEL_SIZE,
        maximum=MAX_LEVEL_SIZE,
    )

    return dimension


def _parse_levels(value: Any) -> tuple[LevelConfig, ...]:
    """Validate the configured levels."""

    if not isinstance(value, list):
        _warn("Invalid levels list. Using default levels.")
        return _default_levels()

    levels: list[LevelConfig] = []

    for index, level_data in enumerate(value):
        if not isinstance(level_data, dict):
            _warn(f"Level {index + 1} is invalid and was ignored.")
            continue

        width = _safe_dimension(
            value=level_data.get("width"),
            default=DEFAULT_LEVEL_WIDTH,
            name=f"levels[{index}].width",
        )
        height = _safe_dimension(
            value=level_data.get("height"),
            default=DEFAULT_LEVEL_HEIGHT,
            name=f"levels[{index}].height",
        )

        levels.append(LevelConfig(width=width, height=height))

    while len(levels) < DEFAULT_LEVEL_COUNT:
        levels.append(
            LevelConfig(
                width=DEFAULT_LEVEL_WIDTH,
                height=DEFAULT_LEVEL_HEIGHT,
            )
        )

    return tuple(levels)


def _read_json_file(path: Path) -> dict[str, Any]:
    """Read and decode a JSON configuration file."""

    if not path.is_file():
        raise ConfigError(f"Configuration file not found: {path}")

    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise ConfigError(
            f"Unable to read configuration file: {error}"
        ) from error

    cleaned_content = _remove_comment_lines(content)

    try:
        decoded = json.loads(cleaned_content)
    except json.JSONDecodeError:
        _warn("Invalid JSON format. Using the default configuration.")
        return {}

    if not isinstance(decoded, dict):
        _warn("The configuration root must be an object.")
        return {}

    return decoded


def load_config(filename: str) -> GameConfig:
    """Load and validate the game configuration."""

    data = _read_json_file(Path(filename))

    return GameConfig(
        highscore_filename=_safe_filename(
            data.get(
                "highscore_filename",
                DEFAULT_HIGHSCORE_FILENAME,
            )
        ),
        lives=_safe_int(
            value=data.get("lives", DEFAULT_LIVES),
            default=DEFAULT_LIVES,
            name="lives",
            minimum=MIN_LIVES,
            maximum=MAX_LIVES,
        ),
        points_per_pacgum=_safe_int(
            value=data.get(
                "points_per_pacgum",
                DEFAULT_POINTS_PER_PACGUM,
            ),
            default=DEFAULT_POINTS_PER_PACGUM,
            name="points_per_pacgum",
        ),
        points_per_super_pacgum=_safe_int(
            value=data.get(
                "points_per_super_pacgum",
                DEFAULT_POINTS_PER_SUPER_PACGUM,
            ),
            default=DEFAULT_POINTS_PER_SUPER_PACGUM,
            name="points_per_super_pacgum",
        ),
        points_per_ghost=_safe_int(
            value=data.get(
                "points_per_ghost",
                DEFAULT_POINTS_PER_GHOST,
            ),
            default=DEFAULT_POINTS_PER_GHOST,
            name="points_per_ghost",
        ),
        super_pacgum_duration=_safe_float(
            value=data.get(
                "super_pacgum_duration",
                DEFAULT_SUPER_PACGUM_DURATION,
            ),
            default=DEFAULT_SUPER_PACGUM_DURATION,
            name="super_pacgum_duration",
        ),
        ghost_respawn_time=_safe_float(
            value=data.get(
                "ghost_respawn_time",
                DEFAULT_GHOST_RESPAWN_TIME,
            ),
            default=DEFAULT_GHOST_RESPAWN_TIME,
            name="ghost_respawn_time",
        ),
        level_max_time=_safe_int(
            value=data.get(
                "level_max_time",
                DEFAULT_LEVEL_MAX_TIME,
            ),
            default=DEFAULT_LEVEL_MAX_TIME,
            name="level_max_time",
            minimum=MIN_LEVEL_TIME,
            maximum=MAX_LEVEL_TIME,
        ),
        seed=_safe_int(
            value=data.get("seed", DEFAULT_SEED),
            default=DEFAULT_SEED,
            name="seed",
            minimum=1,
        ),
        levels=_parse_levels(data.get("levels")),
    )
