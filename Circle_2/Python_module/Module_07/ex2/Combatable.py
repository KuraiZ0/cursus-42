"""Define the combat interface for game entities."""
from abc import ABC, abstractmethod


class Combatable(ABC):
    """Interface for entities capable of combat interactions."""

    @abstractmethod
    def attack(self, target) -> dict:
        """Execute an attack on the specified target."""
        pass

    @abstractmethod
    def defend(self, incoming_damage: int) -> dict:
        """Handle incoming damage and calculate reduction."""
        pass

    @abstractmethod
    def get_combat_stats(self) -> dict:
        """Retrieve current combat statistics."""
        pass
