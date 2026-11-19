"""Ghost entity implementation."""

from enum import Enum, auto

from src.entities.entity import Entity, Position


class GhostState(Enum):
    """Represent the current state of a ghost."""

    CHASE = auto()
    FRIGHTENED = auto()
    EATEN = auto()
    FROZEN = auto()


class Ghost(Entity):
    """Represent an autonomous Pac-Man ghost."""

    def __init__(
        self,
        name: str,
        position: Position,
        corner: Position,
        speed: float = 1.0,
    ) -> None:
        """Initialise a ghost."""

        super().__init__(position=position, speed=speed)

        self.name = name
        self.corner = corner
        self.state = GhostState.CHASE
        self.frightened_time = 0.0
        self.respawn_time = 0.0

    @property
    def is_edible(self) -> bool:
        """Return whether the ghost can be eaten."""

        return self.state == GhostState.FRIGHTENED

    @property
    def can_move(self) -> bool:
        """Return whether the ghost can currently move."""

        return self.state not in {
            GhostState.EATEN,
            GhostState.FROZEN,
        }

    def frighten(self, duration: float) -> None:
        """Make the ghost edible for a limited duration."""

        if self.state != GhostState.EATEN:
            self.state = GhostState.FRIGHTENED
            self.frightened_time = max(0.0, duration)

    def eat(self, respawn_delay: float) -> None:
        """Mark the ghost as eaten."""

        self.state = GhostState.EATEN
        self.respawn_time = max(0.0, respawn_delay)

    def freeze(self) -> None:
        """Freeze the ghost."""

        if self.state != GhostState.EATEN:
            self.state = GhostState.FROZEN

    def unfreeze(self) -> None:
        """Restore the ghost chase state."""

        if self.state == GhostState.FROZEN:
            self.state = GhostState.CHASE

    def update(self, delta_time: float) -> None:
        """Update ghost timers and states."""

        if self.state == GhostState.FRIGHTENED:
            self.frightened_time -= delta_time

            if self.frightened_time <= 0.0:
                self.frightened_time = 0.0
                self.state = GhostState.CHASE

        if self.state == GhostState.EATEN:
            self.respawn_time -= delta_time

            if self.respawn_time <= 0.0:
                self.respawn_time = 0.0
                self.position = self.corner
                self.state = GhostState.CHASE

    def respawn(self) -> None:
        """Immediately respawn the ghost in its corner."""

        self.position = self.corner
        self.state = GhostState.CHASE
        self.frightened_time = 0.0
        self.respawn_time = 0.0
