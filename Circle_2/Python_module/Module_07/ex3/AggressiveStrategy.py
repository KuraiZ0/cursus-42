"""Aggressive Strategy."""

from GameStrategy import GameStrategy
from typing import Any


class AggressiveStrategy(GameStrategy):
    """
    An aggressive game strategy that prioritizes dealing maximum damage.

    This strategy focuses on playing low-cost cards and attacking with all
    available creatures to overwhelm the opponent as quickly as possible.
    """

    def execute_turn(self, hand: list, battlefield: list) -> dict:
        """
        Execute an aggressive turn strategy.

        This strategy prioritizes playing low-cost cards and attacking with all
        available creatures on the battlefield to maximize damage output.

        Args:
            hand (list): A list of cards currently in the player's hand.
            battlefield (list): A list of cards currently on the battlefield.

        Returns:
            dict: A dictionary summarizing the actions taken, including the
                  strategy name, a list of actions, total damage dealt, and
                  mana spent.
        """
        actions: list[Any] = []
        dmg = 0
        mana_spent = 0

        for card in hand:
            if card.cost <= 3:
                actions.append(f"Played: {card.name}")
                mana_spent += card.cost
            if hasattr(card, "effect_type") and card.effect_type == "damage":
                dmg += card.cost

        for card in battlefield:
            if hasattr(card, "attack_target"):
                actions.append(f"{card.name} attack!")
                dmg += getattr(card, "attack", 0)
        return {
            "strategy": self.get_strategy_name(),
            "actions": actions,
            "damage_dealt": dmg,
            "mana_used": mana_spent
        }

    def get_strategy_name(self) -> str:
        """Return the name of the strategy."""
        return "AggressiveStrategy"

    def prioritize_targets(self, available_targets: list) -> list:
        """
        Prioritize targets for an attack.

        This strategy does not prioritize any specific targets and returns the
        list of available targets without modification.

        Args:
            available_targets (list): A list of potential targets.

        Returns:
            list: The unmodified list of available targets.
        """
        return available_targets
