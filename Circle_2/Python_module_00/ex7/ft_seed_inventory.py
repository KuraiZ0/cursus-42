# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_seed_inventory.py                               :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 18:06:05 by iliasalmani       #+#    #+#             #
#    Updated: 2025/12/08 18:06:10 by iliasalmani      ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

def ft_seed_inventory(seed_ty: str, quantity: int, unit: str) -> None:
    if unit == "packets":
        print(f"{seed_ty.capitalize()} seeds: {quantity} packets available")
    elif unit == "grams":
        print(f"{seed_ty.capitalize()} seeds: {quantity} grams total")
    elif unit == "area":
        print(f"{seed_ty.capitalize()} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")
