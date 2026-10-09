"""Custom exceptions used by the Pac-Man project."""


class PacmanError(Exception):
    """Base exception for all Pac-Man errors."""


class ConfigError(PacmanError):
    """Raised when the configuration file cannot be loaded."""


class MazeError(PacmanError):
    """Raised when the maze cannot be generated."""


class HighscoreError(PacmanError):
    """Raised when highscores cannot be loaded or saved."""
