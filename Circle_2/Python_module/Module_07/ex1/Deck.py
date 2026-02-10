"""This module provides the `Deck` class for managing a collection of cards."""

from typing import List, Dict, Any
from .SpellCard import SpellCard
from .ArtifactCard import ArtifactCard
from ex0.Card import Card
import random


class Deck:
    """Represents a deck of cards."""

    def __init__(self, deck: list) -> None:
        """
        Initialize a Deck instance.

        Args:
            deck: An unused parameter.
        """
        self.deck: List[Card] = []

    def add_card(self, card: Card) -> None:
        """
        Add a card to the deck.

        Args:
            card: The card to add.
        """
        self.deck.append(card)

    def remove_card(self, card_name: str) -> bool:
        """
        Remove a card from the deck by name.

        Args:
            card_name: The name of the card to remove.

        Returns:
            True if the card was removed, False otherwise.
        """
        for i, card in enumerate(self.deck):
            if card.name == card_name:
                self.deck.pop(i)
                return True
        return False

    def shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.deck)

    def draw_card(self) -> Card:
        """
        Draw a card from the top of the deck.

        Returns:
            The card drawn, or None if the deck is empty.
        """
        if self.deck:
            return self.deck.pop(0)
        return None

    def get_deck_stats(self) -> Dict[str, any]:
        """
        Get statistics about the deck.

        Returns:
            A dictionary with deck statistics.
        """
        if not self.deck:
            return {'total_cards': 0}

        total_cost: int = sum(card.cost for card in self.deck)
        avg: float = total_cost / len(self.deck)
        stats: dict[Any] = {
            'total_cards': len(self.deck),
            'creatures': sum(
                1 for card in self.deck if hasattr(card, 'attack')),
            'spells': sum(
                1 for card in self.deck if isinstance(card, SpellCard)),
            'artifacts': sum(
                1 for card in self.deck if isinstance(card, ArtifactCard)),
            'avg_cost': f"{avg:.2f}"
        }
        return stats
