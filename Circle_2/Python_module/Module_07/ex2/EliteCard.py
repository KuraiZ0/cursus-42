"""Implement the EliteCard class combining multiple interfaces."""
from ex0.Card import Card
from .Combatable import Combatable
from .Magical import Magical
from typing import Any


class EliteCard(Card, Combatable, Magical):
    """Represent a powerful card with combat and magic abilities."""

    def __init__(
            self, name: str, cost: int, rarity: str, attack: int,
            health: int, mana: int, type: str = "", armor: int = 0):
        """Initialize the EliteCard with combat and magic stats."""
        super().__init__(name, cost, rarity)
        self.attack_value = attack
        self.health = health
        self.mana = mana
        self.type = type
        self.armor = armor

    def attack(self, target: Any) -> dict:
        """Execute an attack against a specific target."""
        return {
            "attacker": self.name,
            "target": target.name,
            "damage": self.attack_value,
            "combat_type": self.type
        }

    def defend(self, incoming_damage: int) -> dict:
        """Calculate damage taken after armor reduction."""
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
        """Cast a spell and consume mana."""
        result: dict[Any] = {
            "caster": self.name,
            "spell": spell_name,
            "targets": targets,
            "mana_used": self.cost
        }
        return result

    def channel_mana(self, amount: int) -> dict:
        """Increase the mana pool by the specified amount."""
        self.mana += amount
        result: dict[Any] = {
            "channeled": amount,
            "total_mana": self.mana
        }
        return result

    def get_combat_stats(self) -> dict:
        """Return the attack and health values."""
        return {
            "attack": self.attack_value,
            "health": self.health
        }

    def get_magic_stats(self) -> dict:
        """Return the current mana value."""
        return {
            "mana": self.mana
        }

    def play(self, game_state: dict) -> dict:
        """Activate the card in the game."""
        return {
            "card_played": self.name,
            "type": "EliteCard",
            "info": "Joined the battle"
        }
