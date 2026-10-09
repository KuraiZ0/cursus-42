"""Constants shared across the Pac-Man project."""

from typing import Final

GAME_TITLE: Final[str] = "Pac-Man 42"

WINDOW_WIDTH: Final[int] = 960
WINDOW_HEIGHT: Final[int] = 720
FPS: Final[int] = 60
TILE_SIZE: Final[int] = 24

BLACK: Final[tuple[int, int, int]] = (0, 0, 0)
WHITE: Final[tuple[int, int, int]] = (255, 255, 255)
YELLOW: Final[tuple[int, int, int]] = (255, 255, 0)
BLUE: Final[tuple[int, int, int]] = (30, 60, 255)
RED: Final[tuple[int, int, int]] = (255, 50, 50)

DEFAULT_HIGHSCORE_FILENAME: Final[str] = "highscores.json"
DEFAULT_LIVES: Final[int] = 3
DEFAULT_POINTS_PER_PACGUM: Final[int] = 10
DEFAULT_POINTS_PER_SUPER_PACGUM: Final[int] = 50
DEFAULT_POINTS_PER_GHOST: Final[int] = 200
DEFAULT_SUPER_PACGUM_DURATION: Final[float] = 8.0
DEFAULT_GHOST_RESPAWN_TIME: Final[float] = 5.0
DEFAULT_LEVEL_MAX_TIME: Final[int] = 90
DEFAULT_SEED: Final[int] = 42

DEFAULT_LEVEL_COUNT: Final[int] = 10
DEFAULT_LEVEL_WIDTH: Final[int] = 21
DEFAULT_LEVEL_HEIGHT: Final[int] = 21

MIN_LEVEL_SIZE: Final[int] = 7
MAX_LEVEL_SIZE: Final[int] = 51

MIN_LIVES: Final[int] = 1
MAX_LIVES: Final[int] = 10

MIN_LEVEL_TIME: Final[int] = 10
MAX_LEVEL_TIME: Final[int] = 600
