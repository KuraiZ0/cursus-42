"""Implement the EliteCard class combining multiple interfaces."""
from ex0.Card import Card
from .Combatable import Combatable
from .Magical import Magical
from typing import Any


class EliteCard(Card, Combatable, Magical):
    """Represent a powerful card with combat and magic abilities."""

    def __init__(
            self, name: str, cost: int, rarity: str, attack: int,
            health: int, mana: int, type: str = "", armor: int = 0) -> None:
        """
        Initialize the EliteCard with combat and magic stats.

        Args:
            name: The name of the card.
            cost: The mana cost of the card.
            rarity: The rarity of the card.
            attack: The attack power of the card.
            health: The health points of the card.
            mana: The mana points of the card.
            type: The combat type of the card.
            armor: The armor points of the card.
        """
        super().__init__(name, cost, rarity)
        self.attack_value = attack
        self.health = health
        self.mana = mana
        self.type = type
        self.armor = armor

    def attack(self, target: Any) -> dict:
        """
        Execute an attack against a specific target.

        Args:
            target: The target of the attack.

        Returns:
            A dictionary with the combat results.
        """
        return {
            "attacker": self.name,
            "target": target.name,
            "damage": self.attack_value,
            "combat_type": self.type
        }

    def defend(self, incoming_damage: int) -> dict:
        """
        Calculate damage taken after armor reduction.

        Args:
            incoming_damage: The amount of damage to defend against.

        Returns:
            A dictionary with the defense results.
        """
        blocked: int = min(incoming_damage, self.armor)
        taken: int = max(0, incoming_damage - self.armor)
        result: dict[Any] = {
            "defender": self.name,
            "damage_taken": taken,
            "damage_blocked": blocked,
            "still_alive": self.health > 0
        }
        return result

    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """
        Cast a spell and consume mana.

        Args:
            spell_name: The name of the spell to cast.
            targets: A list of targets for the spell.

        Returns:
            A dictionary with the spell casting results.
        """
        result: dict[Any] = {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": self.cost
        }
        return result

    def channel_mana(self, amount: int) -> dict:
        """
        Increase the mana pool by the specified amount.

        Args:
            amount: The amount of mana to channel.

        Returns:
            A dictionary with the mana channeling results.
        """
        self.mana += amount
        result: dict[Any] = {
            "channeled": amount,
            "total_mana": self.mana
        }
        return result

    def get_combat_stats(self) -> dict:
        """
        Return the attack and health values.

        Returns:
            A dictionary with the combat stats.
        """
        return {
            "attack": self.attack_value,
            "health": self.health
        }

    def get_magic_stats(self) -> dict:
        """
        Return the current mana value.

        Returns:
            A dictionary with the magic stats.
        """
        return {
            "mana": self.mana
        }

    def play(self, game_state: dict) -> dict:
        """
        Activate the card in the game.

        Args:
            game_state: The current game state.

        Returns:
            A dictionary with the play results.
        """
        return {
            "card_played": self.name,
            "type": "EliteCard",
            "info": "Joined the battle"
        }
