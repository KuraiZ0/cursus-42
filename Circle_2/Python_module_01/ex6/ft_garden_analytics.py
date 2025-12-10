# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_garden_analytics.py                             :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: marvin <marvin@student.42.fr>              +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/10 10:02:00 by marvin            #+#    #+#             #
#    Updated: 2025/12/10 10:02:00 by marvin           ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age
        # function for grow plant

    def grow(self):
        self.height += 1
        print(f"{self.name} grew 1cm")


class FloweringPlant(Plant):
    def __init__(self, name, height, age, color, blooming):
        super().__init__(name, height, age)
        self.color = color
        self.blooming = blooming


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, age, color, blooming, points):
        super().__init__(name, height, age, color, blooming)
        self.points = points


class GardenManager:
    total_gardens = 0

    class GardenStats:
        def __init__(self):
            self.count = 0
            self.total_growth = 0
            self.total_height = 0
            self.regular_count = 0
            self.flowering_count = 0
            self.prize_count = 0

        def update(self, plant):
            self.count += 1
            if hasattr(plant, "points"):
                self.prize_count += 1
            elif hasattr(plant, "color"):
                self.flowering_count += 1
            else:
                self.regular_count += 1

        # logique de stat

    def __init__(self, name):
        self.name = name
        self.plants = []
        # incremente la variable de classe
        self.stats = self.GardenStats()
        GardenManager.total_gardens += 1

    @classmethod
    def create_garden_network(cls):
        print(f"Total garden managed: {cls.total_gardens}")

    @staticmethod
    def valid_height(height):
        return height > 0

    def add_plant(self, plant):
        self.plants.append(plant)
        print(f"Added {plant.name} to {self.name}'s garden.")
        self.stats.update(plant)

    def calculate(self):
        score = 0
        for plant in self.plants:
            score += plant.height
            if isinstance(plant, PrizeFlower):
                score += plant.points
        return score

    def print_report(self):
        print(f"\n=== {self.name}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.plants:
            if isinstance(plant, PrizeFlower):
                status = "blooming" if plant.blooming else "not blooming"
                print(
                    f"- {plant.name}: {plant.height}cm, {plant.color} "
                    f"flowers ({status}), Prize points: {plant.points}"
                )
                print()
            elif isinstance(plant, FloweringPlant):
                status = "blooming" if plant.blooming else "not blooming"
                print(
                    f"- {plant.name}: {plant.height}cm, "
                    f"{plant.color} flowers ({status})"
                )
            else:
                print(
                    f"- {plant.name}: {plant.height}cm"
                )
        print(
            f"Plants added: {self.stats.count},"
            f"Total growth: {self.stats.total_growth}cm"
            )
        print(
            f"Plant types: {self.stats.regular_count} "
            f"regular, {self.stats.flowering_count} "
            f"flowering, {self.stats.prize_count} prize flowers"
            )


if __name__ == "__main__":

    alice = GardenManager("Alice")
    bob = GardenManager("Bob")

    rose = FloweringPlant("Rose", 25, 30, "red", True)
    sunf = PrizeFlower("Sunflower", 34, 40, "yellow", True, 10)
    oak = Plant("Oak Tree", 15, 600)

    pine = Plant("Pine Tree", 60, 200)
    tulip = FloweringPlant("Tulip", 15, 10, "pink", True)
    grass = PrizeFlower("Grass", 12, 5, "green", True, 5)

    print("=== Garden Management System Demo ===")
    print()
    alice.add_plant(oak)
    alice.add_plant(rose)
    alice.add_plant(sunf)
    print()
    bob.add_plant(pine)
    bob.add_plant(tulip)
    bob.add_plant(grass)
    print()
    print("Alice is helping all plant to grow...")
    for plant in alice.plants:
        plant.grow()
        alice.stats.total_growth += 1
    print()
    alice.print_report()
    print()
    bob.print_report()
    print()
    print(f"Height validation test: {GardenManager.valid_height(oak.height)}")
    print(
        f"Garden scores - Alice: {alice.calculate()}, Bob: {bob.calculate()}"
        )
    GardenManager.create_garden_network()
