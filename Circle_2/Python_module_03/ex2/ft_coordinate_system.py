# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_coordinate_system.py                            :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/12 14:54:02 by marvin            #+#    #+#             #
#    Updated: 2025/12/12 14:54:02 by marvin           ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

import math

# import sys


def dist_formula(pos1, pos2):
    """calculate 3D Euclidean distance between two positions"""
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2

    result = math.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)
    return result


def parsing(coo_string):
    """parse a coordinate string like '3,4,0' into a tuple"""
    parts = coo_string.split(",")
    nbr = []
    for x in parts:
        nbr.append(int(x))
    return tuple(nbr)


if __name__ == "__main__":
    pos1 = (10, 20, 5)
    pos2 = (0, 0, 0)
    print("=== Game Coordinate System ===")
    print()
    dist1 = round(dist_formula(pos1, pos2), 2)

    print(f"Position created: {pos1}")
    print(f"Distance between {pos2} and {pos1}: {dist1}")
    print()

    coo_string = "3,4,0"
    print(f'Parsing coordinates: "{coo_string}"')
    try:
        new_coo = parsing(coo_string)
        print(f"Parsed position: {new_coo}")

        dist2 = round(dist_formula(new_coo, pos2), 2)
        print(f"Distance between {pos2} and {new_coo}: {dist2}")
    except ValueError as ve:
        print(f"Error parsing coordinates: {ve}")
    print()
    print('Parsing invalid coordinates: "abc,def,ghi"')
    invalid = "abc,def,ghi"
    try:
        invalid_coo = parsing(invalid)
    except ValueError as ve:
        print(f"Error parsing coordinates: {ve}")
        print(f"Error details - Type: {type(ve).__name__}, Args: {ve.args}")
    print()
    print("Unpacking demonstration:")
    x, y, z = new_coo
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}")
