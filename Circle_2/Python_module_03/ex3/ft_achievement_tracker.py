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
    def __init__(self, name, level, speed, boss_slain, achievement=None):
        self.name = name
        self.level = level
        self.speed = speed
        self.boss_slain = boss_slain
        if achievement is None:
            self.achievement = set()
        else:
            self.achievement = achievement

    def check_achievement(player):
        if player.level >= 10:
            player.achievement.add("level_10")
        if player.speed >= 100:
            player.achievement.add("speed_demon")
        if player.name != "Bob":
            player.achievement.add("treasure_hunter")
        if player.boss_slain > 10:
            player.achievement.add("boss_slayer")


if __name__ == "__main__":

    alice = Player("alice", 17, 140, 3, {"first_kill"})
    bob = Player("bob", 170, 97, 62, {"collector", "first_kill"})
    charlie = Player("charlie", 47, 140, 18, {"perfectionist"})

    print("=== Achievement Tracker System ===")
    print()

    alice.check_achievement()
    print(f"Player {alice.name} achievements: {alice.achievement}")
    bob.check_achievement()
    print(f"Player {bob.name} achievements: {bob.achievement}")
    charlie.check_achievement()
    print(f"Player {charlie.name} achievements: {charlie.achievement}")
    print()

    print("=== Achievement Analytics ===")

    all_achievements = (alice.achievement | bob.achievement
                        | charlie.achievement)
    print(f"All unique achievements: {all_achievements}")
    print(f"Total unique achievements: {len(all_achievements)}")
    print()

    common = alice.achievement & bob.achievement & charlie.achievement
    print(f"Common to all players: {common}")
    uniq_alice = alice.achievement - bob.achievement - charlie.achievement
    uniq_bob = bob.achievement - alice.achievement - charlie.achievement
    uniq_charlie = charlie.achievement - alice.achievement - bob.achievement

    rare_achi = uniq_alice.union(uniq_alice, uniq_charlie)
    print(f"Rare achievements (1 player): {rare_achi}")
    print()

    ab_common = alice.achievement & bob.achievement
    print(f"{alice.name} vs {bob.name} common: {ab_common}")

    alice_uniq = alice.achievement.difference(bob.achievement)
    print(f"Alice unique: {alice_uniq}")

    bob_uniq = bob.achievement.difference(alice.achievement)
    print(f"Bob unique: {bob_uniq}")
