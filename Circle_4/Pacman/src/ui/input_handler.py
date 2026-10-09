"""Keyboard input conversion."""

import pygame

from src.entities.entity import Direction


class InputHandler:
    """Convert Pygame events into application actions."""

    DIRECTION_KEYS = {
        pygame.K_UP: Direction.UP,
        pygame.K_w: Direction.UP,
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_s: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_a: Direction.LEFT,
        pygame.K_RIGHT: Direction.RIGHT,
        pygame.K_d: Direction.RIGHT,
    }

    def get_direction(
        self,
        key: int,
    ) -> Direction | None:
        """Return the direction assigned to a key."""

        return self.DIRECTION_KEYS.get(key)

    def is_start_key(self, key: int) -> bool:
        """Return whether the start key was pressed."""

        return key in {
            pygame.K_SPACE,
            pygame.K_RETURN,
            pygame.K_KP_ENTER,
        }

    def is_pause_key(self, key: int) -> bool:
        """Return whether the pause key was pressed."""

        return key in {
            pygame.K_ESCAPE,
            pygame.K_p,
        }

    def is_confirm_key(self, key: int) -> bool:
        """Return whether a confirmation key was pressed."""

        return key in {
            pygame.K_RETURN,
            pygame.K_KP_ENTER,
            pygame.K_SPACE,
        }

    def is_back_key(self, key: int) -> bool:
        """Return whether a back key was pressed."""

        return key in {
            pygame.K_ESCAPE,
            pygame.K_BACKSPACE,
        }

    def is_up_key(self, key: int) -> bool:
        """Return whether an upward menu key was pressed."""

        return key in {
            pygame.K_UP,
            pygame.K_w,
        }

    def is_down_key(self, key: int) -> bool:
        """Return whether a downward menu key was pressed."""

        return key in {
            pygame.K_DOWN,
            pygame.K_s,
        }
