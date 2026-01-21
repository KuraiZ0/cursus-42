from .SpellCard import SpellCard
from .Deck import Deck
from .ArtifactCard import ArtifactCard
from ex0.CreatureCard import CreatureCard


if __name__ == "__main__":
    print("=== DataDeck Deck Builder ===\n")
    print("Building deck with different card types...")
    light = SpellCard("Lightning Bolt", 3, "Common", "damage")
    mana_crystal = ArtifactCard(
        "Mana Crystal", 2, "Rare", 999, "+1 mana per turn")
    f_dragon = CreatureCard(
        "Fire Dragon", 5, "Rare", 6, 4)  # attack=6, health=4

    deck = Deck([])
    deck.add_card(light)
    deck.add_card(mana_crystal)
    deck.add_card(f_dragon)
    print(f"Deck stats: {deck.get_deck_stats()}")
    print()
    print("Drawing and playing cards:\n")
    deck.shuffle()

    game_state = {'mana': 10, 'artifacts': []}
    
    spell = deck.draw_card()
    if spell:
        print(f"Drew: {spell.name} (Spell)")
        print(f"Play result: {spell.play(game_state)}\n")

    artifact = deck.draw_card()
    if artifact:
        print(f"Drew: {artifact.name} (Artifact)")
        print(f"Play result: {artifact.play(game_state)}\n")

    creature = deck.draw_card()
    if creature:
        print(f"Drew: {creature.name} (Creature)")
        print(f"Play result: {creature.play(game_state)}\n")

    print("Polymorphism in action: Same interface, different card behaviors!")
