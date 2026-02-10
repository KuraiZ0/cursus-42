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
    artifacts_list: list[Any] = [
        {"name": "Crystal Orb", "power": 85, "type": "magical"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
    ]

    spells_list: list[str] = ["fireball", "heal", "shield"]

    print("Testing artifact sorter...")
    sorted_artifacts: list[Any] = artifact_sorter(artifacts_list)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']} power)"
        f"comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']} power)"
    )

    print("\nTesting spell transformer...")
    transformed: list[str] = spell_transformer(spells_list)
    print(" ".join(transformed))
