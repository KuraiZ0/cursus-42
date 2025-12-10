# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_count_harvest_iterative.py                      :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 16:06:36 by iliasalmani       #+#    #+#             #
#    Updated: 2025/12/08 18:04:42 by iliasalmani      ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def ft_count_harvest_iterative():
    day_harvest = int(input("Days until harvest: "))
    for i in range(1, day_harvest + 1):
        print(f"Day {i}")
    print("Harvest time!")
