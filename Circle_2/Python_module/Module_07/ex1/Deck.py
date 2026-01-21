"""Base class for creating a deck."""
from typing import List, Dict
from .SpellCard import SpellCard
from .ArtifactCard import ArtifactCard
from ex0.Card import Card
import random


class Deck:
    def __init__(self, deck: list):
        self.deck: List[Card] = []

    def add_card(self, card: Card):
        self.deck.append(card)

    def remove_card(self, card_name: str) -> bool:
        for i, card in enumerate(self.deck):
            if card.name == card_name:
                self.deck.pop(i)
                return True
        return False

    def shuffle(self) -> None:
        random.shuffle(self.deck)

    def draw_card(self) -> Card:
        if self.deck:
            return self.deck.pop(0)
        return None

    def get_deck_stats(self) -> Dict[str, any]:
        if not self.deck:
            return {'total_cards': 0}

        total_cost = sum(card.cost for card in self.deck)
        avg = total_cost / len(self.deck)
        stats = {
            'total_cards': len(self.deck),
            'avg_cost': f"{avg:.2f}",
            'creatures': sum(
                1 for card in self.deck if hasattr(card, 'attack')),
            'spells': sum(
                1 for card in self.deck if isinstance(card, SpellCard)),
            'artifacts': sum(
                1 for card in self.deck if isinstance(card, ArtifactCard))
        }
        return stats
