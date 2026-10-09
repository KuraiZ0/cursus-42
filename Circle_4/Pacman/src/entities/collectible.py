"""Pacgum and super-pacgum entities."""

from dataclasses import dataclass
from enum import Enum, auto

from src.entities.entity import Position


class CollectibleType(Enum):
    """Represent the different collectible types."""

    PACGUM = auto()
    SUPER_PACGUM = auto()


@dataclass
class Collectible:
    """Represent one collectible placed in the maze."""

    position: Position
    collectible_type: CollectibleType
    points: int
    eaten: bool = False

    @property
    def is_super_pacgum(self) -> bool:
        """Return whether this collectible is a super-pacgum."""

        return self.collectible_type == CollectibleType.SUPER_PACGUM

    def consume(self) -> int:
        """Consume the collectible and return its points."""

        if self.eaten:
            return 0

        self.eaten = True
        return self.points
