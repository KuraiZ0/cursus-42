# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_import_transmutation.py                         :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/01/07 16:03:07 by ialmani           #+#    #+#             #
#    Updated: 2026/01/07 16:03:07 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

"""This module demonstrates different ways to import modules in Python."""


def method1() -> None:
    """Demonstrates full module import."""
    import alchemy
    print("Method 1 - Full module import:")
    print(f"alchemy.elements.create_fire(): {alchemy.elements.create_fire()}")


def method2() -> None:
    """Demonstrates specific function import."""
    from alchemy.elements import create_water
    print("Method 2 - Specific function import:")
    print(f"create_water(): {create_water()}")


def method3() -> None:
    """Demonstrates aliased import."""
    from alchemy.potions import healing_potion as heal
    print("Method 3 - Aliased import:")
    print(f"heal(): {heal()}")


def method4() -> None:
    """Demonstrates multiple imports."""
    from alchemy.elements import create_fire, create_earth
    from alchemy.potions import strength_potion as sp
    print("Method 4 - Multiple imports:")
    print(f"create_earth(): {create_earth()}")
    print(f"create_fire(): {create_fire()}")
    print(f"strength_potion(): {sp()}")


if __name__ == "__main__":
    print("=== Import Transmutation Mastery ===\n")
    method1()
    print()
    method2()
    print()
    method3()
    print()
    method4()
    print()
    print("All import transmutation methods mastered!")
