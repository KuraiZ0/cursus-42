"""This is the main script for the Sacred Scroll."""
# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_sacred_scroll.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/01/05 13:31:02 by ialmani           #+#    #+#             #
#    Updated: 2026/01/05 13:31:02 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#
import alchemy

if __name__ == "__main__":
    print("=== Sacred Scroll Mastery ===\n")
    print("Testing direct module access:")
    print(
        f"alchemy.elements.create_fire(): {alchemy.elements.create_fire()}")
    print(
        f"alchemy.elements.create_water(): {alchemy.elements.create_water()}")
    print(
        f"alchemy.elements.create_earth(): {alchemy.elements.create_earth()}")
    print(
        f"alchemy.elements.create_air(): {alchemy.elements.create_air()}")
    print()
    print("Testing package-level access (controlled by __init__.py):")
    print(f"alchemy.create_fire(): {alchemy.create_fire()}")
    print(f"alchemy.create_water(): {alchemy.create_water()}")
    try:
        print(f"alchemy.create_earth(): {alchemy.create_earth()}")
    except AttributeError:
        print("alchemy.create_earth(): AttributeError - not exposed")
    try:
        print(f"alchemy.create_air(): {alchemy.create_air()}")
    except AttributeError:
        print("alchemy.create_air(): AttributeError - not exposed")

    print()
    print("Package metadata:")
    print(f"Version: {alchemy.__version__}")
    print(f"Author: {alchemy.__author__}")
