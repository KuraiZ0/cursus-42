"""Player entity implementation."""

from src.entities.entity import Direction, Entity, Position


class Player(Entity):
    """Represent the Pac-Man player."""

    NORMAL_SPEED = 1.0
    BOOSTED_SPEED = 2.0

    def __init__(
        self,
        position: Position,
        lives: int,
        speed: float = NORMAL_SPEED,
    ) -> None:
        """Initialise the player."""

        super().__init__(position=position, speed=speed)

        self.lives = lives
        self.direction = Direction.LEFT
        self.requested_direction = Direction.LEFT
        self.invincible = False
        self.speed_boosted = False

    def request_move(self, direction: Direction) -> None:
        """Store the direction requested by the player."""

        self.requested_direction = direction

    def change_direction(self, direction: Direction) -> None:
        """Change the current movement direction."""

        self.direction = direction

    def lose_life(self) -> bool:
        """Remove one life and return whether the player is alive."""

        if self.invincible:
            return True

        if self.lives > 0:
            self.lives -= 1

        return self.lives > 0

    def add_life(self, amount: int = 1) -> None:
        """Add lives to the player."""

        if amount > 0:
            self.lives += amount

    def respawn(self) -> None:
        """Respawn the player at the starting position."""

        self.reset_position()
        self.direction = Direction.LEFT
        self.requested_direction = Direction.LEFT

    def set_invincible(self, enabled: bool) -> None:
        """Enable or disable player invincibility."""

        self.invincible = enabled

    def toggle_speed_boost(self) -> None:
        """Toggle the player speed cheat."""

        self.speed_boosted = not self.speed_boosted

        if self.speed_boosted:
            self.speed = self.BOOSTED_SPEED
        else:
            self.speed = self.NORMAL_SPEED
