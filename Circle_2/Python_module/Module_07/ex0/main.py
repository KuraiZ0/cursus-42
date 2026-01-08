from Card import Card
from CreatureCard import CreatureCard


print("=== DataDeck Card Foundation ===\n")
print("Testing Abstract Base Class Design:\n")
print("CreatureCard Info:")
first_card = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
print(first_card.get_stats())
