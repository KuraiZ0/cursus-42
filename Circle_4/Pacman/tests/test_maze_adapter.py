"""Tests for the adapter around the assigned maze generator package."""

from collections import deque

import pytest

from src.entities.entity import Position
from src.exceptions import MazeError
from src.game.maze_adapter import MazeAdapter


def test_cells_to_tiles_opens_only_open_walls() -> None:
    """A wall bit closes the passage between two cells."""

    # Two cells side by side: east wall of the first cell is open.
    tiles = MazeAdapter.cells_to_tiles([[1 | 4 | 8, 1 | 4 | 2]])

    assert tiles == [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ]


def test_cells_to_tiles_keeps_walls_closed() -> None:
    """Closed walls and isolated cells stay walls."""

    tiles = MazeAdapter.cells_to_tiles([[1 | 2 | 4 | 8, 15]])

    assert tiles == [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]


def test_generate_size_and_connectivity() -> None:
    """The real package gives a fully connected maze of 2n+1 tiles."""

    pytest.importorskip("mazegenerator")

    maze = MazeAdapter().generate(width=16, height=11, seed=42)

    assert maze.width == 33
    assert maze.height == 23

    corridors = set(maze.corridor_positions())
    start = maze.center_position()
    seen = {start}
    queue = deque([start])

    while queue:
        current = queue.popleft()

        for row, column in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbour = Position(
                current.row + row,
                current.column + column,
            )

            if neighbour in corridors and neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)

    assert seen == corridors


def test_generate_is_reproducible_with_a_seed() -> None:
    """The same seed gives the same maze."""

    pytest.importorskip("mazegenerator")

    first = MazeAdapter().generate(width=16, height=11, seed=42)
    second = MazeAdapter().generate(width=16, height=11, seed=42)

    assert first.corridor_positions() == second.corridor_positions()


def test_missing_package_raises_maze_error() -> None:
    """A missing package is reported as a MazeError."""

    with pytest.raises(MazeError):
        MazeAdapter(package_name="no_such_package").generate(16, 11, 42)
