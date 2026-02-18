"""A module of higher-order functions for spell manipulation."""
from typing import Any


def spell_combiner(spell1: callable, spell2: callable) -> callable:
    """Combine two spells into a single spell that executes both.

    Args:
        spell1: The first spell to combine.
        spell2: The second spell to combine.

    Returns:
        A new spell that returns a tuple with the results of both spells.
    """
    return lambda *args: (spell1(*args), spell2(*args))


def power_amplifier(base_spell: callable, multiplier: int) -> callable:
    """Amplify the power of a spell by a given multiplier.

    Args:
        base_spell: The spell to amplify.
        multiplier: The factor by which to multiply the spell's result.

    Returns:
        A new spell with the amplified result.
    """
    return lambda *args: base_spell(*args) * multiplier


def conditional_caster(condition: callable, spell: callable) -> callable:
    """Cast a spell only if a condition is met.

    Args:
        condition: A function that returns a boolean.
        spell: The spell to cast if the condition is true.

    Returns:
        A new function that casts the spell or returns "Spell fizzled".
    """
    return lambda *args: spell(*args) if condition(*args) else "Spell fizzled"


def spell_sequence(spells: list[callable]) -> callable:
    """Create a sequence of spells to be cast in order.

    Args:
        spells: A list of spells to cast in sequence.

    Returns:
        A new function that returns a list of the results of each spell.
    """
    return lambda *args: [spell(arg) for arg in args for spell in spells]


if __name__ == "__main__":

    def fireball(target: str) -> str:
        """Cast a fireball spell."""
        return f"Fireball hits {target}"

    def heal(target: str) -> str:
        """Cast a healing spell."""
        return f"Heals {target}"

    def get_power() -> int:
        """Get the base power level."""
        return 10

    def is_boss(target: str) -> bool:
        """Check if the target is a boss."""
        return target.lower() == "dragon"

    print("\nTesting spell combiner...")
    combined_spell = spell_combiner(fireball, heal)
    result = combined_spell('Dragon')
    print(f"Combined spell result: {result[0]}, {result[1]}")

    print("\nTesting power amplifier...")
    amplified_power = power_amplifier(get_power, 3)
    print(f"Original: {get_power()}, Amplified: {amplified_power()}")

    print("\nTesting conditional caster...")
    cond_spell: callable = conditional_caster(is_boss, fireball)
    print(f"On Dragon: {cond_spell('Dragon')} | "
          f"On Goblin: {cond_spell('Goblin')}")

    print("\nTesting spell sequence...")
    seq_spell: callable = spell_sequence([fireball, heal])
    seq_results: list[Any] = seq_spell("Hero")
    print(f"Sequence results: {', '.join(seq_results)}")
