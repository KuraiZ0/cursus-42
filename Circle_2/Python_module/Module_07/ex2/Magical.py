"""Define the magic interface for game entities."""
from abc import ABC, abstractmethod


class Magical(ABC):
    """Interface for entities capable of casting spells."""

    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """Cast a specific spell on a list of targets."""
        ...

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        """Recover or channel a specific amount of mana."""
        ...

    @abstractmethod
    def get_magic_stats(self) -> dict:
        """Retrieve current magic statistics."""
        ...
