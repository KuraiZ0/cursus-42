# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_water_reminder.py                               :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 15:59:22 by iliasalmani       #+#    #+#             #
#    Updated: 2025/12/08 18:04:23 by iliasalmani      ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def ft_water_reminder():
    water_days = int(input("Days since last watering: "))
    if (water_days > 2):
        print("Water the plants!")
    else:
        print("Plants are fine.")
