# ########################################################################### #
#   shebang: 0                                                                #
#                                                          :::      ::::::::  #
#   scheduler.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/01 12:07:31 by ialmani             #+#    #+#            #
#   Updated: 2026/04/01 16:19:30 by ialmani            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Module for scheduling and managing drone movements along paths."""

from typing import Any
from zone import Zone, Drone
from parser import Manager


class Scheduler:
    """Manages the simulation steps and drone movement."""

    def __init__(self, manager: Manager, path: list[list[Zone]]) -> None:
        """Initialize a Scheduler instance.

        Args:
            manager: The simulation manager containing map and drone info.
            path: A list of paths assigned to drones.
        """
        self.manager = manager
        self.path = path
        self.drones: list[Drone] = []
        self.create_new_drone()
        self.total_turns = 0

    def create_new_drone(self) -> None:
        """Create drone instances based on the manager's drone count."""
        for i in range(self.manager.nb_drones):
            new_drone = Drone(i + 1, self.manager.start_zone, False, 0)
            self.drones.append(new_drone)

    def is_finish(self) -> bool:
        """Check if all drones have reached the end zone.

        Returns:
            True if all drones are at the end zone, False otherwise.
        """
        for drone in self.drones:
            if drone.current_zone != self.manager.end_zone:
                return False
        return True

    def step(self) -> None:
        """Execute a simulation step, moving drones along their paths."""
        if self.is_finish():
            return
        
        turn_moves: list[Any] = []

        for drone in self.drones:
            drone.previous_zone = drone.current_zone

        for drone in self.drones:
            if drone.turns_left > 0:
                drone.turns_left -= 1
                if drone.turns_left == 0:
                    turn_moves.append(f"D{drone.id}-{drone.current_zone.name}")
                else:
                    turn_moves.append(
                        f"D{drone.id}-{drone.previous_zone.name}-{
                            drone.current_zone.name}")
            else:
                drone_path: list[Zone] = self.path[(drone.id - 1) % len(
                    self.path)]
                if drone.current_zone != self.manager.end_zone:
                    current_index: int = drone_path.index(drone.current_zone)
                    next_zone: Zone = drone_path[current_index + 1]

                    if (next_zone == self.manager.end_zone
                       or next_zone.current_drone < next_zone.max_drones):
                        prev_name: str = drone.current_zone.name
                        drone.current_zone.current_drone -= 1
                        next_zone.current_drone += 1
                        drone.current_zone = next_zone

                        match next_zone.type_zone:
                            case "normal" | "priority":
                                drone.turns_left = 0
                                turn_moves.append(
                                    f"D{drone.id}-{next_zone.name}")
                            case "restricted":
                                drone.turns_left = 1
                                turn_moves.append(
                                    f"D{drone.id}-{prev_name}-{
                                        next_zone.name}")
        print(" ".join(turn_moves))
        self.total_turns += 1
