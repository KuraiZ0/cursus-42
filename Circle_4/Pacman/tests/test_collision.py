"""Tests for collision helpers."""

from src.entities.entity import Entity, Position
from src.game.collision import (
    can_enter_position,
    entities_collide,
    positions_collide,
)
from src.game.maze import Maze


def test_identical_positions_collide() -> None:
    """Test collision between identical positions."""

    first = Position(row=2, column=3)
    second = Position(row=2, column=3)

    assert positions_collide(first, second)


def test_different_positions_do_not_collide() -> None:
    """Test positions with different coordinates."""

    first = Position(row=2, column=3)
    second = Position(row=3, column=2)

    assert not positions_collide(first, second)


def test_entities_collide_on_same_tile() -> None:
    """Test two entities occupying the same tile."""

    first = Entity(
        position=Position(row=1, column=1)
    )
    second = Entity(
        position=Position(row=1, column=1)
    )

    assert entities_collide(first, second)


def test_entity_can_enter_corridor() -> None:
    """Test entering a corridor tile."""

    maze = Maze.from_integer_grid(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
    )

    assert can_enter_position(
        maze,
        Position(row=1, column=1),
    )


def test_entity_cannot_enter_wall() -> None:
    """Test rejection of a wall tile."""

    maze = Maze.from_integer_grid(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
    )

    assert not can_enter_position(
        maze,
        Position(row=0, column=0),
    )


def test_entity_cannot_leave_maze() -> None:
    """Test rejection of an external position."""

    maze = Maze.from_integer_grid(
        [
            [1, 1],
            [1, 1],
        ]
    )

    assert not can_enter_position(
        maze,
        Position(row=-1, column=0),
    )
