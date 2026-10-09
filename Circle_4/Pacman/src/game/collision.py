"""Collision helper functions."""

from src.entities.entity import Entity, Position
from src.game.maze import Maze


def positions_collide(
    first_position: Position,
    second_position: Position,
) -> bool:
    """Return whether two positions are identical."""

    return first_position == second_position


def entities_collide(
    first_entity: Entity,
    second_entity: Entity,
) -> bool:
    """Return whether two entities occupy the same position."""

    return positions_collide(
        first_entity.position,
        second_entity.position,
    )


def can_enter_position(
    maze: Maze,
    position: Position,
) -> bool:
    """Return whether an entity can enter a maze position."""

    return maze.is_walkable(position)


def can_entity_move(
    maze: Maze,
    entity: Entity,
    destination: Position,
) -> bool:
    """Return whether an entity may move to a destination."""

    if entity.position == destination:
        return False

    return can_enter_position(maze, destination)
