"""This module provides the `SpellCard` class."""


class SpellCard:
    """Represents a spell card."""

    def __init__(self, name: str, cost: int, rarity: str, effect_type: str):
        """
        Initialize a SpellCard instance.

        Args:
            name: The name of the card.
            cost: The mana cost of the card.
            rarity: The rarity of the card.
            effect_type: The type of effect the spell has.
        """
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.effect_type = effect_type

    def play(self, game_state: dict) -> dict:
        """
        Play the spell card.

        This method reduces the player mana and returns the game state change.

        Args:
            game_state: The current game state.

        Returns:
            A dictionary representing the effect of playing the card.
        """
        result = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Deal {self.cost} damage to target'
        }
        game_state['mana'] -= self.cost
        return result

    def resolve_effect(self, targets: list) -> dict:
        """
        Resolve the spell's effect on a list of targets.

        Args:
            targets: A list of targets for the spell.

        Returns:
            A dictionary with the effect resolution details.
        """
        return (
            {'target_affected': len(targets), 'effect_type': self.effect_type})
