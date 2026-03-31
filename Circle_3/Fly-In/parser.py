# ########################################################################### #
#   shebang: 0                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/28 15:24:33 by ialmani             #+#    #+#            #
#   Updated: 2026/03/31 17:59:28 by ialmani            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

from typing import Any
from .zone import Zone, Connexion

class Manager:
    def __init__(self, nb_drones: int, zones: dict[Zone], start_zone: Zone,
                 end_zone: Zone) -> None:
        self.nb_drones = nb_drones
        self.zones = zones
        self.start_zone
        


class Parser:
    """Class to parse zone and connection data from a configuration file."""

    def __init__(self, file_path: str, current_line: str) -> None:
        self.file_path = file_path
        self.current_line = current_line

    def get_file(self, file_path: str) -> str:
        try:
            with open(file_path, 'r') as file:
                content: str = file.read()
                return content
        except FileNotFoundError as fe:
            raise (fe)

    def _parse_zone(self) -> str:
        zone_dic: dict[Any] = {}
        file: str = self.get_file(self.file_path)
        for line in file.splitlines():
            if (line.startswith("#") or not line):
                continue
            if "[" in line:
                parts: list[str] = line.split("[")
                base_info: str = parts[0]
                metadata: str = parts[1]
                parameters: list[str] = metadata.strip("]").split()
            else:
                base_info = line
                parameters = []

            element: list[str] = base_info.split()
            hub_type: list[str] = ['hub:', 'start_hub:', 'end_hub:']

            if (element[0] in hub_type):
                hub = Zone(element[1], int(element[2]), int(element[3]))
                for param in parameters:
                    key_value: list[str] = param.split("=")
                    key: str = key_value[0]
                    value: str = key_value[1]
                    match key:
                        case "color":
                            hub.color = value
                        case "zone":
                            hub.type_zone = value
                        case "max_drones":
                            try:
                                hub.max_drones = int(value)
                            except ValueError:
                                print("ERROR: Max drones must be an int.")
                        case _:
                            raise ValueError(
                                f"Parsing error: metadata unknown'{key}'")
                zone_dic[element[1]] = hub
            elif (element[0] == "connection"):
                zone_name: list[str] = element[1].split("-")
                zone1 = zone_dic[zone_name[0]]
                zone2 = zone_dic[zone_name[1]]
                capacity = 1

                for param in parameters:
                    key_value = param.split("=")
                    if key_value[0] == "max_link_capacity":
                        try:
                            capacity = int(key_value[1])
                        except ValueError:
                            print("ERROR: max_link_capacity must be an int.")
                connection = Connexion(capacity, zone1, zone2)
                zone1.connection.append(connection)
                zone2.connection.append(connection)
            elif (element[0] == "nb_drones:"):
                try:
                    self.nb_drones = int(element[1])
                except ValueError:
                    print("ERROR: nb_drones must be a positive integer.")
