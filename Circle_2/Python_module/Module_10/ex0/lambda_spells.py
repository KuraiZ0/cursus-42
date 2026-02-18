"""A module for demonstrating lambda functions and their equivalents."""
from typing import Any


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort a list of artifacts by power in descending order.

    Args:
        artifacts: A list of artifact dictionaries, each with a 'power' key.

    Returns:
        The sorted list of artifacts.
    """
    return sorted(
        artifacts, key=lambda artifact: artifact["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    """Filter mages by a minimum power level.

    Args:
        mages: A list of mage dictionaries, each with a 'power' key.
        min_power: The minimum power required.

    Returns:
        A list of mages who meet the power requirement.
    """
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """Transform spell names with a decorative pattern.

    Args:
        spells: A list of spell names.

    Returns:
        The list of transformed spell names.
    """
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Calculate power statistics for a list of mages.

    Args:
        mages: A list of mage dictionaries, each with a 'power' key.

    Returns:
        A dictionary with 'max_power', 'min_power', and 'avg_power'.
    """
    powers: list[Any] = [mage["power"] for mage in mages]
    return {
        "max_power": max(powers),
        "min_power": min(powers),
        "avg_power": round(sum(powers) / len(powers), 2),
    }


if __name__ == "__main__":
    artifacts: list[Any] = [{"name": "Crystal Orb", "power": 85},
                            {"name": "Fire Staff", "power": 92}]
    print("\nTesting artifact sorter...")
    sorted_list: list[dict] = artifact_sorter(artifacts)
    if len(sorted_list) >= 2:
        first: dict = sorted_list[0]
        second: dict = sorted_list[1]
        print(f"{first['name']} ({first['power']} power) comes before "
              f"{second['name']} ({second['power']} power)")

    print("\nTesting spell transformer...")
    spell: list[str] = spell_transformer(["fireball", "heal", "shield"])
    result: str = " ".join(spell)
    print(result)

    mages: list[dict[str, Any]] = [
        {"name": "Alex", "power": 50},
        {"name": "Jordan", "power": 30},
        {"name": "Morgan", "power": 85}
    ]
    print("\nTesting power filter...")
    strong: list[dict] = power_filter(mages, 40)

    formatted_mages: str = ", ".join(
        [f"{m['name']} ({m['power']})" for m in strong]
    )
    print(f"Qualified mages: {formatted_mages}")
    print("\nTesting mage stats...")
    stats: dict[str, Any] = mage_stats(mages)

    print(f"Max: {stats['max_power']} | Min: {stats['min_power']} | "
          f"Average: {stats['avg_power']}")
