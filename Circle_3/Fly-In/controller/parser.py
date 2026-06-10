# ########################################################################### #
#   shebang: 0                                                                #
#                                                          :::      ::::::::  #
#   parser.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/03/28 15:24:33 by ialmani             #+#    #+#            #
#   Updated: 2026/04/01 12:07:11 by ialmani            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Module for parsing map configuration files and managing parsed data."""

from typing import Optional
from controller.zone import Zone, Connexion


class Manager:
    """Manages the parsed simulation data."""

    def __init__(self, nb_drones: int, zones: dict[str, Zone],
                 start_zone: Zone, end_zone: Zone) -> None:
        """Initialize a Manager instance.

        Args:
            nb_drones: Total number of drones in the simulation.
            zones: Dictionary mapping zone names to Zone objects.
            start_zone: The starting zone of the simulation.
            end_zone: The ending zone of the simulation.
        """
        self.nb_drones = nb_drones
        self.zones = zones
        self.start_zone = start_zone
        self.end_zone = end_zone


class Parser:
    """Class to parse zone and connection data from a configuration file."""

    def __init__(self, file_path: str, current_line: str) -> None:
        """Initialize a Parser instance.

        Args:
            file_path: Path to the configuration file.
            current_line: (Placeholder) Current line being processed.
        """
        self.file_path = file_path
        self.current_line = current_line

    def get_file(self, file_path: str) -> str:
        """Read the content of a file.

        Args:
            file_path: Path to the file to read.

        Returns:
            The content of the file as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        try:
            with open(file_path, 'r') as file:
                content: str = file.read()
                return content
        except FileNotFoundError as fe:
            raise (fe)

    def _parse_zone(self) -> Manager:
        """Parse the configuration file and return a Manager instance.

        Returns:
            A Manager instance containing the parsed data.

        Raises:
            ValueError: If there's a parsing error or missing start/end hub.
        """
        zone_dic: dict[str, Zone] = {}
        start_zone: Optional[Zone] = None
        end_zone: Optional[Zone] = None
        nb_drones: int = 0
        file_content: str = self.get_file(self.file_path)
        for line in file_content.splitlines():
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
            hub_types: list[str] = ['hub:', 'start_hub:', 'end_hub:']

            if element[0] in hub_types:
                hub = Zone(element[1], int(element[2]), int(element[3]), 0)
                match element[0]:
                    case "start_hub:":
                        start_zone = hub
                    case "end_hub:":
                        end_zone = hub
                for param in parameters:
                    key_value: list[str] = param.split("=")
                    key: str = key_value[0]
                    value: str = key_value[1]
                    match key:
                        case "color":
                            hub.color = value
                        case "zone":
                            valid_types: set[str] = {"normal", "blocked",
                                                     "restricted", "priority"}
                            if value not in valid_types:
                                raise ValueError(
                                    f"Parsing ERROR: invalid zone type {value}"
                                    f" (must be one of {valid_types})"
                                )
                            hub.type_zone = value
                        case "max_drones":
                            try:
                                val = int(value)
                                if val <= 0:
                                    raise ValueError()
                                hub.max_drones = val
                            except ValueError:
                                print("ERROR: Max drones must be "
                                      "a positive int.")
                        case _:
                            raise ValueError(
                                f"Parsing error: metadata unknown'{key}'")
                if element[1] in zone_dic:
                    raise ValueError(
                        f"Parsing ERROR: duplicate connection '{element[1]}'"
                    )
                zone_dic[element[1]] = hub
            elif (element[0] == "nb_drones:"):
                try:
                    val = int(element[1])
                    if val <= 0:
                        raise ValueError()
                    nb_drones = val
                except ValueError:
                    raise ValueError(
                        "ERROR: nb_drones must be a positive integer.")

        seen_connection: set[frozenset[str]] = set()
        for line in file_content.splitlines():
            if (line.startswith("#") or not line):
                continue
            if "[" in line:
                c_parts: list[str] = line.split("[")
                c_base_info: str = c_parts[0]
                c_metadata: str = c_parts[1]
                c_parameters: list[str] = c_metadata.strip("]").split()
            else:
                c_base_info = line
                c_parameters = []

            c_element: list[str] = c_base_info.split()

            if (c_element[0] == "connection:"):
                zone_names: list[str] = c_element[1].split("-")

                pair = frozenset([zone_names[0], zone_names[1]])
                if pair in seen_connection:
                    raise ValueError(
                        f"Parsing ERROR: duplicate connection '{
                            c_element[1]}'")
                seen_connection.add(pair)
                try:
                    zone1: Zone = zone_dic[zone_names[0]]
                    zone2: Zone = zone_dic[zone_names[1]]
                except KeyError as ke:
                    raise ValueError(
                        f"Parsing ERROR: unknow zone name "
                        f"{ke} in connection '{c_element[1]}'"
                    )
                capacity = 1

                for param in c_parameters:
                    c_key_value: list[str] = param.split("=")
                    if c_key_value[0] == "max_link_capacity":
                        try:
                            val = int(c_key_value[1])
                            if val <= 0:
                                raise ValueError()
                            capacity = val
                        except ValueError:
                            print("ERROR: max_link_capacity "
                                  "must be a positive int.")
                connection = Connexion(capacity, zone1, zone2)
                zone1.connection.append(connection)
                zone2.connection.append(connection)

        if start_zone is None or end_zone is None:
            raise ValueError("Simulation requires both a start and end hub.")

        return Manager(
            nb_drones, zone_dic, start_zone, end_zone)
