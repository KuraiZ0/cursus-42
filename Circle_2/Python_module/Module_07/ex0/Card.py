"""This module provides the abstract base class for cards."""

from abc import ABC, abstractmethod


class Card(ABC):
    """Represents an abstract base for a card."""

    def __init__(self, name: str, cost: int, rarity: str) -> None:
        """
        Initialize a Card instance.

        Args:
            name: The name of the card.
            cost: The mana cost of the card.
            rarity: The rarity of the card.
        """
        self.name = name
        self.cost = cost
        self.rarity = rarity

    @abstractmethod
    def play(self, game_state: dict) -> dict:
        """
        Play the card.

        This is an abstract method that must be implemented by subclasses.

        Args:
            game_stats: The current game statistics.

        Returns:
            The updated game statistics.
        """
        pass

    def get_card_info(self) -> dict:
        """
        Get the card's information.

        Returns:
            A dictionary containing the card's information.
        """
        return {
            "name": self.name,
            "cost": self.cost,
            "rarity": self.rarity,
            "type": "Creature"
        }

    def is_playable(self, available_mana: int) -> bool:
        """
        Check if the card is playable.

        Args:
            available_mana: The amount of mana available.

        Returns:
            True if the card is playable, False otherwise.
        """
        return available_mana >= self.cost
