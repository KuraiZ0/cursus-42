"""
This module demonstrates the usage of the TournamentPlatform.

And TournamentCard classes.
"""
from ex4 import TournamentPlatform
from ex4 import TournamentCard


if __name__ == "__main__":
    print("\n=== DataDeck Tournament Platform ===\n")
    print("Registering Tournament Cards... \n")

    dragon = TournamentCard(
        "Fire Dragon", 7, "Legendary", 9, 7, 9, "dragon_001", 4)
    wizard = TournamentCard("Ice Wizard", 4, "Rare", 6, 5, 4, "wizard_001", 2)

    tournament = TournamentPlatform()
    tournament.register_card(dragon)
    print()
    tournament.register_card(wizard)
    print()
    print("Creating tournament match...")
    print(f"Match result: "
          f"{tournament.create_match(dragon.card_id, wizard.card_id)}")
    print()
    print("Tournament Leaderboard:")
    print(tournament.get_leaderboard())
    print()
    print("Platform Report:")
    print(f"{tournament.generate_tournament_report()}\n")
    print("=== Tournament Platform Successfully Deployed! ===")
    print("All abstract patterns working together harmoniously!")
