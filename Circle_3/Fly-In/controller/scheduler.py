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

from typing import Optional
from controller.zone import Zone, Drone
from controller.parser import Manager
from controller.algo import dist_to_goal


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
        self.dist_to_goal: dict[Zone, int] = dist_to_goal(manager.end_zone)

    def create_new_drone(self) -> None:
        """Create drone instances based on the manager's drone count."""
        self.manager.start_zone.current_drone = self.manager.nb_drones
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

    def _best_next_zone(
        self, drone: Drone, freed: dict[Zone, int],
            claimed: dict[Zone, int]) -> Optional[Zone]:
        """Find the best next zone for a drone using greedy dist-to-goal.

        Args:
            drone: The drone to route.
            freed: Zones freed this turn (drones moving out).
            claimed: Zones claimed this turn (drones moving in).

        Returns:
            The best neighbor zone, or None if the drone must wait.
        """
        best: Optional[Zone] = None
        best_dist: int = 10**9

        for link in drone.current_zone.connection:
            neighbor: Zone = (
                link.zone2 if link.zone1 == drone.current_zone else link.zone1
            )
            if neighbor.type_zone == "blocked":
                continue
            if neighbor == self.manager.end_zone:
                return neighbor

            eff_occ: int = (
                neighbor.current_drone + claimed.get(neighbor, 0)
                - freed.get(neighbor, 0))

            if eff_occ < neighbor.max_drones:
                d: int = self.dist_to_goal.get(neighbor, 10**9)
                if d < best_dist:
                    best_dist = d
                    best = neighbor
        return best

    def step(self) -> None:
        """Execute a simulation step, moving drones along their paths."""
        if self.is_finish():
            return

        turn_moves: list[str] = []

        for drone in self.drones:
            drone.previous_zone = drone.current_zone

        sorted_drones: list[Drone] = sorted(
            self.drones,
            key=lambda d: self.dist_to_goal.get(d.current_zone, 10**9))

        freed: dict[Zone, int] = {}
        claimed: dict[Zone, int] = {}

        for drone in sorted_drones:
            if drone.turns_left > 0:
                drone.turns_left -= 1
                if drone.turns_left == 0:
                    drone.current_zone.current_drone += 1
                    claimed[drone.current_zone] = (
                        claimed.get(drone.current_zone, 0) + 1)
                    turn_moves.append(
                        f"D{drone.id}-{drone.current_zone.name}")
                else:
                    turn_moves.append(
                        f"D{drone.id}-{drone.previous_zone.name}"
                        f"-{drone.current_zone.name}")
                continue

            if drone.current_zone == self.manager.end_zone:
                continue

            next_zone: Zone | None = self._best_next_zone(
                drone, freed, claimed)
            if next_zone is None:
                continue

            prev_name: str = drone.current_zone.name
            drone.current_zone.current_drone -= 1
            freed[drone.current_zone] = (
                freed.get(drone.current_zone, 0) + 1)
            drone.current_zone = next_zone

            if next_zone.type_zone == "restricted":
                drone.turns_left = 1
                turn_moves.append(
                    f"D{drone.id}-{prev_name}-{next_zone.name}")
            else:
                next_zone.current_drone += 1
                claimed[next_zone] = claimed.get(next_zone, 0) + 1
                drone.turns_left = 0
                turn_moves.append(f"D{drone.id}-{next_zone.name}")

        print(" ".join(turn_moves))
        self.total_turns += 1
