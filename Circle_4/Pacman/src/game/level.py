"""Pac-Man level implementation."""

from src.entities.collectible import (
    Collectible,
    CollectibleType,
)
from src.entities.entity import Position
from src.game.maze import Maze


class Level:
    """Represent one playable Pac-Man level."""

    def __init__(
        self,
        number: int,
        maze: Maze,
        time_limit: int,
        points_per_pacgum: int,
        points_per_super_pacgum: int,
    ) -> None:
        """Initialise the level."""

        self.number = number
        self.maze = maze
        self.time_limit = time_limit
        self.remaining_time = float(time_limit)

        self.points_per_pacgum = points_per_pacgum
        self.points_per_super_pacgum = (
            points_per_super_pacgum
        )

        self.player_start = maze.center_position()
        self.ghost_starts = maze.corner_positions()

        self.collectibles = self._create_collectibles()

    def _create_collectibles(
        self,
    ) -> dict[Position, Collectible]:
        """Create pacgums and super-pacgums."""

        collectibles: dict[Position, Collectible] = {}
        super_positions = set(self.ghost_starts)

        for position in self.maze.corridor_positions():
            if position == self.player_start:
                continue

            if position in super_positions:
                collectible = Collectible(
                    position=position,
                    collectible_type=(
                        CollectibleType.SUPER_PACGUM
                    ),
                    points=self.points_per_super_pacgum,
                )
            else:
                collectible = Collectible(
                    position=position,
                    collectible_type=CollectibleType.PACGUM,
                    points=self.points_per_pacgum,
                )

            collectibles[position] = collectible

        return collectibles

    def update_timer(self, delta_time: float) -> None:
        """Decrease the remaining level time."""

        self.remaining_time = max(
            0.0,
            self.remaining_time - delta_time,
        )

    def reset_timer(self) -> None:
        """Reset the level timer."""

        self.remaining_time = float(self.time_limit)

    def consume_at(
        self,
        position: Position,
    ) -> Collectible | None:
        """Consume and return a collectible at a position."""

        collectible = self.collectibles.get(position)

        if collectible is None or collectible.eaten:
            return None

        collectible.consume()
        return collectible

    def is_complete(self) -> bool:
        """Return whether every collectible was eaten."""

        return all(
            collectible.eaten
            for collectible in self.collectibles.values()
        )

    def is_time_over(self) -> bool:
        """Return whether the level timer reached zero."""

        return self.remaining_time <= 0.0

    def remaining_collectibles(self) -> int:
        """Return the number of uneaten collectibles."""

        return sum(
            not collectible.eaten
            for collectible in self.collectibles.values()
        )
