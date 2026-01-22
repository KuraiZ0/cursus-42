"""Card factory."""

from abc import ABC, abstractmethod
from ex0.Card import Card


class CardFactory(ABC):
    """
    Abstract base class for creating cards and themed decks.

    This factory provides an interface for generating different types of cards
    (Creature, Spell, Artifact) and creating pre-defined themed decks.
    """

    @abstractmethod
    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        """
        Create a new Creature card.

        Args:
            name_or_power (str | int | None):The name or power of the creature.

        Returns:
            Card: A new Creature card instance.
        """
        pass

    @abstractmethod
    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        """
        Create a new Spell card.

        Args:
            name_or_power (str | int | None): The name or power of the spell.

        Returns:
            Card: A new Spell card instance.
        """
        pass

    @abstractmethod
    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        """
        Create a new Artifact card.

        Args:
            name_or_power (str | int | None):The name or power of the artifact.

        Returns:
            Card: A new Artifact card instance.
        """
        pass

    @abstractmethod
    def create_themed_deck(self, size: int) -> dict:
        """
        Create a themed deck of cards.

        Args:
            size (int): The number of cards in the deck.

        Returns:
            dict: A dictionary representing the themed deck.
        """
        pass

    @abstractmethod
    def get_supported_types(self) -> dict:
        """
        Get a dictionary of supported card types.

        Returns:
            dict: A dictionary of supported card types.
        """
        pass
