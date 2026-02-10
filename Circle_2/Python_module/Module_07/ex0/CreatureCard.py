"""This module provides the `CreatureCard` class."""

from typing import Any
from .Card import Card


class CreatureCard(Card):
    """Represents a creature card."""

    def __init__(
            self, name: str, cost: int, rarity: str, attack: int, health: int
            ) -> None:
        """
        Initialize a CreatureCard instance.

        Args:
            name: The name of the card.
            cost: The mana cost of the card.
            rarity: The rarity of the card.
            attack: The attack power of the creature.
            health: The health points of the creature.
        """
        super().__init__(name, cost, rarity)
        self.attack = attack
        self.health = health

    def play(self, game_state: dict) -> dict:
        """
        Play the creature card.

        This method reduces the player mana and returns the game state change.

        Args:
            game_state: The current game state.

        Returns:
            A dictionary representing the effect of playing the card.
        """
        result: dict[Any] = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': 'Creature summoned to battlefield'
        }
        game_state['mana'] -= self.cost
        return result

    def attack_target(self, target) -> dict:
        """
        Attack a target creature.

        Args:
            target: The target of the attack.

        Returns:
            A dictionary with the combat results, or the target if the attack
            is not possible.
        """
        if self.attack > 0 and self.health > 0:
            target.health -= self.attack
            return {
                "attacker": self.name,
                "target": target.name,
                "damage_dealt": self.attack,
                "combat_resolved": True
            }
        return target

    def get_stats(self) -> dict:
        """
        Get the stats of the creature card.

        Returns:
            A dictionary with the creature's stats.
        """
        result: dict[Any] = self.get_card_info()
        result["attack"] = self.attack
        result["health"] = self.health
        return result
