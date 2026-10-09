#!/usr/bin/env python3

"""Command-line entry point for the Pac-Man game."""

import sys

import pygame

from src.app import App
from src.config import load_config
from src.exceptions import PacmanError


def main() -> int:
    """Validate arguments and launch the game."""

    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py config.json")
        return 1

    try:
        config = load_config(sys.argv[1])
        application = App(config)
        application.run()
    except KeyboardInterrupt:
        print("Game interrupted.")
        return 130
    except PacmanError as error:
        print(f"Pac-Man error: {error}")
        return 1
    except pygame.error as error:
        print(f"Graphical error: {error}")
        return 1
    except OSError as error:
        print(f"System error: {error}")
        return 1
    except Exception as error:
        print(f"Unexpected error: {error}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
