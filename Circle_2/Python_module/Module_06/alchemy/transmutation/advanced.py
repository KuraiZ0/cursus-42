"""This module contains advanced transmutation functions."""
from .basic import lead_to_gold
from ..potions import healing_potion


def philosophers_stone() -> str:
    """Create the philosopher's stone."""
    lead_to_gold_result: str = lead_to_gold()
    healing_potion_result: str = healing_potion()
    return (f"Philosopher's stone created using "
            f"{lead_to_gold_result} and {healing_potion_result}")


def elixir_of_life() -> str:
    """Create the elixir of life."""
    return "Elixir of life: eternal youth achieved!"
