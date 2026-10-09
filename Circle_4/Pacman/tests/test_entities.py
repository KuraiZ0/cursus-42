"""Tests for player, ghost and collectible entities."""

from src.entities.collectible import (
    Collectible,
    CollectibleType,
)
from src.entities.entity import (
    Direction,
    Entity,
    Position,
)
from src.entities.ghost import Ghost, GhostState
from src.entities.player import Player


def test_entity_movement() -> None:
    """Test movement in one direction."""

    entity = Entity(
        position=Position(row=2, column=2)
    )

    entity.move(Direction.RIGHT)

    assert entity.position == Position(
        row=2,
        column=3,
    )


def test_entity_reset_position() -> None:
    """Test resetting an entity to its start."""

    entity = Entity(
        position=Position(row=1, column=1)
    )

    entity.move(Direction.DOWN)
    entity.reset_position()

    assert entity.position == Position(
        row=1,
        column=1,
    )


def test_player_loses_life() -> None:
    """Test normal player life loss."""

    player = Player(
        position=Position(row=1, column=1),
        lives=3,
    )

    is_alive = player.lose_life()

    assert is_alive
    assert player.lives == 2


def test_invincible_player_keeps_lives() -> None:
    """Test the invincibility cheat."""

    player = Player(
        position=Position(row=1, column=1),
        lives=3,
    )

    player.set_invincible(True)
    player.lose_life()

    assert player.lives == 3


def test_player_game_over() -> None:
    """Test losing the player's final life."""

    player = Player(
        position=Position(row=1, column=1),
        lives=1,
    )

    is_alive = player.lose_life()

    assert not is_alive
    assert player.lives == 0


def test_player_add_life() -> None:
    """Test the extra-life cheat."""

    player = Player(
        position=Position(row=1, column=1),
        lives=3,
    )

    player.add_life()

    assert player.lives == 4


def test_ghost_becomes_frightened() -> None:
    """Test frightened ghost state."""

    position = Position(row=1, column=1)

    ghost = Ghost(
        name="Blinky",
        position=position,
        corner=position,
    )

    ghost.frighten(5.0)

    assert ghost.is_edible
    assert ghost.state == GhostState.FRIGHTENED


def test_frightened_ghost_returns_to_chase() -> None:
    """Test expiration of frightened mode."""

    position = Position(row=1, column=1)

    ghost = Ghost(
        name="Pinky",
        position=position,
        corner=position,
    )

    ghost.frighten(2.0)
    ghost.update(2.5)

    assert not ghost.is_edible
    assert ghost.state == GhostState.CHASE


def test_eaten_ghost_respawns() -> None:
    """Test ghost respawn after being eaten."""

    corner = Position(row=1, column=1)

    ghost = Ghost(
        name="Inky",
        position=Position(row=5, column=5),
        corner=corner,
    )

    ghost.eat(3.0)
    ghost.update(4.0)

    assert ghost.position == corner
    assert ghost.state == GhostState.CHASE


def test_collectible_can_only_be_consumed_once() -> None:
    """Test collectible consumption."""

    collectible = Collectible(
        position=Position(row=2, column=2),
        collectible_type=CollectibleType.PACGUM,
        points=10,
    )

    first_score = collectible.consume()
    second_score = collectible.consume()

    assert first_score == 10
    assert second_score == 0
    assert collectible.eaten


def test_super_pacgum_type() -> None:
    """Test super-pacgum identification."""

    collectible = Collectible(
        position=Position(row=2, column=2),
        collectible_type=(
            CollectibleType.SUPER_PACGUM
        ),
        points=50,
    )

    assert collectible.is_super_pacgum
