# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_garden_data.py                                  :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/09 11:47:45 by ialmani           #+#    #+#             #
#    Updated: 2025/12/09 11:47:46 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


rose = Plant("Rose", 28, 40)
orch = Plant("Orchidee", 30, 94)
cactus = Plant("Cactus", 10, 235)

print("=== Garden Plant Registry ===")
print(f"{rose.name}: {rose.height}cm, {rose.age} days old")
print(f"{orch.name}: {orch.height}cm, {orch.age} days old")
print(f"{cactus.name}: {cactus.height}cm, {cactus.age} days old")
