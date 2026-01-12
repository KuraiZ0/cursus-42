from __init__ import SpellCard, Deck, ArtifactCard


if __name__ == "__main__":
    print("=== DataDeck Deck Builder ===\n")
    print("Building deck with different card types...")
    light = SpellCard("Lightning Bolt", 3, "Common", "damage")
    mana_crystal = ArtifactCard(
        "Mana Crystal", 2, "Rare", 999, "+1 mana per turn")

    deck = Deck()
    deck.add_card(light)
    deck.add_card(mana_crystal)

    print(f"Deck stats: {deck.get_deck_stats()}")
    print()
    print("Drawing and playing cards:")
    deck.shuffle()

    spell = deck.draw_card()
    if spell:
        game_state = {'mana': 10, 'artifacts': []}
        print(f"Drew: {spell.name} (Spell)")
        print(f"Play result: {spell.play(game_state)}")

    artifact = deck.draw_card()
    if artifact:
        print(f"Drew: {artifact.name} (Artifact)")
        print(f"Play result: {artifact.play(game_state)}")

    print("Polymorphism in action: Same interface, different card behaviors!")
