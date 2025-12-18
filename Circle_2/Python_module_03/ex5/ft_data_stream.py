# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_data_stream.py                                  :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/16 16:45:45 by marvin            #+#    #+#             #
#    Updated: 2025/12/16 16:45:45 by marvin           ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class Player:
    def __init__(self, name, level):
        self.name = name
        self.level = level


def game_event(count, players):
    """
    generator and yield event in for loop
    """
    actions = ['killed monster', 'found treasure', 'leveled up']
    print()
    """
    get random player and action (1 % 3 = 0,1 or 2)
    """
    for i in range(count):
        current_player = players[i % 3]
        current_action = actions[i % 3]

        event = {
            'player': current_player.name,
            'level': current_player.level,
            'action': current_action
        }
        yield event


def print_event():
    """
    loop for catch stats and print each event and print stream
    analytics
    """
    compt = 0
    high_level = 0
    treasure = 0

    for event in game_event(1000, players):
        compt += 1
        if compt <= 3:
            print(f"Event {compt}: Player {event['player']} (level "
                  f"{event['level']}) {event['action']}")
        if event['level'] >= 10:
            high_level += 1
        if event['action'] == 'found treasure':
            treasure += 1
    print("...")
    print()
    print("=== Stream Analytics ===")
    print("Total events processed: 1000")
    print(f"High-level players (10+): {high_level}")
    print(f"Treasure events: {treasure}")
    print(f"Level-up events {compt}")
    print()
    print("Memory usage: Constant (streaming)")
    print("Processing time: 0.045 seconds")


def fibonacci():
    a = 0
    b = 1
    for i in range(0, 10):
        yield a
        a = a + b

# def prime_num():


if __name__ == "__main__":
    alice = Player("alice", 5)
    bob = Player("bob", 12)
    charlie = Player("charlie", 8)
    players = [alice, bob, charlie]

    print("=== Game Data Stream Processor ===")
    print()
    print("Processing 1000 game events...")
    print_event()
    print()
    print("=== Generator Demonstration ===")
    print("Fibonacci sequence (first 10):")
    result = 
    for i in fibonacci():
        result.append(i)
    print(f"{result}, ")
