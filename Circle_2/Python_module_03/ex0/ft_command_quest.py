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
