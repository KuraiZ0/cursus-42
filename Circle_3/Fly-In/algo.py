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
from typing import Optional
from zone import Zone


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

    while len(all_paths) < nb_drones:
        path: list[Zone] = algo(start_node, end_node)

        if not path:
            break
        all_paths.append(path)
        for i in range(len(path) - 1):
            z1, z2 = path[i], path[i+1]
            for link in z1.connection:
                if link.zone1 == z2 or link.zone2 == z2:
                    link.flow += 1
                    break
    return all_paths


def algo(start_node: Zone, end_node: Zone) -> list[Zone]:
    """Find a single shortest path from start to end node using Dijkstra.

    Args:
        start_node: The starting zone.
        end_node: The target zone.

    Returns:
        A list of Zone objects representing the shortest path.
    """
    queue: list[tuple[int, int, Zone]] = [(0, id(start_node), start_node)]
    distances: dict[Zone, int] = {start_node: 0}
    parent: dict[Zone, Optional[Zone]] = {start_node: None}

    while queue:
        current_cost, _, current_zone = heapq.heappop(queue)
        if current_zone == end_node:
            break
        for link in current_zone.connection:
            if link.flow < link.max_link:
                neighbor = (
                    link.zone2 if link.zone1 == current_zone else link.zone1)
                match neighbor.type_zone:
                    case "blocked":
                        continue
                    case "restricted":
                        weight = 2
                    case "normal":
                        weight = 1
                    case "priority":
                        weight = 1
                    case _:
                        weight = 1
                new_cost: int = current_cost + weight
                if neighbor not in distances or new_cost < distances[neighbor]:
                    distances[neighbor] = new_cost
                    parent[neighbor] = current_zone
                    heapq.heappush(queue, (new_cost, id(neighbor), neighbor))
    path: list[Zone] = []
    if end_node not in parent:
        return []

    cursor: Optional[Zone] = end_node
    while cursor is not None:
        path.append(cursor)
        cursor = parent[cursor]
    return path[::-1]
