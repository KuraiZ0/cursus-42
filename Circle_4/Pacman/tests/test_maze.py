"""Tests for the internal maze representation."""

import pytest

from src.entities.entity import Position
from src.exceptions import MazeError
from src.game.maze import Maze, Tile


def create_test_maze() -> Maze:
    """Create a small maze used by tests."""

    return Maze.from_integer_grid(
        [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
    )


def test_maze_dimensions() -> None:
    """Test maze width and height."""

    maze = create_test_maze()

    assert maze.width == 5
    assert maze.height == 5


def test_maze_wall_tile() -> None:
    """Test reading a wall tile."""

    maze = create_test_maze()

    assert maze.tile_at(
        Position(row=0, column=0)
    ) == Tile.WALL


def test_maze_corridor_tile() -> None:
    """Test reading a corridor tile."""

    maze = create_test_maze()

    assert maze.is_walkable(
        Position(row=2, column=2)
    )


def test_position_outside_maze_is_not_walkable() -> None:
    """Test positions outside the maze."""

    maze = create_test_maze()

    assert not maze.is_walkable(
        Position(row=-1, column=0)
    )


def test_center_position_is_walkable() -> None:
    """Test the selected centre position."""

    maze = create_test_maze()
    center = maze.center_position()

    assert maze.is_walkable(center)


def test_four_corner_positions_are_found() -> None:
    """Test accessible positions near maze corners."""

    maze = create_test_maze()
    corners = maze.corner_positions()

    assert len(corners) == 4

    for corner in corners:
        assert maze.is_walkable(corner)


def test_invalid_tile_value_raises_error() -> None:
    """Test rejection of an unsupported tile."""

    with pytest.raises(MazeError):
        Maze.from_integer_grid(
            [
                [0, 0],
                [0, 9],
            ]
        )


def test_irregular_grid_raises_error() -> None:
    """Test rejection of rows with different sizes."""

    with pytest.raises(MazeError):
        Maze.from_integer_grid(
            [
                [0, 0, 0],
                [0, 1],
            ]
        )
