# ########################################################################### #
#   shebang: 0                                                                #
#                                                          :::      ::::::::  #
#   algo.py                                              :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/01 12:07:21 by ialmani             #+#    #+#            #
#   Updated: 2026/04/01 16:19:19 by ialmani            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Module containing pathfinding algorithms for the simulation."""

import heapq
from controller.zone import Zone
from typing import Optional


def find_all(start_node: Zone,
             end_node: Zone, nb_drones: int) -> list[list[Zone]]:
    """Find multiple paths from start to end node based on available flow.

    Args:
        start_node: The starting zone.
        end_node: The target zone.
        nb_drones: The number of drones needing paths.

    Returns:
        A list of paths, where each path is a list of Zone objects.
    """
    all_paths: list[list[Zone]] = []
    link_costs: dict[int, int] = {}

    while len(all_paths) < nb_drones:
        path: list[Zone] = algo(start_node, end_node, link_costs)

        if not path:
            break

        all_paths.append(path)
        for i in range(len(path) - 1):
            z1, z2 = path[i], path[i+1]
            for link in z1.connection:
                if link.zone1 == z2 or link.zone2 == z2:
                    link_costs[id(link)] = (
                        link_costs.get(id(link), 0) + 50)
                    break
    return all_paths


def dist_to_goal(end_zone: Zone) -> dict[Zone, int]:
    """Calcul the absolute shortest path cost from every zone to the goal."""
    dist: dict[Zone, int] = {end_zone: 0}

    queue: list[tuple[int, int, Zone]] = [(0, id(end_zone), end_zone)]

    while queue:
        current_dist, _, current_zone = heapq.heappop(queue)

        if current_dist > dist.get(current_zone, 10**9):
            continue

        for link in current_zone.connection:
            neighbor = link.zone1 if link.zone2 == current_zone else link.zone2

            if neighbor.type_zone == "blocked":
                continue

            weight = 2 if current_zone.type_zone == "restricted" else 1
            new_dist: int = current_dist + weight

            if new_dist < dist.get(neighbor, 10**9):
                dist[neighbor] = new_dist
                heapq.heappush(queue, (new_dist, id(neighbor), neighbor))

    return dist


def algo(start_node: Zone, end_node: Zone,
         link_costs: dict[int, int] | None = None) -> list[Zone]:
    """Find a single shortest path from start to end node using Dijkstra.

    Args:
        start_node: The starting zone.
        end_node: The target zone.

    Returns:
        A list of Zone objects representing the shortest path.
    """
    if link_costs is None:
        link_costs = {}
    queue: list[tuple[int, int, Zone]] = [(0, id(start_node), start_node)]
    distances: dict[Zone, int] = {start_node: 0}
    parent: dict[Zone, Optional[Zone]] = {start_node: None}

    while queue:
        current_cost, _, current_zone = heapq.heappop(queue)
        if current_zone == end_node:
            break
        for link in current_zone.connection:
            neighbor: Zone = (
                link.zone2 if link.zone1 == current_zone else link.zone1)
            if neighbor.type_zone == "blocked":
                continue
            base_weight = 2 if neighbor.type_zone == "restricted" else 1
            penalty = link_costs.get(id(link), 0)
            new_cost = current_cost + base_weight + penalty

            if new_cost < distances.get(neighbor, 10**9):
                distances[neighbor] = new_cost
                parent[neighbor] = current_zone
                heapq.heappush(queue, (new_cost, id(neighbor), neighbor))
    if end_node not in parent:
        return []

    path: list[Zone] = []
    cursor: Zone | None = end_node
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    return path[::-1]
