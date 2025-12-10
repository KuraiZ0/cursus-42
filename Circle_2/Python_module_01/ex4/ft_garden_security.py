# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_garden_security.py                              :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/09 12:27:45 by ialmani           #+#    #+#             #
#    Updated: 2025/12/09 13:02:27 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class SecurePlant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def set_height(self, height):
        if height < 0:
            print(f"Invalid operation attempted: height {height} [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self.height = height
            print(f"Height updated: {self.height}cm [OK]")

    def set_age(self, age):
        if age < 0:
            print(f"Invalid operation attempted: age {age} [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self.age = age
            print(f"Age updated: {self.age} days [OK]")

    def get_height(self):
        return self.height

    def get_age(self):
        return self.age


if __name__ == "__main__":
    print("=== Garden Security System ===")

    rose = SecurePlant("Rose", 28, 40)
    print(f"Plant created: {rose.name}")

    rose.set_height(10)

    rose.set_age(10)
    h = rose.get_height()
    a = rose.get_age()
    print(f"Current plant: {rose.name} ({h}cm, {a} days)")
