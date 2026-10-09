"""Core Pac-Man game logic."""

import random
from collections import deque
from enum import Enum, auto

from src.config import GameConfig
from src.entities.collectible import CollectibleType
from src.entities.entity import Direction, Position
from src.entities.ghost import Ghost, GhostState
from src.entities.player import Player
from src.exceptions import MazeError
from src.game.collision import entities_collide
from src.game.level import Level
from src.game.maze_adapter import MazeAdapter


class GameStatus(Enum):
    """Represent the current game status."""

    READY = auto()
    RUNNING = auto()
    PAUSED = auto()
    WON = auto()
    LOST = auto()


class Game:
    """Control the complete Pac-Man game state."""

    CLYDE_SAFE_DISTANCE = 8
    PINKY_LOOKAHEAD = 4

    def __init__(
        self,
        config: GameConfig,
        maze_adapter: MazeAdapter | None = None,
    ) -> None:
        """Initialise the game controller."""

        self.config = config
        self.maze_adapter = maze_adapter or MazeAdapter()
        # Only the first maze uses the configured seed: every other level
        # (and every ghost decision) must differ from one run to the next.
        self.random = random.Random()

        self.status = GameStatus.READY
        self.score = 0
        self.level_index = 0

        self.level: Level | None = None
        self.player: Player | None = None
        self.ghosts: list[Ghost] = []

        self.ghost_move_timer = 0.0
        self.ghost_move_interval = 0.25
        self.ghosts_frozen = False

    def start(self) -> None:
        """Start a new game."""

        self.status = GameStatus.RUNNING
        self.score = 0
        self.level_index = 0
        self.level = None
        self.player = None
        self.ghosts = []
        self.ghosts_frozen = False
        self.ghost_move_timer = 0.0

        self._load_level()

    def _load_level(self) -> None:
        """Generate and load the current level."""

        if self.level_index >= len(self.config.levels):
            self.status = GameStatus.WON
            return

        level_config = self.config.levels[self.level_index]
        seed = self._get_level_seed()

        maze = self.maze_adapter.generate(
            width=level_config.width,
            height=level_config.height,
            seed=seed,
        )

        self.level = Level(
            number=self.level_index + 1,
            maze=maze,
            time_limit=self.config.level_max_time,
            points_per_pacgum=(
                self.config.points_per_pacgum
            ),
            points_per_super_pacgum=(
                self.config.points_per_super_pacgum
            ),
        )

        if self.player is None:
            self.player = Player(
                position=self.level.player_start,
                lives=self.config.lives,
            )
        else:
            self.player.position = self.level.player_start
            self.player.start_position = self.level.player_start
            self.player.respawn()

        self._create_ghosts()
        self._consume_player_position()

    def _get_level_seed(self) -> int:
        """Return the maze seed for the current level."""

        if self.level_index == 0:
            return self.config.seed

        return self.random.randint(1, 2_147_483_647)

    def _create_ghosts(self) -> None:
        """Create four ghosts near the maze corners."""

        if self.level is None:
            raise MazeError(
                "A level must exist before creating ghosts."
            )

        corners = self.level.ghost_starts

        if not corners:
            raise MazeError(
                "No valid ghost position was found."
            )

        names = (
            "Blinky",
            "Pinky",
            "Inky",
            "Clyde",
        )

        self.ghosts = []

        for index, name in enumerate(names):
            corner = corners[index % len(corners)]

            self.ghosts.append(
                Ghost(
                    name=name,
                    position=corner,
                    corner=corner,
                )
            )

    def request_player_direction(
        self,
        direction: Direction,
    ) -> None:
        """Store the direction requested by the player."""

        if self.player is not None:
            self.player.request_move(direction)

    def move_player(self) -> None:
        """Move the player by one maze tile."""

        if (
            self.status != GameStatus.RUNNING
            or self.level is None
            or self.player is None
        ):
            return

        requested_position = self.player.next_position(
            self.player.requested_direction
        )

        if self.level.maze.is_walkable(requested_position):
            self.player.change_direction(
                self.player.requested_direction
            )

        next_position = self.player.next_position(
            self.player.direction
        )

        if self.level.maze.is_walkable(next_position):
            self.player.move(self.player.direction)

        self._consume_player_position()
        self._handle_collisions()
        self._check_level_completion()

    def update(self, delta_time: float) -> None:
        """Update timers, ghosts and game progression."""

        if (
            self.status != GameStatus.RUNNING
            or self.level is None
            or self.player is None
        ):
            return

        self.level.update_timer(delta_time)

        for ghost in self.ghosts:
            ghost.update(delta_time)

        if self.level.is_time_over():
            self._handle_player_hit()
            return

        if not self.ghosts_frozen:
            self.ghost_move_timer += delta_time

            if (
                self.ghost_move_timer
                >= self.ghost_move_interval
            ):
                self.ghost_move_timer = 0.0
                self._move_ghosts()

        self._handle_collisions()
        self._check_level_completion()

    def _move_ghosts(self) -> None:
        """Move every active ghost once."""

        if self.level is None or self.player is None:
            return

        player_distances = self._distance_map(self.player.position)

        for ghost in self.ghosts:
            if not ghost.can_move:
                continue

            directions = self._available_directions(
                ghost.position
            )

            if not directions:
                continue

            direction = self._choose_ghost_direction(
                ghost=ghost,
                directions=directions,
                player_distances=player_distances,
            )

            ghost.move(direction)
            ghost.last_direction = direction

    def _distance_map(
        self,
        target: Position,
    ) -> dict[Position, int]:
        """Return the walking distance from the target to every tile."""

        distances: dict[Position, int] = {target: 0}

        if self.level is None:
            return distances

        queue: deque[Position] = deque([target])

        while queue:
            current = queue.popleft()

            for direction in self._available_directions(current):
                neighbour = Position(
                    row=current.row + direction.row_offset,
                    column=current.column + direction.column_offset,
                )

                if neighbour not in distances:
                    distances[neighbour] = distances[current] + 1
                    queue.append(neighbour)

        return distances

    def _available_directions(
        self,
        position: Position,
    ) -> list[Direction]:
        """Return walkable directions around a position."""

        if self.level is None:
            return []

        directions: list[Direction] = []

        for direction in Direction:
            destination = Position(
                row=(
                    position.row
                    + direction.row_offset
                ),
                column=(
                    position.column
                    + direction.column_offset
                ),
            )

            if self.level.maze.is_walkable(destination):
                directions.append(direction)

        return directions

    def _choose_ghost_direction(
        self,
        ghost: Ghost,
        directions: list[Direction],
        player_distances: dict[Position, int],
    ) -> Direction:
        """Choose a chase or escape direction.

        Edible ghosts run away from the player. Otherwise each ghost follows
        the shortest path to its own target:

        * Blinky chases the player directly.
        * Pinky ambushes a few tiles ahead of the player.
        * Inky is unpredictable: it often moves at random.
        * Clyde chases from afar but retreats to his corner when close.
        """

        # Never turn back on the same tile unless it is a dead end.
        forward = [
            direction
            for direction in directions
            if ghost.last_direction is None
            or direction != ghost.last_direction.opposite
        ]
        candidates = forward or directions

        if ghost.state == GhostState.FRIGHTENED:
            return self._best_direction(
                ghost, candidates, player_distances, flee=True
            )

        if ghost.name == "Inky" and self.random.random() < 0.4:
            return self.random.choice(candidates)

        if ghost.name == "Pinky":
            target_distances = self._distance_map(
                self._ambush_target()
            )
        elif (
            ghost.name == "Clyde"
            and player_distances.get(ghost.position, 0)
            <= self.CLYDE_SAFE_DISTANCE
        ):
            target_distances = self._distance_map(ghost.corner)
        else:
            target_distances = player_distances

        return self._best_direction(
            ghost, candidates, target_distances, flee=False
        )

    def _best_direction(
        self,
        ghost: Ghost,
        directions: list[Direction],
        distances: dict[Position, int],
        flee: bool,
    ) -> Direction:
        """Pick the direction closest to (or farthest from) a target."""

        unreachable = 1_000_000
        scored = [
            (
                distances.get(ghost.next_position(direction), unreachable),
                direction,
            )
            for direction in directions
        ]

        if flee:
            best = max(score for score, _ in scored)
        else:
            best = min(score for score, _ in scored)

        return self.random.choice(
            [direction for score, direction in scored if score == best]
        )

    def _ambush_target(self) -> Position:
        """Return the tile a few steps ahead of the player."""

        if self.player is None or self.level is None:
            return Position(row=0, column=0)

        target = self.player.position
        direction = self.player.direction

        for _ in range(self.PINKY_LOOKAHEAD):
            ahead = Position(
                row=target.row + direction.row_offset,
                column=target.column + direction.column_offset,
            )

            if not self.level.maze.is_walkable(ahead):
                break

            target = ahead

        return target

    def _consume_player_position(self) -> None:
        """Consume the collectible under the player."""

        if self.level is None or self.player is None:
            return

        collectible = self.level.consume_at(
            self.player.position
        )

        if collectible is None:
            return

        self.score += collectible.points

        if (
            collectible.collectible_type
            == CollectibleType.SUPER_PACGUM
        ):
            for ghost in self.ghosts:
                ghost.frighten(
                    self.config.super_pacgum_duration
                )

    def _handle_collisions(self) -> None:
        """Resolve player and ghost collisions."""

        if self.player is None:
            return

        for ghost in self.ghosts:
            if not entities_collide(
                self.player,
                ghost,
            ):
                continue

            if ghost.is_edible:
                ghost.eat(
                    self.config.ghost_respawn_time
                )
                self.score += (
                    self.config.points_per_ghost
                )
            elif ghost.state != GhostState.EATEN:
                self._handle_player_hit()
                return

    def _handle_player_hit(self) -> None:
        """Remove one life and reset positions."""

        if self.player is None or self.level is None:
            return

        is_alive = self.player.lose_life()

        if not is_alive:
            self.status = GameStatus.LOST
            return

        self.player.respawn()
        self.level.reset_timer()

        for ghost in self.ghosts:
            ghost.respawn()

    def _check_level_completion(self) -> None:
        """Load the next level when all pacgums are eaten."""

        if self.level is None:
            return

        if not self.level.is_complete():
            return

        self.level_index += 1
        self._load_level()

    def toggle_pause(self) -> None:
        """Pause or resume the game."""

        if self.status == GameStatus.RUNNING:
            self.status = GameStatus.PAUSED
        elif self.status == GameStatus.PAUSED:
            self.status = GameStatus.RUNNING

    def toggle_invincibility(self) -> None:
        """Toggle the player invincibility cheat."""

        if self.player is not None:
            self.player.set_invincible(
                not self.player.invincible
            )

    def toggle_ghost_freeze(self) -> None:
        """Toggle the ghost freeze cheat."""

        self.ghosts_frozen = not self.ghosts_frozen

    def add_extra_life(self) -> None:
        """Add one player life."""

        if self.player is not None:
            self.player.add_life()

    def toggle_speed_boost(self) -> None:
        """Toggle the player speed cheat."""

        if self.player is not None:
            self.player.toggle_speed_boost()

    def skip_level(self) -> None:
        """Immediately move to the next level."""

        if self.status != GameStatus.RUNNING:
            return

        self.level_index += 1
        self._load_level()
