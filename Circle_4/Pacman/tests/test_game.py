"""Tests for the main game controller."""

from src.config import GameConfig, LevelConfig
from src.entities.entity import Position
from src.game.game import Game, GameStatus
from src.game.maze import Maze
from src.game.maze_adapter import MazeAdapter


class FakeMazeAdapter(MazeAdapter):
    """Return a predictable maze without an external package."""

    def generate(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> Maze:
        """Return a fixed test maze."""

        del width
        del height
        del seed

        return Maze.from_integer_grid(
            [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ]
        )


def create_config(
    level_count: int = 2,
) -> GameConfig:
    """Create a game configuration used by tests."""

    levels = tuple(
        LevelConfig(
            width=7,
            height=7,
        )
        for _ in range(level_count)
    )

    return GameConfig(
        highscore_filename="highscores.json",
        lives=3,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
        points_per_ghost=200,
        super_pacgum_duration=8.0,
        ghost_respawn_time=5.0,
        level_max_time=90,
        seed=42,
        levels=levels,
    )


def create_game(
    level_count: int = 2,
) -> Game:
    """Create a test game."""

    return Game(
        config=create_config(level_count),
        maze_adapter=FakeMazeAdapter(),
    )


def test_start_game() -> None:
    """Test creation of the first level."""

    game = create_game()

    game.start()

    assert game.status == GameStatus.RUNNING
    assert game.level is not None
    assert game.player is not None
    assert len(game.ghosts) == 4
    assert game.score == 0


def test_player_keeps_configured_lives() -> None:
    """Test initial player lives."""

    game = create_game()

    game.start()

    assert game.player is not None
    assert game.player.lives == 3


def test_player_collects_pacgum() -> None:
    """Test movement and score increase."""

    game = create_game()

    game.start()
    game.move_player()

    assert game.score == 10


def test_pause_and_resume() -> None:
    """Test game pause state."""

    game = create_game()

    game.start()
    game.toggle_pause()

    assert game.status.name == GameStatus.PAUSED.name

    game.toggle_pause()

    assert game.status.name == GameStatus.RUNNING.name


def test_invincibility_cheat() -> None:
    """Test invincibility activation."""

    game = create_game()

    game.start()
    game.toggle_invincibility()

    assert game.player is not None
    assert game.player.invincible


def test_extra_life_cheat() -> None:
    """Test adding a player life."""

    game = create_game()

    game.start()
    game.add_extra_life()

    assert game.player is not None
    assert game.player.lives == 4


def test_speed_boost_cheat() -> None:
    """Test player speed boost."""

    game = create_game()

    game.start()
    game.toggle_speed_boost()

    assert game.player is not None
    assert game.player.speed_boosted
    assert game.player.speed == 2.0


def test_ghost_freeze_cheat() -> None:
    """Test freezing all ghosts."""

    game = create_game()

    game.start()
    game.toggle_ghost_freeze()

    assert game.ghosts_frozen


def test_skip_last_level_wins_game() -> None:
    """Test level skip on the final level."""

    game = create_game(level_count=1)

    game.start()
    game.skip_level()

    assert game.status == GameStatus.WON


def test_ghosts_chase_player_by_shortest_path() -> None:
    """Chasing ghosts get closer to the player on every move."""

    game = create_game()
    game.start()

    assert game.player is not None
    ghost = game.ghosts[0]
    ghost.position = Position(row=1, column=1)
    game.player.position = Position(row=5, column=5)

    distances = game._distance_map(game.player.position)
    before = distances[ghost.position]

    game._move_ghosts()

    assert distances[ghost.position] == before - 1


def test_frightened_ghost_runs_away() -> None:
    """Edible ghosts increase their distance from the player."""

    game = create_game()
    game.start()

    assert game.player is not None
    ghost = game.ghosts[0]
    ghost.position = Position(row=3, column=3)
    ghost.frighten(5.0)
    game.player.position = Position(row=2, column=3)

    distances = game._distance_map(game.player.position)
    before = distances[ghost.position]

    game._move_ghosts()

    assert distances[ghost.position] == before + 1


def test_next_levels_are_not_reproducible() -> None:
    """Only the first level uses the configured seed."""

    first = create_game()
    second = create_game()
    first.level_index = 1
    second.level_index = 1

    seeds = {first._get_level_seed(), second._get_level_seed()}

    assert first.config.seed not in seeds
