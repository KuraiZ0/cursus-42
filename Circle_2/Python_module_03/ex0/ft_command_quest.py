# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_command_quest.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/12 12:43:42 by marvin            #+#    #+#             #
#    Updated: 2025/12/12 12:43:42 by marvin           ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

import sys


class ArgumentError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


if __name__ == "__main__":
    count = len(sys.argv)

    print("=== Command Quest ===")

    try:
        if count == 1:
            raise ArgumentError("No arguments provided!")
        print(f"Program name: {sys.argv[0]}")

        print(f"Arguments received: {count - 1}")

        for i in range(1, count):
            print(f"Argument {i}: {sys.argv[i]}")

    except ArgumentError as ae:
        print(ae)
        print(f"Program name: {sys.argv[0]}")
    finally:
        print(f"Total arguments: {count}")
