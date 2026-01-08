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

def method1() -> None:
    import alchemy
    print("Method 1 - Full module import:")
    print(f"alchemy.elements.create_fire(): {alchemy.elements.create_fire()}")


def method2() -> None:
    from alchemy.elements import create_water
    print("Method 2 - Specific function import:")
    print(f"create_water(): {create_water()}")


def method3() -> None:
    from alchemy.potions import healing_potion as heal
    print("Method 3 - Aliased import:")
    print(f"heal(): {heal()}")


def method4() -> None:
    from alchemy.elements import create_fire, create_water
    from alchemy.potions import strength_potion as sp
    print("Method 4 - Multiple imports:")
    print(f"create_water(): {create_water()}")
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
