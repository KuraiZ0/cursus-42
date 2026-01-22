"""Game engine."""

from .GameStrategy import GameStrategy
from .CardFactory import CardFactory
from typing import Any


class GameEngine:
    """Game engine class to manage game configurations and turn simulations."""

    def configure_engine(
            self, factory: CardFactory, strategy: GameStrategy) -> None:
        """
        Configure the game engine with a specific factory and strategy.

        Args:
            factory (CardFactory): The factory used to create cards.
            strategy (GameStrategy): The strategy used to play the turn.
        """
        self.factory = factory
        self.strategy = strategy

    def simulate_turn(self) -> dict:
        """
        Simulate a complete game turn.

        Generates a hand of cards using the factory, then executes
        the turn using the configured strategy.

        Returns:
            dict: The comprehensive report of the turn execution.
        """
        hand: list[Any] = [
            self.factory.create_creature("dragon"),
            self.factory.create_creature("goblin"),
            self.factory.create_spell("fireball"),
            self.factory.create_artifact("ring")
        ]

        battlefield: list[Any] = []

        result_turn: dict[Any] = self.strategy.execute_turn(hand, battlefield)
        return result_turn

    def get_engine_status(self) -> dict:
        """
        Get the current configuration of the game engine.

        Returns:
            dict: A dictionary containing the factory class name
            and the strategy name.
        """
        return {
            "factory_type": self.factory.__class__.__name__,
            "strategy_type": self.strategy.get_strategy_name()
        }
