"""Adapter for the assigned A-Maze-ing package (``mazegenerator``)."""

import importlib
from typing import Any

from src.exceptions import MazeError
from src.game.maze import Maze

NORTH_WALL = 1
EAST_WALL = 2
SOUTH_WALL = 4
WEST_WALL = 8
ISOLATED_CELL = 15


class MazeAdapter:
    """Convert the wall-based maze of ``mazegenerator`` into a tile grid.

    The external package describes every cell with four wall bits. Pac-Man
    needs a grid where each tile is either a wall or a corridor, so a maze of
    ``width x height`` cells becomes a grid of ``(2 * height + 1)`` rows and
    ``(2 * width + 1)`` columns: cells sit on odd coordinates and the tiles
    between two cells are corridors only when the wall between them is open.
    """

    def __init__(self, package_name: str = "mazegenerator") -> None:
        """Initialise the adapter with the name of the package to use."""

        self.package_name = package_name

    def generate(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> Maze:
        """Generate an imperfect maze and convert it to a ``Maze``."""

        generator_class = self._load_generator_class()

        try:
            generator = generator_class(
                size=(width, height),
                perfect=False,
                seed=max(1, seed),
            )
            cells = self._validate_cells(generator.maze, width, height)
            return Maze.from_integer_grid(self.cells_to_tiles(cells))

        except MazeError:
            raise

        except Exception as error:
            raise MazeError(
                f"The external maze generator failed: {error}"
            ) from error

    def _load_generator_class(self) -> Any:
        """Import the package and return its ``MazeGenerator`` class."""

        try:
            module = importlib.import_module(self.package_name)
        except ImportError as error:
            raise MazeError(
                "Unable to import the assigned A-Maze-ing package "
                f"'{self.package_name}'. Run 'make install'."
            ) from error

        generator_class = getattr(module, "MazeGenerator", None)

        if not callable(generator_class):
            raise MazeError(
                f"'{self.package_name}' does not provide MazeGenerator."
            )

        return generator_class

    @staticmethod
    def _validate_cells(
        raw_cells: Any,
        width: int,
        height: int,
    ) -> list[list[int]]:
        """Check that the generated cells form a ``height x width`` grid."""

        if (
            not isinstance(raw_cells, list)
            or len(raw_cells) != height
        ):
            raise MazeError("The generated maze has an invalid height.")

        cells: list[list[int]] = []

        for raw_row in raw_cells:
            if not isinstance(raw_row, list) or len(raw_row) != width:
                raise MazeError("The generated maze has an invalid row.")

            if not all(
                isinstance(cell, int) and not isinstance(cell, bool)
                for cell in raw_row
            ):
                raise MazeError("The generated maze has an invalid cell.")

            cells.append(list(raw_row))

        return cells

    @staticmethod
    def cells_to_tiles(cells: list[list[int]]) -> list[list[int]]:
        """Expand wall-bit cells into a grid of 0 (wall) and 1 (corridor)."""

        height = len(cells)
        width = len(cells[0])
        grid = [[0] * (2 * width + 1) for _ in range(2 * height + 1)]

        for y in range(height):
            for x in range(width):
                cell = cells[y][x]

                if cell & 0xF == ISOLATED_CELL:
                    continue

                grid[2 * y + 1][2 * x + 1] = 1

                if (
                    x + 1 < width
                    and not cell & EAST_WALL
                    and not cells[y][x + 1] & WEST_WALL
                    and cells[y][x + 1] & 0xF != ISOLATED_CELL
                ):
                    grid[2 * y + 1][2 * x + 2] = 1

                if (
                    y + 1 < height
                    and not cell & SOUTH_WALL
                    and not cells[y + 1][x] & NORTH_WALL
                    and cells[y + 1][x] & 0xF != ISOLATED_CELL
                ):
                    grid[2 * y + 2][2 * x + 1] = 1

        return grid
