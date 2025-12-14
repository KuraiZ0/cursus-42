# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_inventory_system.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/12/13 16:56:47 by marvin            #+#    #+#              #
#    Updated: 2025/12/13 16:56:47 by marvin           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

class Player:
    def __init__(self, name, inventory=None):
        self.name = name
        if inventory is None:
            self.inventory = {}
        else:
            self.inventory = inventory

        inv = {
            'DragonSlayer': {
                'quantity': 1,
                'type': 'sword',
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
            'My_precious': {
                'quantity': 1,
                'type': 'ring',
                'rarity': 'iconic',
                'value': 200.0
            }
        }

    # def track_inv(self):
    #     """
    #     function to display inventory item
    #     """
    
    # def add_item(self, item_type):
        

    # def rich(self, player):
    #     for i in player:



if __name__ == "__main__":
    alice = Player("alice", ('DragonSlayer', 'My_precious'))
    print("=== Player Inventory System ===")
    print()

    print("=== Alice's Inventory ===")
    print(alice.inventory.items())
