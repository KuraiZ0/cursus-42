"""A module for exploring variable scopes in Python."""


def mage_counter() -> callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter

def spell_accumulator(initial_power: int) -> callable:
    total_power: int = initial_power

    def counter(added_power: int) -> int:
        nonlocal total_power
        total_power += added_power
        return total_power
    return counter

def enchantment_factory(enchantment_type: str) -> callable:

    def apply_enchantment(enchantment: str):