# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_inventory_system.py                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/16 17:38:13 by ialmani           #+#    #+#             #
#    Updated: 2025/12/16 17:38:13 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class Player:
    def __init__(self, name, inventory=None):
        self.name = name
        if inventory is None:
            self.inventory = dict()
        else:
            self.inventory = inventory

    def display_inv(self):
        """
        function to display inventory item
        """
        for name, data in self.inventory.items():
            result = data['quantity'] * data['value']
            print(f"{name} ({data['type']}, {data['rarity']}): "
                  f"{data['quantity']}x @ {int(data['value'])} "
                  f"gold each = {int(result)}")

    def trade(self, item_name, quantity, player2):
        """
        trade either 2 players
        """
        print(f"=== Transaction: {self.name} gives {player2.name}"
              f" {quantity} {item_name}(s) ===")
        if (item_name in self.inventory and
                self.inventory[item_name]['quantity'] >= quantity):
            if item_name not in player2.inventory:
                player2.inventory[item_name] = inv[item_name].copy()
            self.inventory[item_name]['quantity'] -= quantity
            player2.inventory[item_name]['quantity'] += quantity
            print("Transaction successful!")

    def total_value(self):
        """
        Function to return the value of inventory
        """
        total = 0
        for name, data in self.inventory.items():
            total += data['quantity'] * data['value']
        return int(total)

    def count_item(self):
        """
        Function to count how much item for one player
        """
        count = 0
        for name, data in self.inventory.items():
            count += data['quantity']
        return int(count)

    def count_categories(self):
        """
        Function to count how much item in each categories for
        display like the output
        """
        categories = {}
        for name, data in self.inventory.items():
            item_type = data['type']
            categories[item_type] = (
                categories.get(item_type, 0) + data['quantity'])
        return ', '.join([f"{k}({v})" for k, v in categories.items()])


def comp_player(player1, player2):
    """
    Function to compare and display the most valuable player,
    item, and which is the rarest item
    """
    value_player1 = player1.total_value()
    value_player2 = player2.total_value()

    item_player1 = player1.count_item()
    item_player2 = player2.count_item()

    """
    for-loop to add all rare and iconic item to <rarest>
    """
    rarest = []
    for name, data in player1.inventory.items():
        if data['rarity'] in ['rare', 'iconic']:
            rarest.append(name)
    for name, data in player2.inventory.items():
        if data['rarity'] in ['rare', 'iconic']:
            rarest.append(name)
    if value_player1 > value_player2:
        print(f"Most valuable player: {player1.name} ({value_player1} gold)")
    else:
        print(f"Most valuable player: {player2.name} ({value_player2} gold)")
    if item_player1 > item_player2:
        print(f"Most items: {player1.name} ({item_player1} items)")
    else:
        print(f"Most items: {player2.name} ({item_player2} items)")
    rarest = list(set(rarest))
    print(f"Rarest items: {', '.join(rarest)}")


"""
Dict with all items
"""
inv = {
    'doran sword': {
        'quantity': 1,
        'type': 'weapon',
        'rarity': 'iconic',
        'value': 500.0
    },
    'potion': {
        'quantity': 5,
        'type': 'consumable',
        'rarity': 'common',
        'value': 50.0
    },
    'doran shield': {
        'quantity': 2,
        'type': 'armor',
        'rarity': 'rare',
        'value': 200.0
    },
    'doran ring': {
        'quantity': 1,
        'type': 'doran ring',
        'rarity': 'iconic',
        'value': 200.0
    }
}


if __name__ == "__main__":
    """
    Alice inventory attribution
    """
    alice_stuff = {
        'doran sword': inv['doran sword'],
        'doran ring': inv['doran ring'],
        'potion': inv['potion']
    }
    alice = Player("Alice", alice_stuff)
    """
    Bob inventory attribution
    """
    bob_stuff = {
        'doran sword': inv['doran sword'],
        'potion': inv['potion'],
    }
    bob = Player("Bob", bob_stuff)

    print("=== Player Inventory System ===")
    print()

    print("=== Alice's Inventory ===")
    alice.display_inv()
    print()
    print(f"Inventory value: {alice.total_value()} golds")
    print(f"Item count: {alice.count_item()} items")
    cat_alice = alice.count_categories()
    print(f"Categories: {cat_alice}")
    print()
    alice.trade('potion', 2, bob)
    print()
    print("=== Inventory Analytics ===")
    comp_player(alice, bob)
