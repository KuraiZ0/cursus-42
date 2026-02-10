"""A module for demonstrating the use of functools."""

import functools
import operator
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    """Apply a reduction operation to a list of spells.

    Args:
        spells: A list of integers representing spell values.
        operation: The name of the operation to perform
        ("add", "multiply", "max", "min").

    Returns:
        The result of the reduction operation.
    """
    op: dict[str, Any] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }
    f = op[operation]
    return functools.reduce(f, spells)


def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    """Create a dictionary of partially applied enchantment functions.

    Args:
        base_enchantment: The base enchantment function to partially apply.

    Returns:
        A dictionary where keys are enchantment names and values
        are partially applied functions.
    """
    enchantment: dict[str, Any] = {
        "fire_enchant": functools.partial(
            base_enchantment, power=50, element="fire"),
        "ice_enchant": functools.partial(
            base_enchantment, power=50, element="ice"),
        "lightning_enchant": functools.partial(
            base_enchantment, power=50, element="lightning"
        ),
    }
    return enchantment


@functools.lru_cache
def memoized_fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number using memoization.

    Args:
        n: The index of the Fibonacci number to calculate.

    Returns:
        The nth Fibonacci number.
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> callable:
    """Create a single-dispatch generic function for handling different spell.

    Returns:
        A callable single-dispatch function that dispatches based on the type
        of the spell argument.
    """

    @functools.singledispatch
    def dispatcher(spell: Any):
        """Handle unknown spell types.

        Args:
            spell: The spell to dispatch.

        Returns:
            A string indicating an unknown spell type.
        """
        return "Unknow spell type."

    @dispatcher.register(int)
    def _(spell: int):
        """Handle integer spells, representing damage.

        Args:
            spell: The integer spell value.

        Returns:
            A string describing the damage inflicted.
        """
        return f"Damaged {spell} into ennemies."

    @dispatcher.register(str)
    def _(spell: str):
        """Handle string spells, representing named spells.

        Args:
            spell: The string spell name.

        Returns:
            A string indicating the spell's usage.
        """
        return f"{spell} are used."

    @dispatcher.register(list)
    def _(spell: list):
        """Handle list spells, representing multiple effects or targets.

        Args:
            spell: The list of spell effects or targets.

        Returns:
            A string describing the collective effect of the spells.
        """
        return f"{spell} all of them are used and damage who needed."

    return dispatcher


if __name__ == "__main__":
    print("\nTesting spell reducer...")
    spell_power: list[int] = [10, 20, 30, 40]
    total_sum: int = spell_reducer(spell_power, "add")
    print(f"Sum: {total_sum}")
    total_prod: int = spell_reducer(spell_power, "multiply")
    print(f"Product: {total_prod}")
    total_max: int = spell_reducer(spell_power, "max")
    print(f"Max: {total_max}\n")
    print("Testing partial enchanter...")

    def fire(power, element, target="Dragon"):
        """Simulate a fire enchantment."""
        return f"{element} does {power} on {target}"

    fire_ench: dict[str, callable] = partial_enchanter(fire)
    print(fire_ench["fire_enchant"](target="Dragon\n"))
    print("Testing memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print()
    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(100))
    print(cast("Frost"))
    print(cast([1, 2, 3]))
