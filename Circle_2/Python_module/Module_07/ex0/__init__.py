"""This package provides the base classes for a card game."""


from .Card import Card
from .CreatureCard import CreatureCard

__all__: list[str] = [
    "CreatureCard",
    "Card"
]
