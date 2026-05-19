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

"""Module defining the Zone, Connexion, Drone classes for the simulation."""

from __future__ import annotations
from typing import Optional


class Zone:
    """Represents a zone in the simulation map."""

    def __init__(self, name: str, x: int, y: int, current_drone: int,
                 max_drones: int = 1, type_zone: str = "normal",
                 color: Optional[str] = "") -> None:
        """Initialize a Zone instance.

        Args:
            name: The name of the zone.
            x: The x-coordinate of the zone.
            y: The y-coordinate of the zone.
            current_drone: Number of drones currently in the zone.
            max_drones: Maximum number of drones the zone can hold.
            type_zone: The type of the zone (e.g., "start", "end", "normal").
            color: The color assigned to the zone for display.
        """
        self.name = name
        self.x = x
        self.y = y
        self.current_drone = current_drone
        self.max_drones = max_drones
        self.type_zone = type_zone
        self.color = color
        self.connection: list[Connexion] = []


class Connexion:
    """Represents a connection between two zones."""

    def __init__(self, max_link: int, zone1: Zone, zone2: Zone,
                 flow: int = 0) -> None:
        """Initialize a Connexion instance.

        Args:
            max_link: Maximum flow capacity of the connection.
            zone1: The first zone of the connection.
            zone2: The second zone of the connection.
            flow: Current flow in the connection.
        """
        self.max_link = max_link
        self.zone1 = zone1
        self.zone2 = zone2
        self.flow = flow


class Drone:
    """Represents a drone in the simulation."""

    def __init__(self, id: int, current_zone: Zone, in_transit: bool,
                 turns_left: int) -> None:
        """Initialize a Drone instance.

        Args:
            id: Unique identifier for the drone.
            current_zone: The zone where the drone is currently located.
            in_transit: Whether the drone is currently moving between zones.
            turns_left: Number of turns remaining in transit.
        """
        self.id = id
        self.current_zone = current_zone
        self.in_transit = in_transit
        self.turns_left = turns_left
        self.previous_zone = current_zone
