# ########################################################################### #
#   shebang: 0                                                                #
#                                                          :::      ::::::::  #
#   zone.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/28 15:14:46 by ialmani             #+#    #+#            #
#   Updated: 2026/04/01 13:46:30 by ialmani            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import Optional


class Zone:
    def __init__(self, name: str, x: int, y: int, current_drone: int,
                 max_drones: int = 1, type_zone: str = "normal",
                 color: Optional = "") -> None:
        self.name = name
        self.x = x
        self.y = y
        self.current_drone = current_drone
        self.max_drones = max_drones
        self.type_zone = type_zone
        self.color = color
        self.connection = []


class Connexion:
    def __init__(self, max_link: int, zone1: Zone, zone2: Zone,
                 flow: int = 0) -> None:
        self.max_link = max_link
        self.zone1 = zone1
        self.zone2 = zone2
        self.flow = flow


class Drone:
    def __init__(self, id: int, current_zone: Zone, in_transit: bool,
                 turns_left: int) -> None:
        self.id = id
        self.current_zone = current_zone
        self.in_transit = in_transit
        self.turns_left = turns_left
