"""Tournament Card implementation."""

from .Rankable import Rankable
from ex0.Card import Card
from ex2.Combatable import Combatable
from random import randint
from typing import Any


class TournamentCard(Card, Combatable, Rankable):
    """
    A card capable of participating in tournaments.

    Inherits from Card, Combatable, and Rankable to provide a complete
    set of features for the tournament platform.
    """

    def __init__(
        self, name: str, cost: int, rarity: str,
            attack_value: int, health: int, mana: int, card_id: str,
            armor: int = 0, rating: int = 0, win: int = 0, loose: int = 0
            ) -> None:
        """Initialize a TournamentCard."""
        super().__init__(name, cost, rarity)
        self.attack_value = attack_value
        self.health = health
        self.mana = mana
        if rating:
            self.rating = rating
        else:
            self.rating = randint(999, 1501)
        self.win = win
        self.loose = loose
        self.card_id = card_id
        self.armor = armor

    def play(self, game_state: dict) -> dict:
        """Play the card."""
        return game_state

    def attack(self, target) -> dict:
        """Execute an attack on a target."""
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

    def update_wins(self, wins: int) -> None:
        """
        Update the win count and increase the rating.

        Increments the win counter by the specified amount and applies
        a rating bonus (e.g., +16 points as seen in the subject).

        Args:
            wins (int): The number of wins to add.
        """
        self.win += wins
        self.rating += 16

    def update_losses(self, losses: int) -> None:
        """
        Update the loss count and decrease the rating.

        Increments the loss counter by the specified amount and applies
        a rating penalty.

        Args:
            losses (int): The number of losses to add.
        """
        self.loose += losses
        self.rating -= 16

    def get_rank_info(self) -> dict:
        return {
            "rating": self.rating,
            "record": f"{self.win}-{self.loose}"
        }

    def calculate_rating(self) -> int:
        """
        Return the current rating of the card.

        Returns:
            int: The current ELO rating.
        """
        return self.rating

    def get_tournament_stats(self) -> dict:
        return {
            "wins": self.win,
            "losses": self.loose,
            "rating": self.rating
        }

    def get_combat_stats(self) -> dict:
        return {
            "attacker": self.name
        }
