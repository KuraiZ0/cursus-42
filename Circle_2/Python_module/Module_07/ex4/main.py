from ex4 import TournamentPlateform
from ex4 import TournamentCard


if __name__ == "__main__":
    print("\n=== DataDeck Tournament Plateform ===\n")
    print("Registering Tournament Cards... \n")

    dragon = TournamentCard(
        "Fire Dragon", 7, "Legendary", 9, 7, 9, "dragon_001", 4)
    wizard = TournamentCard("Ice Wizard", 4, "Rare", 6, 5, 4, "wizard_001", 2)

    tournament = TournamentPlateform()
    print("- Interfaces: [Card, Combatable, Rankable]")
    dragon.get_rank_info()
