"""Lambda methods using."""
artifact_sorter: list[dict] = (
    lambda artifacts: sorted(artifacts, key=lambda
                             artifact: artifact['power'], reverse=True))

power_filter: list[dict] = (
    lambda mages, min_power: list(filter(
        lambda mage: mage['power'] >= min_power, mages)))

spell_transformer: list[dict] = (
    lambda spells: list(
        map(lambda spell: "* " + spell + " *", spells)))

mage_stats: dict = (lambda mages: {
    "max_power": max(mages, key=lambda mage: mage['power'])['power'],
    "min_power": min(mages, key=lambda mage: mage['power'])['power'],
    "avg_power": round(sum(
        map(lambda mage: mage['power'], mages)) / len(mages), 2)
    })

if __name__ == "__main__":
    firestaff: dict = {
        "name": "Fire Staff",
        "power": 92,
    }
    crystal: dict = {
        "name": "Crystal Orb",
        "power": 85,
    }
    lis: list[int] = [firestaff, crystal]
    print("\nTesting artifact sorter...")
    result = artifact_sorter(lis)
    print(f"{result[0]['name']} ({result[0]['power']} power) come "
          f"before {result[1]['name']} ({result[1]['power']} power)")
