"""Tests for Pac-Man levels."""

from src.entities.collectible import CollectibleType
from src.game.level import Level
from src.game.maze import Maze


def create_level() -> Level:
    """Create a small level used by tests."""

    maze = Maze.from_integer_grid(
        [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
    )

    return Level(
        number=1,
        maze=maze,
        time_limit=90,
        points_per_pacgum=10,
        points_per_super_pacgum=50,
    )


def test_level_initial_values() -> None:
    """Test the initial level state."""

    level = create_level()

    assert level.number == 1
    assert level.remaining_time == 90.0
    assert not level.is_complete()


def test_player_start_has_no_collectible() -> None:
    """Test that Pac-Man starts on an empty tile."""

    level = create_level()

    assert level.player_start not in level.collectibles


def test_super_pacgums_are_created() -> None:
    """Test creation of super-pacgums."""

    level = create_level()

    super_pacgums = [
        collectible
        for collectible in level.collectibles.values()
        if (
            collectible.collectible_type
            == CollectibleType.SUPER_PACGUM
        )
    ]

    assert len(super_pacgums) == 4


def test_consume_collectible() -> None:
    """Test consuming a collectible."""

    level = create_level()
    position = next(iter(level.collectibles))

    collectible = level.consume_at(position)

    assert collectible is not None
    assert collectible.eaten


def test_collectible_cannot_be_consumed_twice() -> None:
    """Test repeated collectible consumption."""

    level = create_level()
    position = next(iter(level.collectibles))

    first = level.consume_at(position)
    second = level.consume_at(position)

    assert first is not None
    assert second is None


def test_level_is_complete_after_all_collectibles() -> None:
    """Test level completion."""

    level = create_level()

    for position in level.collectibles:
        level.consume_at(position)

    assert level.is_complete()


def test_level_timer() -> None:
    """Test decreasing the level timer."""

    level = create_level()

    level.update_timer(15.0)

    assert level.remaining_time == 75.0


def test_level_timer_does_not_become_negative() -> None:
    """Test timer lower limit."""

    level = create_level()

    level.update_timer(200.0)

    assert level.remaining_time == 0.0
    assert level.is_time_over()
