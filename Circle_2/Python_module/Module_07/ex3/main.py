"""
Main entry point for the DataDeck Game Engine.

This script demonstrates the usage of the FantasyCardFactory to create various
types of cards and simulates a game turn.
"""
from ex3.GameEngine import GameEngine
from .AggressiveStrategy import AggressiveStrategy
from ex3.FantasyCardFactory import FantasyCardFactory
from typing import Any


if __name__ == "__main__":
    print("\n=== DataDeck Game Engine ===\n")
    print("Configuring Fantasy Card Game...")

    factory: FantasyCardFactory = FantasyCardFactory()
    strategy: AggressiveStrategy = AggressiveStrategy()
    engine: GameEngine = GameEngine()

    engine.configure_engine(factory, strategy)
    status: dict[Any] = engine.get_engine_status()
    print(f"Factory: {status['factory_type']}")
    print(f"Strategy: {status['strategy_type']}")
    print(f"Available types: {factory.get_supported_types()}")

    print("\nSimulating aggressive turn...")
    turn: dict[Any] = engine.simulate_turn()

    print("Turn execution:")
    print(f"Strategy: {turn['strategy']}")
    print(f"Actions: {turn}")
    game_report: dict[Any] = {
        'turn_simulated': 1,
        'strategy_used': turn['strategy'],
        'total_damage': turn['damage_dealt'],
        'cards_created': 4
    }
    print()
    print("Game Report:")
    print(game_report)
    print()
    print("Abstract Factory & Strategy Pattern: Maximum flexibility achieved!")
