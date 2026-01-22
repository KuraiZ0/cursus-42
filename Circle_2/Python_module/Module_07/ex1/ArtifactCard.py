"""This module provides the `ArtifactCard` class."""


class ArtifactCard:
    """Represents an artifact card."""

    def __init__(
            self, name: str,
            cost: int, rarity: str, durability: int, effect: str):
        """
        Initialize an ArtifactCard instance.

        Args:
            name: The name of the card.
            cost: The mana cost of the card.
            rarity: The rarity of the card.
            durability: The durability of the artifact.
            effect: The effect of the artifact.
        """
        self.name = name
        self.cost = cost
        self.rarity = rarity
        self.durability = durability
        self.effect = effect

    def play(self, game_state: dict) -> dict:
        """
        Play the artifact card.

        This method reduces the player's mana and adds the artifact to the
        game state.

        Args:
            game_state: The current game state.

        Returns:
            A dictionary representing the effect of playing the card.
        """
        result = {
            'card_played': self.name,
            'mana_used': self.cost,
            'effect': f'Permanent: {self.effect}'
        }
        game_state['mana'] -= self.cost
        game_state['artifacts'].append(self.name)
        return result

    def activate_ability(self) -> dict:
        """
        Activate the artifact's ability.

        This method reduces the artifact's durability.

        Returns:
            A dictionary with the activation details.
        """
        self.durability -= 1
        return {
            'activated': self.name, 'remaining_durability': self.durability}
