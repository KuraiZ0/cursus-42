# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_inventory_system.py                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/13 16:56:47 by marvin            #+#    #+#             #
#    Updated: 2025/12/13 16:56:47 by marvin           ###   ########.fr       #
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
                  f"{data['quantity']}x {int(data['value'])} "
                  f"gold each = {int(result)}")

    def trade(self, item_name, item_data):
        """
        trade either 2 players
        """
        if item_name == item_name:
            print()

    def total_value(self):
        total = 0
        for name, data in self.inventory.items():
            total += data['quantity'] * data['value']
        return int(total)

    def count_item(self):
        count = 0
        for name, data in self.inventory.items():
            count += data['quantity']
        return int(count)

    def count_categories(self):
        categories = {}
        for name, data in self.inventory.items():
            item_type = data['type']
            categories[item_type] = (
                categories.get(item_type, 0) + data['quantity'])
        return categories


inv = {
    'DragonSlayer': {
        'quantity': 1,
        'type': 'weapon',
        'rarity': 'iconic',
        'value': 150.0
    },
    'Berserk_potion': {
        'quantity': 5,
        'type': 'consumable',
        'rarity': 'common',
        'value': 15.0
    },
    'Aegis': {
        'quantity': 2,
        'type': 'shield',
        'rarity': 'rare',
        'value': 100.0
    },
    'My precious': {
        'quantity': 1,
        'type': 'ring',
        'rarity': 'iconic',
        'value': 200.0
    }
}


if __name__ == "__main__":
    alice_stuff = {
        'DragonSlayer': inv['DragonSlayer'],
        'My precious': inv['My precious']
    }
    alice = Player("alice", alice_stuff)

    print("=== Player Inventory System ===")
    print()

    print("=== Alice's Inventory ===")
    alice.display_inv()
    print()
    print(f"Inventory value: {alice.total_value()} golds")
    print(f"Item count: {alice.count_item()} items")
    print(f"Categories: {}")
