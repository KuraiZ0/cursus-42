# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_plant_factory.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/09 12:16:02 by ialmani           #+#    #+#             #
#    Updated: 2025/12/09 12:17:23 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

class Plant:
    def __init__(self, name, start_height, start_age):
        self.name = name
        self.start_height = start_height
        self.start_age = start_age


rose = Plant("Rose", 28, 40)
orch = Plant("Orchidee", 30, 94)
cact = Plant("Cactus", 10, 235)
acon = Plant("Aconite", 19, 48)
pis = Plant("Pissenlit", 10, 10)

print("=== Plant Factory Output ===")
print(f"Created: {rose.name} ({rose.start_height}cm, {rose.start_age} days)")
print(f"Created: {orch.name} ({orch.start_height}cm, {orch.start_age} days)")
print(f"Created: {cact.name} ({cact.start_height}cm, {cact.start_age} days)")
print(f"Created: {acon.name} ({acon.start_height}cm, {acon.start_age} days)")
print(f"Created: {pis.name} ({pis.start_height}cm, {pis.start_age} days)")
print("Total plants created: 5")
