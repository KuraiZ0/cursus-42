# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    ft_garden_summary.py                               :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/08 18:09:48 by ialmani           #+#    #+#             #
#    Updated: 2025/12/08 18:09:49 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

def ft_garden_summary():
    garden_name = input("Enter garden name: ")
    nb_plants = int(input("Enter number of plants: "))
    print(f"Garden: {garden_name}")
    print(f"Plants: {nb_plants}")
    print("Status: Growing well!")
