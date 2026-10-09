"""Base entities and movement types."""

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Position:
    """Represent a position inside the maze."""

    row: int
    column: int


class Direction(Enum):
    """Represent one of the four movement directions."""

    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @property
    def opposite(self) -> "Direction":
        """Return the opposite direction."""

        return Direction((-self.value[0], -self.value[1]))

    @property
    def row_offset(self) -> int:
        """Return the vertical movement offset."""

        return self.value[0]

    @property
    def column_offset(self) -> int:
        """Return the horizontal movement offset."""

        return self.value[1]


class Entity:
    """Represent a movable game entity."""

    def __init__(
        self,
        position: Position,
        speed: float = 1.0,
    ) -> None:
        """Initialise the entity."""

        self.position = position
        self.start_position = position
        self.speed = speed

    def next_position(self, direction: Direction) -> Position:
        """Return the position reached after one movement."""

        return Position(
            row=self.position.row + direction.row_offset,
            column=self.position.column + direction.column_offset,
        )

    def move(self, direction: Direction) -> None:
        """Move the entity in the selected direction."""

        self.position = self.next_position(direction)

    def reset_position(self) -> None:
        """Move the entity back to its starting position."""

        self.position = self.start_position
