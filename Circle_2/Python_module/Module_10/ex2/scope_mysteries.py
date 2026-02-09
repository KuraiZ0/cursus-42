"""A module for exploring variable scopes in Python."""


def mage_counter() -> callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        print(f"Call {count}: {count}")
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

    def apply_enchantment(item_name: str) -> None:
        return f"{enchantment_type} {item_name}"
    return apply_enchantment

def memory_vault() -> dict[str, callable]:
    dic: dict = {}
    def store(key: str, value: callable):
        dic[key] = value
    def recall(key):
        return dic.get(key, "Memory not found")
    return {
        "store": store,
        "recall": recall
    }


if __name__ == "__main__":
    print("Testing mage counter...")
    mage = mage_counter()
    mage()
    mage()
    mage()
    print()
    print("Testing spell acumulator...")
    spell = spell_accumulator(2)
    print(
        f"Initial power: 2 and 4 being added so: {spell(4)}\n")
    print("Testing enchantment factory...")
    sword = enchantment_factory("Flaming")
    print(sword("Sword"))
    shield = enchantment_factory("Frozen")
    print(shield("Shield"))
    print()
    print("Testing memory vault...")
    vault = memory_vault()
    stored = vault['store']
    recalled = vault['recall']
    stored('password', '12345')
    print(f"Password stored: {recalled('password')}")
    print()
