"""Demonstrate the usage of the Ability System (Exercise 2)."""
from ex2.EliteCard import EliteCard
from typing import Any


if __name__ == "__main__":
    print("=== DataDeck Ability System ===\n")
    print("EliteCard capabilites:")
    print("Card: ['play', 'get_card_info', 'is_playable']")
    print("Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']")
    print()

    arcane = EliteCard(
        "Arcane Warrior", 8, "Legendary", attack=5, health=20,
        mana=10, type="melee", armor=5)
    enemy = EliteCard("Enemy", 8, "Legendary", 5, 6, 4, "melee", 5)
    enemy1 = EliteCard("Goblin", 2, "Common", attack=2, health=4, mana=0)
    enemy2 = EliteCard("Troll", 6, "Rare", attack=4, health=15, mana=0)

    print(f"Playing {arcane.name} (Elite Card):\n")
    print("Combat phase:")

    result_attack: dict[Any] = arcane.attack(enemy)
    print(f"Attack result: {result_attack}")
    dmg = result_attack['damage']
    print(f"Defend result: {enemy.defend(dmg)}\n")

    print("Magic phase:")
    enemy_list: list[EliteCard] = [enemy1.name, enemy2.name]
    print(f"Spell cast: {arcane.cast_spell('Fireball', enemy_list)}")
    print(f"Manal channel: {arcane.channel_mana(3)}\n")

    print("Multiple interface implementation successful!")
