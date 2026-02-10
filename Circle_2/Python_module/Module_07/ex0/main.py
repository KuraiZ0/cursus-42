"""This script demonstrates the usage of the CreatureCard class."""

from typing import Any
from ex0.CreatureCard import CreatureCard

if __name__ == "__main__":
    print("=== DataDeck Card Foundation ===\n")

    print("Testing Abstract Base Class Design:\n")
    print("CreatureCard Info:")
    first_card: CreatureCard = CreatureCard(
        "Fire Dragon", 5, "Legendary", 7, 5)
    print(first_card.get_stats())
    print()
    print("Playing Fire Dragon with 6 mana available:")
    print(f"Playable: {first_card.is_playable(6)}")
    game_state: dict[Any] = {"mana": 6, "battlefield": []}
    result_play: dict[Any] = first_card.play(game_state)
    print(f"Play result: {result_play}")
    print()
    print(f"{first_card.name} attacks Goblin Warrior:")
    goblin: CreatureCard = CreatureCard("Goblin Warrior", 4, "Rare", 2, 7)
    print(f"Attack result: {first_card.attack_target(goblin)}")
    print()
    print("Testing insufficient mana (3 available):")
    print(f"Playable: {first_card.is_playable(3)}")
    print()
    print("Abstract pattern successfully demonstrated!")
