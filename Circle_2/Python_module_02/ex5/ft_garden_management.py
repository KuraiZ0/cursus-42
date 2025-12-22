# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_garden_management.py                            :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/11 21:17:36 by ialmani           #+#    #+#             #
#    Updated: 2025/12/11 21:17:37 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


class Plant:
    def __init__(self, name, water_level=10, sunlight_hours=12):
        self.name = name
        self.water_level = water_level
        self.sunlight_hours = sunlight_hours


class GardenError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class PlantError(GardenError):
    def __init__(self, message):
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message):
        super().__init__(message)


class SunlightError(GardenError):
    def __init__(self, message):
        super().__init__(message)


class GardenManager:
    """
    gardener object
    """
    def __init__(self, name):
        self.name = name
        self.plants = []
        self.water_tank = 100

    def water(self, plant):
        if self.water_tank < 10:
            raise WaterError("Not enough water in tank")
        self.water_tank -= 10
        print(f"Watering {plant.name} - success")

    def add_plant(self, plant):
        if not plant.name:
            raise (PlantError("Plant name cannot be empty!"))
        self.plants.append(plant)
        print(f"Added {plant.name} successfully")

    def add_water(self):
        """
        Adding water to all plant with a for loop
        """
        print("Watering plants...")
        print("Opening watering system")
        try:
            for plant in self.plants:
                self.water(plant)
        except WaterError as we:
            print(f"Error: {we}")
        finally:
            print("Closing watering system (cleanup)")

    def check_plant_health(self, plant):
        """
        check if the plant name, water level and sunlight hours are ok
        """
        if not plant.name:
            raise (PlantError("Plant name cannot be empty!"))
        elif plant.water_level > 10:
            raise (
                WaterError(
                    f"{plant.water_level} is too high (max 10)."))
        elif plant.water_level < 1:
            raise (
                WaterError(
                    f"Water level {plant.water_level} is too low (min 1)."))
        elif plant.sunlight_hours < 2:
            raise (
                SunlightError(
                    f"Sunlight hours {plant.sunlight_hours} "
                    f"is too low (min 2)."))
        elif plant.sunlight_hours > 12:
            raise (
                SunlightError(
                    f"Sunlight hours {plant.sunlight_hours}"
                    f" is too high (max 12)."))
        else:
            return (
                f"{plant.name}: healthy! (water: "
                f"{plant.water_level}, sun: {plant.sunlight_hours})")


if __name__ == "__main__":
    """initialize plant and gardener"""

    tomato = Plant("tomato", 5, 8)
    lettuce = Plant("lettuce", 15, 8)

    gardener = GardenManager("Willie")

    print("=== Garden Management System ===")
    print()

    print("Adding plants to garden...")
    gardener.add_plant(tomato)
    gardener.add_plant(lettuce)
    try:
        gardener.add_plant(Plant("", 5, 8))
    except PlantError as pe:
        print(f"Error adding plant: {pe}")
    print()

    gardener.add_water()
    print()

    print("Checking plant health...")
    print(gardener.check_plant_health(tomato))
    try:
        gardener.check_plant_health(lettuce)
    except WaterError as we:
        print(f"Error checking lettuce: Water level {we}")
    print()
    gardener.check_plant_health(tomato)
    print("Testing error recovery...")
    gardener.water_tank = 5
    try:
        gardener.water(tomato)
    except GardenError as ge:
        print(f"Caught GardenError: {ge}")
        print("System recovered and continuing...")
    print()

    print("Garden management system test complete!")
