"""
Main entry point for the DataDeck Game Engine.

This script demonstrates the usage of the FantasyCardFactory to create various
types of cards and simulates a game turn.
"""
from ex3.FantasyCardFactory import FantasyCardFactory
from ex0.Card import Card



if __name__ == "__main__":
    print("\n=== DataDeck Game Engine ===\n")
    print("Configuring Fantasy Card Game...")

    factory = FantasyCardFactory()
    dragon: Card = factory.create_creature("dragon")
    goblin: Card = factory.create_creature("goblin")
    fireball: Card = factory.create_spell("fireball")
    ring: Card = factory.create_artifact("mana_ring")

    print("Factory: FantasyCardFactory")
    print("Strategy: AggressiveStrategy")
    print(f"Available types: ")

    print("Simulating aggressive turn...")
    print(f"Hand: {}")
