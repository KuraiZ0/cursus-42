# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_analytics_dashboard.py                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/19 12:18:51 by ialmani           #+#    #+#             #
#    Updated: 2025/12/19 12:18:51 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

player_list = [
    ('alice', 2300, {"first_kill", "level_10"}),
    ('bob', 1800, {"level_10"}),
    ('diana', 2001, {"first_kill", "boss_slayer"}),
    ('charlie', 2150, {"boss_slayer"})]

player_dict = {
    'alice': 2300,
    'bob': 1800,
    'diana': 2001,
    'charlie': 2150}

achievement_dict = {
    "alice": {"first_kill", "level_10"},
    'bob': {"level_10"},
    'diana': {"first_kill", "boss_slayer"},
    'charlie': {"boss_slayer"}}

active_region = {
    'alice': 'north',
    'bob': 'south',
    'charlie': 'eastern',
    'diana': 'west'}


def print_list():
    """
    function to print list in the good format with comprehensions method
    """
    high_player = [name for name, score, _ in player_list if score > 2000]
    high_score = [score * 2 for _, score, _ in player_list]
    active_player = [name for name, _, _ in player_list]

    print(f"High scorers (>2000): {high_player}")
    print(f"Scores doubled: {high_score}")
    print(f"Active players: {active_player}\n")


def print_dict():
    """
    function to print dict in the good format with comprehensions method
    """
    high_player = ({name: player_dict[name]
                    for name in player_dict if player_dict[name] > 2000})
    categories = {(
        'high' if score > 2000 else 'medium' if score > 1500 else 'low')
                  for score in player_dict.values()}

    cat_score = {'high': list(categories).count('high'),
                 'medium': list(categories).count('medium'),
                 'low': list(categories).count('low')}

    ach_count = ({name: len(achievement_dict[name])
                 for name in achievement_dict})

    print(f"Player scores: {high_player}")
    print(f"Scores categories: {cat_score}")
    print(f"Achievements counts: {ach_count}\n")


def print_set():
    """
    function to print set in the good format with comprehensions method
    """
    uniq_player = {name for name in player_dict}
    uniq_ach = {ach for achs in achievement_dict.values() for ach in achs}
    active_regions = {region for _, region in active_region.items()}

    print(f"Unique players: {uniq_player}")
    print(f"Unique achievements: {uniq_ach}")
    print(f"Active regions: {active_regions}\n")


def print_analysis():
    total_players = len({name for name in player_dict})
    total_ach = len({name: len(achievement_dict[name])
                    for name in achievement_dict})
    total_score = [score for _, score, _ in player_list]

    avg_score = sum(total_score) / total_players
    top_player = sorted(player_dict, key=player_dict.get)[-1]

    print(f"Total players: {total_players}")
    print(f"Total unique achievements: {total_ach}")
    print(f"Average score: {avg_score}")
    print(f"Top perfomer: {top_player} ({player_dict[top_player]} points,"
          f" {len(achievement_dict[top_player])} achievements)")


if __name__ == "__main__":
    print("=== Game Analytics Dashboard ===\n")
    print("=== List Comprehension Examples ===")
    print_list()
    print("=== Dict Comprehension Examples ===")
    print_dict()
    print("=== Set Comprehension Examples ===")
    print_set()
    print("=== Combined Analysis ===")
    print_analysis()
