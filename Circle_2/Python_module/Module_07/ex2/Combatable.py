"""Define the combat interface for game entities."""
from abc import ABC, abstractmethod


class Combatable(ABC):
    """Interface for entities capable of combat interactions."""

    @abstractmethod
    def attack(self, target) -> dict:
        """
        Execute an attack on the specified target.

        Args:
            target: The target of the attack.

        Returns:
            A dictionary with the combat results.
        """
        pass

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict:
        """
        Handle incoming damage and calculate reduction.

        Args:
            incoming_damage: The amount of damage to defend against.

        Returns:
            A dictionary with the defense results.
        """
        pass

    @abstractmethod
    def get_combat_stats(self) -> dict:
        """
        Retrieve current combat statistics.

        Returns:
            A dictionary with the combat stats.
        """
        pass
