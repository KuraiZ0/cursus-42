# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_achievement_tracker.py                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/12 18:35:51 by marvin            #+#    #+#             #
#    Updated: 2025/12/12 18:35:51 by marvin           ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class Player:
    def __init__(self, name, level, speed, boss_slain, achievement={}):
        self.name = name
        self.level = level
        self.speed = speed
        self.achievement = achievement
        self.boss_slain = boss_slain
    
    def check_achievement(player):
        if player.level >= 10:
            player.achievement.add('level_10')
        if player.speed >= 100:
            player.achievement.add('speed_demon')
        if player.name != "Bob":
            player.achievement.add('treasure_hunter')
        if player.boss_slain > 10:
            player.achievement.add('boss_slayer')


if __name__ == "__main__":

    alice = Player("Alice", 17, 140, 3, {'first_kill'})
    bob = Player("Bob", 170, 97, 62, {'collector', 'first_kill'})
    charlie = Player("Charlie", 47, 140, 18, {'perfectionist'})

    print("=== Achievement Tracker System ===")

    alice.check_achievement()
    print(f"Player {alice.name} achievements: {alice.achievement}")
    bob.check_achievement()
    print(f"Player {bob.name} achievements: {bob.achievement}")
    charlie.check_achievement()
    print(f"Player {charlie.name} achievements: {charlie.achievement}")
    print()

    print("=== Achievement Analytics ===")

    all_achievements = (
        alice.achievement | bob.achievement | charlie.achievement)
    print(f"All unique achievements: {all_achievements}")
    print(f"Total unique achievements: {len(all_achievements)}")
    print()

    common = alice.achievement & bob.achievement & charlie.achievement
    print(f"Common to all players: {common}")
    rare_achi = alice.achievement:difference(bob.achievement)) \
    print(f"Rare achievements (1 player): {rare_achi}")
    print()

    ab_common = alice.achievement & bob.achievement
    print(f"{alice.name} vs {bob.name} common: {ab_common}")
    """
    je suis arrive a la dis toi ce quil manque cest le dernier paragraphe de
    l'output oublie pas (.union() op: (|) & .intersection()
    op: (&) & .difference() op: (-) et les operateurs
    qui vont avec
    """
