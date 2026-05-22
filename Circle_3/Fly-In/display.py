# ########################################################################### #
#   shebang: 0                                                                #
#                                                          :::      ::::::::  #
#   display.py                                           :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: ialmani <ialmani@student.42belgium.be>       +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/04/01 12:07:01 by ialmani             #+#    #+#            #
#   Updated: 2026/04/01 16:19:40 by ialmani            ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Module for the simulation GUI using the arcade library."""

import math
import arcade
from scheduler import Scheduler
from algo import find_all
from parser import Parser
from zone import Zone


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800


class SimulationWindow(arcade.Window):
    """Main window for the Fly-In simulation."""

    def __init__(self, file_path: str) -> None:
        """Initialize the simulation window.

        Args:
            file_path: Path to the map configuration file.
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Fly-In : Simulation")
        arcade.set_background_color(arcade.color.EERIE_BLACK)

        self.timer: float = 0.0
        self.turn_delay: float = 1.0
        self.auto_mode: bool = False
        self.file_path = file_path
        self.scheduler: Scheduler
        self.drone_sprite: arcade.Texture
        self.zone_sprite: arcade.Texture
        self.zones: set[Zone] = set()
        self.map_scale: float = 1.0
        self.offset_x: float = 0.0
        self.offset_y: float = 0.0

        self.setup()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events.

        Args:
            key: The key that was pressed.
            modifiers: Any modifier keys (like Shift, Ctrl) held down.
        """
        match key:
            case arcade.key.SPACE:
                if not self.scheduler.is_finish():
                    self.scheduler.step()
                    self.timer = self.turn_delay
            case arcade.key.V:
                self.auto_mode = not self.auto_mode
            case arcade.key.ESCAPE:
                arcade.exit()
            case arcade.key.R:
                self.setup()

    def setup(self) -> None:
        """Initialize or reset the simulation state."""
        parser = Parser(self.file_path, "")
        manager = parser._parse_zone()
        paths: list[list[Zone]] = find_all(
            manager.start_zone, manager.end_zone, manager.nb_drones)

        self.scheduler = Scheduler(manager, paths)
        self.timer = 0.0
        self.auto_mode = False
        self.drone_sprite = arcade.load_texture("img/Spider.png")
        self.zone_sprite = arcade.load_texture("img/Zone.png")
        self.background = arcade.load_texture("img/background.png")

        self.zones = set()
        for path in self.scheduler.path:
            for zone in path:
                self.zones.add(zone)

        # Camera dynamic
        min_x = min(zone.x for zone in self.zones)
        max_x = max(zone.x for zone in self.zones)
        max_y = max(zone.y for zone in self.zones)
        min_y = min(zone.y for zone in self.zones)

        map_width = max_x - min_x
        map_height = max_y - min_y

        padding_x = 30
        padding_y = 200
        scale_x: float = ((SCREEN_WIDTH - 2 * padding_x) /
                          map_width if map_width > 0 else 100)
        scale_y: float = ((SCREEN_HEIGHT - 2 * padding_y) /
                          map_height if map_height > 0 else 100)

        self.map_scale = min(scale_x, scale_y)

        self.offset_x = (
            SCREEN_WIDTH - (map_width * self.map_scale)) / 2 - (
                min_x * self.map_scale)
        self.offset_y = (
            SCREEN_HEIGHT - (map_height * self.map_scale)) / 2 - (
                min_y * self.map_scale)

    def on_draw(self) -> None:
        """Render the simulation screen."""
        self.clear()
        bg_rect = arcade.LRBT(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_texture_rect(self.background, bg_rect)
        y_boost = 2.5
        for path in self.scheduler.path:
            for i in range(len(path) - 1):
                z1, z2 = path[i], path[i+1]
                x1, y1 = (z1.x * self.map_scale + self.offset_x,
                          z1.y * y_boost * self.map_scale + self.offset_y)
                x2, y2 = (z2.x * self.map_scale + self.offset_x,
                          z2.y * y_boost * self.map_scale + self.offset_y)
                arcade.draw_line(x1, y1, x2, y2, arcade.color.GRAY, 2)

        sprite_size: float = max(
            24.0, min(45.0, 35.0 * (self.map_scale / 10.0))
        )
        for zone in self.zones:
            cx = zone.x * self.map_scale + self.offset_x
            cy = (zone.y * y_boost) * self.map_scale + self.offset_y

            half_size: float = sprite_size / 2

            offset_visual_x = 0
            offset_visual_y = -8

            if int(zone.x) % 2 == 0:
                text_y = cy + half_size + 20
            else:
                text_y = cy - 75

            arcade.draw_line(cx, cy, cx, text_y, (150, 150, 150, 150), 1)

            color = arcade.color.CORNFLOWER_BLUE
            if zone.type_zone == "restricted":
                color = arcade.color.IMPERIAL_RED
            elif zone.type_zone == "priority":
                color = arcade.color.SAE
            arcade.draw_text(
                zone.name, cx, text_y, color, 10,
                align="center", anchor_x="center", anchor_y="center")

            zone_rect = arcade.XYWH(
                (cx - half_size) + offset_visual_x,
                (cy - half_size) + offset_visual_y, sprite_size, sprite_size)
            arcade.draw_texture_rect(self.zone_sprite, zone_rect)

        progress: float = self.timer / self.turn_delay
        for drone in self.scheduler.drones:
            start_x: float = (drone.previous_zone.x
                       * self.map_scale + self.offset_x)
            start_y: float = (drone.previous_zone.y * y_boost
                       * self.map_scale + self.offset_y)
            end_x = (drone.current_zone.x
                     * self.map_scale + self.offset_x)
            end_y = (drone.current_zone.y * y_boost
                     * self.map_scale + self.offset_y)

            theorical_dx = start_x + (end_x - start_x) * progress
            theorical_dy = start_y + (end_y - start_y) * progress
            arrange_radius = 10
            angle = float(drone.id)

            off_x: float = math.cos(angle) * arrange_radius
            off_y: float = math.sin(angle) * arrange_radius

            dx = theorical_dx + off_x
            dy = theorical_dy + off_y

            drone_size: float = sprite_size * 0.7
            half_drone = drone_size / 2

            drone_rect = arcade.XYWH(
                (dx - half_drone) + offset_visual_x,
                (dy - half_drone) + offset_visual_y, drone_size, drone_size)
            arcade.draw_texture_rect(self.drone_sprite, drone_rect)

        # Leaderboard creation
        arcade.draw_lrbt_rectangle_filled(
            20, 220, 660, 780, (50, 50, 50, 200))
        drones_arrived = 0
        for drone in self.scheduler.drones:
            if drone.current_zone == self.scheduler.manager.end_zone:
                drones_arrived += 1
        arcade.draw_text(
            f"Score: {drones_arrived}", 40, 750,
            arcade.color.IMPERIAL_RED, 16)
        arcade.draw_text(
            f"Turn: {self.scheduler.total_turns}", 40, 715,
            arcade.color.IMPERIAL_RED, 16)

        # Mode creation
        arcade.draw_text(
            "Mode: AUTO" if self.auto_mode else "Mode: MANUAL",
            40, 675, arcade.color.AFRICAN_VIOLET, 16)

        if self.scheduler.is_finish():
            arcade.draw_text(
                "SIMULATION FINISHED", SCREEN_WIDTH//2 - 150,
                SCREEN_HEIGHT - 40, arcade.color.GREEN, 20, bold=True)

    def on_update(self, delta_time: float) -> None:
        """Update the simulation state.

        Args:
            delta_time: Time passed since the last update.
        """
        if self.scheduler.is_finish():
            self.timer = self.turn_delay
            return

        if self.auto_mode:
            self.timer += delta_time
            if self.timer >= self.turn_delay:
                self.scheduler.step()
                self.timer = 0.0



# ajouter une legende a droite avec les differentes touches qui existent