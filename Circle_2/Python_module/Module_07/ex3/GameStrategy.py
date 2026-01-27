"""
Defines the abstract base class for all game strategies.

This module provides the `GameStrategy` interface, which outlines the
methods required to implement a valid game strategy.
"""
from abc import ABC, abstractmethod


class GameStrategy(ABC):
    """
    Abstract base class for defining game strategies.

    This class provides an interface for executing a turn, retrieving the
    strategy's name, and prioritizing targets.
    """

    @abstractmethod
    def execute_turn(self, hand: list, battlefield: list) -> dict:
        """
        Execute a single game turn based on the implemented strategy.

        Args:
            hand (list): The cards in the player's hand.
            battlefield (list): The cards on the player's battlefield.

        Returns:
            dict: A dictionary of actions taken during the turn.
        """
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """
        Return the name of the strategy.

        Returns:
            str: The name of the strategy.
        """
        pass

    @abstractmethod
    def prioritize_targets(self, available_targets: list) -> list:
        """
        Prioritize targets based on the strategy.

        Args:
            available_targets (list): A list of potential targets.

        Returns:
            list: A prioritized list of targets.
        """
        pass
