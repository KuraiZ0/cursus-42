"""A module for demonstrating lambda functions and their equivalents."""


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort a list of artifacts by power in descending order.

    Args:
        artifacts: A list of artifact dictionaries, each with a 'power' key.

    Returns:
        The sorted list of artifacts.
    """
    return sorted(artifacts, key=lambda artifact: artifact["power"], reverse=True)


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
    powers = [mage["power"] for mage in mages]
    return {
        "max_power": max(powers),
        "min_power": min(powers),
        "avg_power": round(sum(powers) / len(powers), 2),
    }


if __name__ == "__main__":
    firestaff = {"name": "Fire Staff", "power": 92}
    crystal = {"name": "Crystal Orb", "power": 85}
    artifacts_list = [firestaff, crystal]

    print("\nTesting artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts_list)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']}) "
        f"comes before {sorted_artifacts[1]['name']} "
        f"({sorted_artifacts[1]['power']})"
    )
