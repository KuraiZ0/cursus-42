# *************************************************************************** #
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_harvest_total.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: iliasalmani <iliasalmani@student.42.fr>    +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 15:45:13 by iliasalmani       #+#    #+#             #
#    Updated: 2025/12/08 16:05:25 by iliasalmani      ###   ########.fr       #
#                                                                             #
# *************************************************************************** #

def ft_harvest_total():
    day1 = int(input("Day 1 harvest: "))
    day2 = int(input("Day 2 harvest: "))
    day3 = int(input("Day 3 harvest: "))
    result = (day1 + day2 + day3)
    print(f"Total harvest: {result}")
