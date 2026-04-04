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

from .zone import Zone, Connexion
from collections import deque
from .parser import Manager, Parser


def algo(start_node: Zone, end_node: Zone) -> None:
    waiting: deque[Zone] = deque([start_node])
    visited: set[Zone] = set()
    visited.add(start_node)

    dic_path: dict[Zone, None] = {start_node: None}
    while waiting:
        atm: Zone = waiting.popleft()
        if atm == end_node:
            break
        for link in atm.connection:
            if link.flux < link.max_link:
                if link.zone1 == atm:
                    neighbor = link.zone2
                else:
                    neighbor = link.zone1
                if neighbor not in visited:
                    waiting.append(neighbor)
                    visited.add(neighbor)
                    dic_path[neighbor] = atm
    route: list[Zone] = []
    cursor: Zone = end_node
    while cursor is not None:
        route.append(cursor)
        cursor = dic_path[end_node - 1]
