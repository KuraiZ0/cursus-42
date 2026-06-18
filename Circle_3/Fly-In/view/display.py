"""Module for the simulation GUI using the arcade library."""
import arcade # type: ignore
import math
from controller.scheduler import Scheduler
from controller.algo import find_all
from controller.parser import Parser
from controller.zone import Zone


SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 800


class SimulationWindow(arcade.Window):
    """Main window for the Fly-In simulation."""

    def __init__(
            self, file_path: str, capacity_info: bool) -> None:
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
        self.capacity_info = capacity_info
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
        print(f"nb_drones: {manager.nb_drones}")
        print(f"nb paths found: {len(paths)}")
        print(f"start connections: {len(manager.start_zone.connection)}")

        self.scheduler = Scheduler(manager, paths, self.capacity_info)
        self.timer = 0.0
        self.auto_mode = False
        self.drone_sprite = arcade.load_texture("view/img/Spider.png")
        self.zone_sprite = arcade.load_texture("view/img/Zone.png")
        self.background = arcade.load_texture("view/img/background.png")

        self.text_score = arcade.Text(
            "", 40, 750, arcade.color.IMPERIAL_RED, 16)
        self.text_turn = arcade.Text(
            "", 40, 715, arcade.color.IMPERIAL_RED, 16)
        self.text_mode = arcade.Text(
            "", 40, 675, arcade.color.AFRICAN_VIOLET, 16)

        self.text_finish = arcade.Text(
            "🏁 SIMULATION FINISHED 🏁", SCREEN_WIDTH//2 - 150,
            SCREEN_HEIGHT - 40, arcade.color.GREEN, 20, bold=True)
        self.text_keybinds = arcade.Text(
            "Keybinds", 0, 0, arcade.color.WHITE, 14, bold=True)
        self.text_v = arcade.Text(
            "V :     Auto/Manual", 0, 0, arcade.color.LIGHT_GRAY, 12)
        self.text_r = arcade.Text(
            "R :     Retry", 0, 0, arcade.color.LIGHT_GRAY, 12)
        self.text_space = arcade.Text(
            "SPACE : Next step", 0, 0, arcade.color.LIGHT_GRAY, 12)
        self.text_esc = arcade.Text(
            "ESC :   Leave", 0, 0, arcade.color.LIGHT_GRAY, 12)

        self.zones = set(manager.zones.values())

        self.grid_x = 220
        self.grid_y = 200

        min_x: int = min(zone.x * self.grid_x for zone in self.zones)
        max_x: int = max(zone.x * self.grid_x for zone in self.zones)
        min_y: int = min(zone.y * self.grid_y for zone in self.zones)
        max_y: int = max(zone.y * self.grid_y for zone in self.zones)

        map_width: int = max_x - min_x
        map_height: int = max_y - min_y

        padding_x = 120
        padding_y = 100
        scale_x: float = ((SCREEN_WIDTH - 2 * padding_x)
                          / map_width if map_width > 0 else 1.0)
        scale_y: float = ((SCREEN_HEIGHT - 2 * padding_y)
                          / map_height if map_height > 0 else 1.0)

        self.map_scale = min(scale_x, scale_y)

        self.offset_x = ((SCREEN_WIDTH - (map_width * self.map_scale)) / 2
                         - (min_x * self.map_scale))
        self.offset_y = ((SCREEN_HEIGHT - (map_height * self.map_scale)) / 2
                         - (min_y * self.map_scale) + 40)

    def on_draw(self) -> None:
        """Render the simulation screen."""
        self.clear()
        bg_rect = arcade.LRBT(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
        arcade.draw_texture_rect(self.background, bg_rect)

        sprite_size: float = max(45.0, 70.0 * self.map_scale)
        line_thickness: float = max(2.0, 8.0 * self.map_scale)
        roof_offset: float = sprite_size * 0.15

        drawn_links: set = set()
        for zone in self.zones:
            for link in zone.connection:
                if link not in drawn_links:
                    z1, z2 = link.zone1, link.zone2
                    x1: float = (z1.x * self.grid_x * self.map_scale
                                 + self.offset_x)
                    y1: float = (z1.y * self.grid_y * self.map_scale
                                 + self.offset_y + roof_offset)

                    x2: float = (z2.x * self.grid_x * self.map_scale
                                 + self.offset_x)
                    y2: float = (z2.y * self.grid_y * self.map_scale
                                 + self.offset_y + roof_offset)

                    bright_cable = (180, 200, 220, 220)
                    arcade.draw_line(
                        x1, y1, x2, y2, bright_cable, line_thickness)
                    drawn_links.add(link)

        for zone in self.zones:
            cx: float = zone.x * self.grid_x * self.map_scale + self.offset_x
            cy: float = zone.y * self.grid_y * self.map_scale + self.offset_y

            zone_color = arcade.color.WHITE
            if zone.type_zone == "restricted":
                zone_color = arcade.color.IMPERIAL_RED
            elif zone.type_zone == "priority":
                zone_color = arcade.color.SAE
            elif zone == self.scheduler.manager.start_zone:
                zone_color = arcade.color.EMERALD
            elif zone == self.scheduler.manager.end_zone:
                zone_color = arcade.color.GOLD

            zone_rect = arcade.XYWH(
                cx, cy, sprite_size, sprite_size)
            arcade.draw_texture_rect(
                self.zone_sprite, zone_rect, color=zone_color)

        progress: float = self.timer / self.turn_delay
        for drone in self.scheduler.drones:
            start_x: float = (drone.previous_zone.x * self.grid_x
                              * self.map_scale + self.offset_x)
            start_y: float = (drone.previous_zone.y * self.grid_y
                              * self.map_scale + self.offset_y)
            end_x: float = (drone.current_zone.x * self.grid_x
                            * self.map_scale + self.offset_x)
            end_y: float = (drone.current_zone.y * self.grid_y
                            * self.map_scale + self.offset_y)

            theorical_dx: float = start_x + (end_x - start_x) * progress
            theorical_dy: float = start_y + (end_y - start_y) * progress

            arrange_radius = 12 * self.map_scale
            angle = float(drone.id)

            dx: float = theorical_dx + math.cos(angle) * arrange_radius
            dy: float = theorical_dy + math.sin(angle) * arrange_radius

            drone_size: float = sprite_size * 0.7

            drone_rect = arcade.XYWH(dx, dy,
                                     drone_size, drone_size)
            arcade.draw_texture_rect(self.drone_sprite, drone_rect)

        arcade.draw_lrbt_rectangle_filled(
            20, 220, 660, 780, (50, 50, 50, 200))
        drones_arrived = 0
        for drone in self.scheduler.drones:
            if drone.current_zone == self.scheduler.manager.end_zone:
                drones_arrived += 1
        self.text_score.value = f"Score: {drones_arrived}"
        self.text_turn.value = f"Turn: {self.scheduler.total_turns}"
        self.text_mode.value = (
            "Mode: AUTO" if self.auto_mode else "Mode: MANUAL")

        if self.scheduler.is_finish():
            self.text_finish.draw()

        box_width = 250
        box_height = 170
        padding = 15

        rect_right: int = SCREEN_WIDTH - padding
        rect_left: int = rect_right - box_width
        rect_top: int = SCREEN_HEIGHT - padding
        rect_bottom: int = rect_top - box_height

        arcade.draw_lrbt_rectangle_filled(
            rect_left, rect_right, rect_bottom, rect_top, (50, 50, 50, 200)
        )

        text_x: int = rect_left + 15
        self.text_keybinds.x = text_x

        self.text_score.draw()
        self.text_turn.draw()
        self.text_keybinds.draw()
        self.text_mode.draw()
        self.text_r.draw()
        self.text_space.draw()
        self.text_esc.draw()

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
