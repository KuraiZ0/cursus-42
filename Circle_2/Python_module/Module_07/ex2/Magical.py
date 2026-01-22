"""Define the magic interface for game entities."""
from abc import ABC, abstractmethod


class Magical(ABC):
    """Interface for entities capable of casting spells."""

    @abstractmethod
    def cast_spell(self, spell_name: str, targets: list) -> dict:
        """
        Cast a specific spell on a list of targets.

        Args:
            spell_name: The name of the spell to cast.
            targets: A list of targets for the spell.

        Returns:
            A dictionary with the spell casting results.
        """
        pass

    @abstractmethod
    def channel_mana(self, amount: int) -> dict:
        """
        Recover or channel a specific amount of mana.

        Args:
            amount: The amount of mana to channel.

        Returns:
            A dictionary with the mana channeling results.
        """
        pass

    @abstractmethod
    def get_magic_stats(self) -> dict:
        """
        Retrieve current magic statistics.

        Returns:
            A dictionary with the magic stats.
        """
        pass
