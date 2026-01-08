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

import sys


def get_score():
    score = []
    try:
        if len(sys.argv) < 2:
            raise ValueError()
        for i in sys.argv[1:]:
            score.append(int(i))
    except ValueError:
        raise ValueError(
            "No score provided. Usage: python3 ft_score_analytics.py"
            " <score1> <score2> ..."
        )
    return score


if __name__ == "__main__":
    try:
        score = get_score()
        average = float(int(sum(score)) / int(len(score)))
        score_range = max(score) - min(score)

        print("=== Player Score Analytics ===")

        print(f"Scores processed: {score}")
        print(f"Total players: {len(score)}")

        print(f"Total score: {sum(score)}")
        print(f"Average score: {average}")

        print(f"High score: {max(score)}")
        print(f"Low score: {min(score)}")
        print(f"Score range: {score_range}")
    except ValueError as ve:
        print(ve)
