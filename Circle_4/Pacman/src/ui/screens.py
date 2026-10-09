"""Application screen states."""

from enum import Enum, auto


class Screen(Enum):
    """Represent one visible application screen."""

    MAIN_MENU = auto()
    GAME = auto()
    PAUSE = auto()
    HIGHSCORES = auto()
    INSTRUCTIONS = auto()
    NAME_ENTRY = auto()
    GAME_OVER = auto()
    VICTORY = auto()
