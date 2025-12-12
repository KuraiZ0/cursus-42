# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_custom_erros.py                                 :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/11 10:44:58 by ialmani           #+#    #+#             #
#    Updated: 2025/12/11 12:51:53 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


class GardenError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class PlantError(GardenError):
    def __init__(self, plant, message):
        super().__init__(message)
        self.plant = plant


class WaterError(GardenError):
    def __init__(self, message, water_level):
        super().__init__(message)
        self.water_level = water_level


def check_plant(plant_name, age):
    if age > 60:
        raise PlantError(plant_name, f"The {plant_name} plant is wilting!")
    else:
        print(f"The {plant_name} is healthy.")


def check_water_level(water):
    if water < 20:
        raise WaterError("Not enough water in the tank!", water)
    else:
        print("Water level is good.")


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")
    print()
    try:
        print("Testing PlantError...")
        check_plant("tomato", 63)
    except PlantError as pe:
        print(f"Caught PlantError: {pe}")
    print()
    try:
        print("Testing WaterError...")
        check_water_level(10)
    except WaterError as we:
        print(f"Caught WaterError: {we}")
    print()
    print("Testing catching all garden errors...")
    try:
        check_plant("tomato", 100)
    except GardenError as ge:
        print(f"Caught a garden error: {ge}")
    try:
        check_water_level(0)
    except GardenError as ge:
        print(f"Caught a garden error: {ge}")
    print("\nAll custom error types work correctly!")
