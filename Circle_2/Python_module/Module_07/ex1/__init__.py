"""This module provides the card game classes and the Deck class."""


from .ArtifactCard import ArtifactCard
from .Deck import Deck
from .SpellCard import SpellCard
from ex0.Card import Card
from ex0.CreatureCard import CreatureCard

__all__: list[str] = [
    "ArtifactCard",
    "Deck",
    "SpellCard",
    "Card",
    "CreatureCard"
]
