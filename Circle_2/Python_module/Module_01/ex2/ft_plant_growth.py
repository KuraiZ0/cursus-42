# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_plant_growth.py                                 :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/09 11:59:58 by ialmani           #+#    #+#             #
#    Updated: 2025/12/09 12:15:30 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


rose = Plant("Rose", 28, 40)


def grow(plant):
    plant.height = plant.height + 1


def age(plant):
    plant.age = plant.age + 1


def get_info():
    print(f"{rose.name}: {rose.height}cm, {rose.age} days old")


week = 0
day = 1
while week < 8:
    print(f"=== Day {day} ===")
    grow(rose)
    age(rose)
    get_info()
    day = day + 1
    week = week + 1
