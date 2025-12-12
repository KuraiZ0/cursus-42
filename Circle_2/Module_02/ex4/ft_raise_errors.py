# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_raise_errors.py                                 :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/11 14:33:33 by ialmani           #+#    #+#             #
#    Updated: 2025/12/11 14:33:34 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def check_plant_health(plant_name, water_level, sunlight_hours):
    if not plant_name:
        raise ValueError("Plant name cannot be empty!")
    elif water_level > 10:
        raise ValueError(f"Water level {water_level} is too high (max 10).")
    elif water_level < 1:
        raise ValueError(f"Water level {water_level} is too low (min 1).")
    elif sunlight_hours < 2:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too low (min 2)."
            )
    elif sunlight_hours > 12:
        raise ValueError(
            f"Sunlight hours {sunlight_hours} is too high (max 12)."
            )
    return f"Plant '{plant_name}' is healthy!"


def test_plant_checks():
    """Demonstrates testing with both good and bad values"""
    print("Testing good value...")
    try:
        result = check_plant_health("rose", 8, 4)
        print(result)
        print()
    except ValueError as e:
        print(f"Error: {e}")
    print("Testing empty plant name...")
    try:
        result = check_plant_health("", 5, 6)
        print(result)
    except ValueError as e:
        print(f"Error: {e}\n")
    print("Testing bad water level...")
    try:
        result = check_plant_health("Rose", 80, 5)
        print(result)
    except ValueError as e:
        print(f"Error: {e}\n")
    print("Testing bad sunlight hours...")
    try:
        result = check_plant_health("Tulip", 8, 74)
        print(result)
    except ValueError as e:
        print(f"Error: {e}\n")


if __name__ == "__main__":
    print("=== Garden Plant Health Checker ===\n")
    test_plant_checks()
    print("All error raising tests completed!")
