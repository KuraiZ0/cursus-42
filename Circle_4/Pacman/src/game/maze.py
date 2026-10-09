"""Internal maze representation."""

from enum import Enum
from typing import Iterable

from src.entities.entity import Position
from src.exceptions import MazeError


class Tile(Enum):
    """Represent one maze tile."""

    WALL = 0
    CORRIDOR = 1


class Maze:
    """Represent the walls and corridors of a level."""

    def __init__(self, grid: list[list[Tile]]) -> None:
        """Initialise and validate the maze."""

        if not grid:
            raise MazeError("The maze grid cannot be empty.")

        first_width = len(grid[0])

        if first_width == 0:
            raise MazeError("The maze rows cannot be empty.")

        if any(len(row) != first_width for row in grid):
            raise MazeError("All maze rows must have the same width.")

        self._grid = grid
        self.height = len(grid)
        self.width = first_width

    @classmethod
    def from_integer_grid(
        cls,
        grid: Iterable[Iterable[int]],
    ) -> "Maze":
        """Create a maze from zero and one integer values."""

        converted_grid: list[list[Tile]] = []

        for row in grid:
            converted_row: list[Tile] = []

            for value in row:
                if value == 0:
                    converted_row.append(Tile.WALL)
                elif value == 1:
                    converted_row.append(Tile.CORRIDOR)
                else:
                    raise MazeError(
                        f"Unsupported maze tile value: {value}"
                    )

            converted_grid.append(converted_row)

        return cls(converted_grid)

    def is_inside(self, position: Position) -> bool:
        """Return whether a position is inside the maze."""

        return (
            0 <= position.row < self.height
            and 0 <= position.column < self.width
        )

    def tile_at(self, position: Position) -> Tile:
        """Return the tile located at a position."""

        if not self.is_inside(position):
            raise MazeError(
                "Cannot access a position outside the maze."
            )

        return self._grid[position.row][position.column]

    def is_walkable(self, position: Position) -> bool:
        """Return whether a position is a corridor."""

        if not self.is_inside(position):
            return False

        return self.tile_at(position) == Tile.CORRIDOR

    def corridor_positions(self) -> list[Position]:
        """Return every corridor position in the maze."""

        positions: list[Position] = []

        for row_index, row in enumerate(self._grid):
            for column_index, tile in enumerate(row):
                if tile == Tile.CORRIDOR:
                    positions.append(
                        Position(
                            row=row_index,
                            column=column_index,
                        )
                    )

        return positions

    def find_nearest_corridor(
        self,
        target: Position,
    ) -> Position:
        """Return the corridor nearest to a target position."""

        corridors = self.corridor_positions()

        if not corridors:
            raise MazeError("The maze contains no corridor.")

        return min(
            corridors,
            key=lambda position: (
                abs(position.row - target.row)
                + abs(position.column - target.column)
            ),
        )

    def center_position(self) -> Position:
        """Return the corridor nearest to the maze centre."""

        target = Position(
            row=self.height // 2,
            column=self.width // 2,
        )

        return self.find_nearest_corridor(target)

    def corner_positions(self) -> tuple[Position, ...]:
        """Return accessible positions near all four corners."""

        targets = (
            Position(row=0, column=0),
            Position(row=0, column=self.width - 1),
            Position(row=self.height - 1, column=0),
            Position(
                row=self.height - 1,
                column=self.width - 1,
            ),
        )

        corners: list[Position] = []

        for target in targets:
            position = self.find_nearest_corridor(target)

            if position not in corners:
                corners.append(position)

        return tuple(corners)
