# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_plant_age.py                                    :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 15:53:15 by iliasalmani       #+#    #+#             #
#    Updated: 2025/12/08 16:05:17 by iliasalmani      ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def ft_plant_age():
    age_days = int(input("Enter plant age in days: "))
    if (age_days > 60):
        print("Plant is ready to harvest!")
    else:
        print("Plant needs more time to grow.")
