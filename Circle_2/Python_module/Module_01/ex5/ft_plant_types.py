# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_plant_types.py                                  :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/09 13:02:00 by ialmani           #+#    #+#             #
#    Updated: 2025/12/09 18:08:20 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#


class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        self.height = self.height + 3
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    def __init__(self, name, height, age, diameter):
        super().__init__(name, height, age)
        self.diameter = diameter

    def produce_shade(self):
        area = self.diameter * 1.6
        print(f"{self.name} provides {area} square meters of shade")


class Vegetable(Plant):
    def __init__(self, name, height, age, season, nutritional_value):
        super().__init__(name, height, age)
        self.season = season
        self.nutritional_value = nutritional_value

    def get_info(self):
        print(f"{self.name} is rich in {self.nutritional_value}")


rose = Flower("Rose", 25, 30, "Red")
tulips = Flower("Tulip", 34, 40, "Purple")

babul = Tree("Babul", 250, 65, 2)
oak = Tree("Oak", 15, 600, 3)

tomato = Vegetable("Tomato", 10, 34, "summer", "vitamin C")
onion = Vegetable("Onion", 1, 28, "springs", "antioxydant")

if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    print()
    print(f"{rose.name} (Flower): {rose.height}cm, "
          f"{rose.age} days, {rose.color}")
    rose.bloom()
    print()
    print(f"{oak.name} (Tree): {oak.height}cm, "
          f"{oak.age} days, {oak.diameter}cm diameter")
    oak.produce_shade()
    print()
    print(f"{tomato.name} (Vegetable): {tomato.height}cm, "
          f"{tomato.age} days, {tomato.season} harvest")
    tomato.get_info()
