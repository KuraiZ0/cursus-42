"""A module for demonstrating the use of functools."""
import functools
import functools
import operator
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    op: dict[str, Any] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    f = op[operation]
    return functools.reduce(f, spells)

def partial_enchanter(base_enchantment: callable) -> dict[str, callable]:
    enchantment: dict[str, Any] = {
        "fire_enchant":
        functools.partial(base_enchantment, power=50, element='fire'),
        "ice_enchant":
        functools.partial(base_enchantment, power=50, element='ice'),
        "lightning_enchant":
        functools.partial(base_enchantment, power=50, element='lightning')
    }
    return enchantment


@functools.lru_cache
def memoized_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> callable:
    @functools.singledispatch
    def dispatcher(spell: Any):
        return "Unknow spell type."

    @dispatcher.register(int)
    def _(spell: int):
        return f"Damaged {spell} into ennemies."

    @dispatcher.register(str)
    def _(spell: str):
        return f"{spell} are used."

    @dispatcher.register(list)
    def _(spell: list):
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
        return f"{element} does {power} on {target}"
    fire_ench: dict[str, callable] = partial_enchanter(fire)
    print(fire_ench['fire_enchant'](target="Dragon\n"))
    print("Testing memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print()
    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(100))
    print(cast("Frost"))
    print(cast([1, 2, 3]))
