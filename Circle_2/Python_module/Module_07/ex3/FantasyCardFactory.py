"""
This module provides a concrete implementation of the CardFactory.

A base class for creating fantasy-themed cards.
"""

from ex1 import ArtifactCard
from ex1 import SpellCard
from ex0 import CreatureCard
from ex0.Card import Card
from .CardFactory import CardFactory
from random import randint, choice
from typing import Any


class FantasyCardFactory(CardFactory):
    """
    A factory for creating fantasy-themed cards.

    This class implements the `CardFactory` interface to generate random
    creature, spell, and artifact cards with fantasy-themed attributes. It
    also provides a method for creating a themed deck of a specified size.
    """

    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        """
        Create a new Creature card with random attributes.

        Args:
            name_or_power (str | int | None): The name or power of the
                                              creature.

        Returns:
            Card: A new Creature card instance.
        """
        rarity_type: list[str] = ["Common", "Rare", "Epic", "Legendary"]
        cost: int = randint(0, 9)
        rarity: str = choice(rarity_type)
        attack: int = randint(0, 10)
        health: int = randint(0, 10)
        card: CreatureCard = CreatureCard(
            name_or_power, cost, rarity, attack, health)
        return card

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        """
        Create a new Spell card with random attributes.

        Args:
            name_or_power (str | int | None): The name or power of the spell.

        Returns:
            Card: A new Spell card instance.
        """
        rarity_type: list[str] = ["Common", "Rare", "Epic", "Legendary"]
        cost: int = randint(0, 9)
        rarity: str = choice(rarity_type)
        card: SpellCard = SpellCard(
            name_or_power, cost, rarity, f"{name_or_power} deal damage!")
        return card

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        """
        Create a new Artifact card with random attributes.

        Args:
            name_or_power (str | int | None): The name or power of the
                                              artifact.

        Returns:
            Card: A new Artifact card instance.
        """
        rarity_type: list[str] = ["Common", "Rare", "Epic", "Legendary"]
        cost: int = randint(0, 9)
        rarity: str = choice(rarity_type)
        durability: int = randint(0, 10)
        card: ArtifactCard = ArtifactCard(
            name_or_power, cost, rarity, durability, "+1 mana per turn")
        return card

    def create_themed_deck(self, size: int) -> dict:
        """
        Create a deck with a mix of fantasy cards.

        Args:
            size (int): Number of cards to generate.

        Returns:
            dict: A dictionary containing the generated random deck list.
        """
        deck: list[Any] = []

        for _ in range(0, size):
            random: str = choice(["creature", "spell", "artifact"])
            match random:
                case "creature":
                    deck.append(self.create_creature())
                case "spell":
                    deck.append(self.create_spell())
                case "artifact":
                    deck.append(self.create_artifact())

        return {
            "theme": "Fantasy",
            "count": size,
            "cards": deck
        }

    def get_supported_types(self) -> dict:
        """Return the list of supported fantasy card types."""
        return {
            "creatures": ["Dragon", "Goblin", "Cursed Spirit"],
            "spells": ["Fireball", "Ice Bolt"],
            "artifacts": ["Magic Ring", "Ancient Staff"]
        }
