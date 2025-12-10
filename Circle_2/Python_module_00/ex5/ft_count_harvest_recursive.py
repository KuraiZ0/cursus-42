# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_count_harvest_recursive.py                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 16:06:48 by iliasalmani       #+#    #+#             #
#    Updated: 2025/12/08 18:05:00 by iliasalmani      ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def ft_count_harvest_recursive(day_harvest=None, current_day=1):
    if day_harvest is None:
        day_harvest = int(input("Days until harvest: "))
        print(f"Days until harvest: {day_harvest}")

    if current_day > day_harvest:
        print("Harvest time!")
        return
    print(f"Day {current_day}")
    ft_count_harvest_recursive(day_harvest, current_day + 1)
