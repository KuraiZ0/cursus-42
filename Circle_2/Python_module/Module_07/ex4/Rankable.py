"""
This module defines the Rankable abstract base class.

It provides an interface for objects that can be ranked in a
competitive system.
"""
from abc import ABC, abstractmethod


class Rankable(ABC):
    """Interface for objects that can be ranked in a competitive system."""

    @abstractmethod
    def calculate_rating(self) -> int:
        """
        Calculate and return the current rating.

        Returns:
            int: The current rating.
        """
        pass

    @abstractmethod
    def update_wins(self, wins: int) -> None:
        """
        Update stats based on wins.

        Args:
            wins (int): The number of wins to add.
        """
        pass

    @abstractmethod
    def update_losses(self, losses: int) -> None:
        """
        Update stats based on losses.

        Args:
            losses (int): The number of losses to add.
        """
        pass

    @abstractmethod
    def get_rank_info(self) -> dict:
        """
        Return ranking details.

        Returns:
            dict: A dictionary containing the rank information.
        """
        pass
