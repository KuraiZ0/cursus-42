"""A module for exploring variable scopes in Python."""
from typing import Any


def mage_counter() -> callable:
    """Create a counter function that increments each time it's called.

    Returns:
        A callable function that, when called, increments and returns a count.
    """
    count = 0

    def counter() -> int:
        """Increment and return the current count.

        Returns:
            The current count after incrementing.
        """
        nonlocal count
        count += 1
        print(f"Call {count}: {count}")
        return count

    return counter


def spell_accumulator(initial_power: int) -> callable:
    """Create a function that accumulates power based on an initial value.

    Args:
        initial_power: The starting power level.

    Returns:
        A callable function that, when called with an added power,
        updates and returns the total power.
    """
    total_power: int = initial_power

    def counter(added_power: int) -> int:
        """Add power to the total and return the new total.

        Args:
            added_power: The amount of power to add.

        Returns:
            The updated total power.
        """
        nonlocal total_power
        total_power += added_power
        return total_power

    return counter


def enchantment_factory(enchantment_type: str) -> callable:
    """Create an enchantment function of a specific type.

    Args:
        enchantment_type: The type of enchantment (e.g., "Flaming", "Frozen").

    Returns:
        A callable function that applies the enchantment to an item.
    """

    def apply_enchantment(item_name: str) -> None:
        """Apply the specific enchantment to an item.

        Args:
            item_name: The name of the item to enchant.

        Returns:
            A string representing the enchanted item.
        """
        return f"{enchantment_type} {item_name}"

    return apply_enchantment


def memory_vault() -> dict[str, callable]:
    """Create a closure that acts as a simple key-value store.

    Returns:
        A dictionary containing 'store' and 'recall' functions.
    """
    dic: dict = {}

    def store(key: str, value: callable):
        """Store a key-value pair in the vault.

        Args:
            key: The key to store the value under.
            value: The value to store.
        """
        dic[key] = value

    def recall(key):
        """Recall a value from the vault based on its key.

        Args:
            key: The key of the value to recall.

        Returns:
            The stored value or "Memory not found" if the key does not exist.
        """
        return dic.get(key, "Memory not found")

    return {"store": store, "recall": recall}


if __name__ == "__main__":
    print("Testing mage counter...")
    mage = mage_counter()
    mage()
    mage()
    mage()
    print()
    print("Testing spell acumulator...")
    spell = spell_accumulator(2)
    print(f"Initial power: 2 and 4 being added so: {spell(4)}\n")
    print("Testing enchantment factory...")
    sword = enchantment_factory("Flaming")
    print(sword("Sword"))
    shield = enchantment_factory("Frozen")
    print(shield("Shield"))
    print()
    print("Testing memory vault...")
    vault: dict[Any] = memory_vault()
    stored = vault["store"]
    recalled = vault["recall"]
    stored("password", "12345")
    print(f"Password stored: {recalled('password')}")
    print()
