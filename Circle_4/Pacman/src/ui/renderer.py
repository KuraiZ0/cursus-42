"""Pygame rendering service."""

import pygame

from src.constants import (
    BLACK,
    BLUE,
    RED,
    TILE_SIZE,
    WHITE,
    YELLOW,
)
from src.entities.collectible import CollectibleType
from src.entities.entity import Position
from src.entities.ghost import Ghost, GhostState
from src.entities.player import Player
from src.game.level import Level
from src.game.maze import Tile
from src.services.highscore import HighscoreEntry


class Renderer:
    """Render menus, levels, entities and information."""

    def __init__(
        self,
        screen: pygame.Surface,
    ) -> None:
        """Initialise the renderer."""

        self.screen = screen
        self.title_font = pygame.font.Font(None, 82)
        self.menu_font = pygame.font.Font(None, 42)
        self.text_font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)

    def clear(self) -> None:
        """Clear the screen."""

        self.screen.fill(BLACK)

    def present(self) -> None:
        """Display the completed frame."""

        pygame.display.flip()

    def draw_main_menu(
        self,
        highscores: list[HighscoreEntry],
        options: tuple[str, ...],
        selected_index: int,
    ) -> None:
        """Draw the main menu."""

        self.clear()

        self._draw_centered_text(
            text="PAC-MAN",
            font=self.title_font,
            colour=YELLOW,
            y=80,
        )

        for index, option in enumerate(options):
            colour = YELLOW if index == selected_index else WHITE
            prefix = "> " if index == selected_index else "  "

            self._draw_centered_text(
                text=f"{prefix}{option}",
                font=self.menu_font,
                colour=colour,
                y=190 + index * 55,
            )

        self._draw_centered_text(
            text="BEST SCORES",
            font=self.text_font,
            colour=YELLOW,
            y=445,
        )

        if not highscores:
            self._draw_centered_text(
                text="No highscore yet",
                font=self.small_font,
                colour=WHITE,
                y=485,
            )
        else:
            for index, entry in enumerate(highscores[:5]):
                text = (
                    f"{index + 1}. {entry.name} "
                    f"- {entry.score} pts"
                )

                self._draw_centered_text(
                    text=text,
                    font=self.small_font,
                    colour=WHITE,
                    y=485 + index * 28,
                )

        self._draw_centered_text(
            text="Use UP/DOWN and ENTER",
            font=self.small_font,
            colour=WHITE,
            y=self.screen.get_height() - 25,
        )

    def draw_highscores(
        self,
        highscores: list[HighscoreEntry],
    ) -> None:
        """Draw the complete highscore screen."""

        self.clear()

        self._draw_centered_text(
            text="HIGHSCORES",
            font=self.title_font,
            colour=YELLOW,
            y=80,
        )

        if not highscores:
            self._draw_centered_text(
                text="No saved score",
                font=self.menu_font,
                colour=WHITE,
                y=250,
            )

        for index, entry in enumerate(highscores[:10]):
            text = (
                f"{index + 1:2}. "
                f"{entry.name:<10} "
                f"{entry.score:>8} pts"
            )

            self._draw_centered_text(
                text=text,
                font=self.text_font,
                colour=WHITE,
                y=160 + index * 42,
            )

        self._draw_centered_text(
            text="Press ESC or ENTER to return",
            font=self.small_font,
            colour=WHITE,
            y=self.screen.get_height() - 35,
        )

    def draw_instructions(self) -> None:
        """Draw game instructions and controls."""

        self.clear()

        self._draw_centered_text(
            text="INSTRUCTIONS",
            font=self.title_font,
            colour=YELLOW,
            y=70,
        )

        instructions = (
            "Eat every pacgum to finish the level.",
            "Avoid ghosts while they are dangerous.",
            "Super-pacgums make ghosts edible.",
            "Complete all levels before losing every life.",
            "",
            "Arrow keys / WASD: Move",
            "P or ESC: Pause",
            "F1: Invincibility",
            "F2: Skip level",
            "F3: Freeze ghosts",
            "F4: Add one life",
            "F5: Speed boost",
        )

        for index, instruction in enumerate(instructions):
            colour = YELLOW if instruction.startswith("F") else WHITE

            self._draw_centered_text(
                text=instruction,
                font=self.text_font,
                colour=colour,
                y=145 + index * 40,
            )

        self._draw_centered_text(
            text="Press ESC or ENTER to return",
            font=self.small_font,
            colour=WHITE,
            y=self.screen.get_height() - 30,
        )

    def draw_game(
        self,
        level: Level,
        player: Player,
        ghosts: list[Ghost],
        score: int,
        total_levels: int,
        ghosts_frozen: bool,
    ) -> None:
        """Draw the complete game view."""

        self.clear()

        tile_size = self._calculate_tile_size(level)

        maze_width = level.maze.width * tile_size
        maze_height = level.maze.height * tile_size

        offset_x = (
            self.screen.get_width() - maze_width
        ) // 2

        available_height = self.screen.get_height() - 110
        offset_y = 45 + max(
            0,
            (available_height - maze_height) // 2,
        )

        self._draw_maze(
            level=level,
            offset_x=offset_x,
            offset_y=offset_y,
            tile_size=tile_size,
        )
        self._draw_player(
            player=player,
            offset_x=offset_x,
            offset_y=offset_y,
            tile_size=tile_size,
        )
        self._draw_ghosts(
            ghosts=ghosts,
            offset_x=offset_x,
            offset_y=offset_y,
            tile_size=tile_size,
        )
        self._draw_hud(
            level=level,
            player=player,
            score=score,
            total_levels=total_levels,
        )
        self._draw_cheat_status(
            player=player,
            ghosts_frozen=ghosts_frozen,
        )

    def draw_pause(
        self,
        options: tuple[str, ...],
        selected_index: int,
    ) -> None:
        """Draw the pause menu."""

        overlay = pygame.Surface(
            self.screen.get_size(),
            pygame.SRCALPHA,
        )
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))

        self._draw_centered_text(
            text="PAUSED",
            font=self.title_font,
            colour=YELLOW,
            y=220,
        )

        for index, option in enumerate(options):
            colour = YELLOW if index == selected_index else WHITE
            prefix = "> " if index == selected_index else "  "

            self._draw_centered_text(
                text=f"{prefix}{option}",
                font=self.menu_font,
                colour=colour,
                y=330 + index * 65,
            )

    def draw_end_screen(
        self,
        title: str,
        score: int,
    ) -> None:
        """Draw a victory or game-over screen."""

        self.clear()

        self._draw_centered_text(
            text=title,
            font=self.title_font,
            colour=YELLOW,
            y=180,
        )
        self._draw_centered_text(
            text=f"Final score: {score}",
            font=self.menu_font,
            colour=WHITE,
            y=300,
        )
        self._draw_centered_text(
            text="Press ENTER to save your score",
            font=self.text_font,
            colour=WHITE,
            y=390,
        )

    def draw_name_entry(
        self,
        name: str,
        score: int,
        error_message: str = "",
    ) -> None:
        """Draw the player-name entry screen."""

        self.clear()

        self._draw_centered_text(
            text="SAVE HIGHSCORE",
            font=self.title_font,
            colour=YELLOW,
            y=140,
        )
        self._draw_centered_text(
            text=f"Score: {score}",
            font=self.menu_font,
            colour=WHITE,
            y=260,
        )
        self._draw_centered_text(
            text=f"Name: {name}_",
            font=self.menu_font,
            colour=WHITE,
            y=340,
        )
        self._draw_centered_text(
            text="Maximum 10 letters, numbers or spaces",
            font=self.text_font,
            colour=WHITE,
            y=420,
        )

        if error_message:
            self._draw_centered_text(
                text=error_message,
                font=self.small_font,
                colour=RED,
                y=470,
            )

    def _calculate_tile_size(self, level: Level) -> int:
        """Calculate a tile size fitting inside the window."""

        available_width = self.screen.get_width() - 30
        available_height = self.screen.get_height() - 130

        width_size = available_width // level.maze.width
        height_size = available_height // level.maze.height

        return max(
            6,
            min(TILE_SIZE, width_size, height_size),
        )

    def _draw_maze(
        self,
        level: Level,
        offset_x: int,
        offset_y: int,
        tile_size: int,
    ) -> None:
        """Draw maze tiles and collectibles."""

        for row in range(level.maze.height):
            for column in range(level.maze.width):
                position = Position(
                    row=row,
                    column=column,
                )
                tile = level.maze.tile_at(position)

                rectangle = pygame.Rect(
                    offset_x + column * tile_size,
                    offset_y + row * tile_size,
                    tile_size,
                    tile_size,
                )

                colour = BLUE if tile == Tile.WALL else BLACK

                pygame.draw.rect(
                    self.screen,
                    colour,
                    rectangle,
                )

        for collectible in level.collectibles.values():
            if collectible.eaten:
                continue

            center = (
                offset_x
                + collectible.position.column * tile_size
                + tile_size // 2,
                offset_y
                + collectible.position.row * tile_size
                + tile_size // 2,
            )

            if (
                collectible.collectible_type
                == CollectibleType.SUPER_PACGUM
            ):
                radius = max(3, tile_size // 4)
            else:
                radius = max(1, tile_size // 10)

            pygame.draw.circle(
                self.screen,
                WHITE,
                center,
                radius,
            )

    def _draw_player(
        self,
        player: Player,
        offset_x: int,
        offset_y: int,
        tile_size: int,
    ) -> None:
        """Draw Pac-Man."""

        center = (
            offset_x
            + player.position.column * tile_size
            + tile_size // 2,
            offset_y
            + player.position.row * tile_size
            + tile_size // 2,
        )

        pygame.draw.circle(
            self.screen,
            YELLOW,
            center,
            max(3, tile_size // 2 - 2),
        )

    def _draw_ghosts(
        self,
        ghosts: list[Ghost],
        offset_x: int,
        offset_y: int,
        tile_size: int,
    ) -> None:
        """Draw all active ghosts."""

        colours = (
            RED,
            (255, 105, 180),
            (0, 255, 255),
            (255, 165, 0),
        )

        for index, ghost in enumerate(ghosts):
            if ghost.state == GhostState.EATEN:
                continue

            colour = colours[index % len(colours)]

            if ghost.state == GhostState.FRIGHTENED:
                colour = BLUE

            margin = max(2, tile_size // 8)

            rectangle = pygame.Rect(
                offset_x
                + ghost.position.column * tile_size
                + margin,
                offset_y
                + ghost.position.row * tile_size
                + margin,
                tile_size - margin * 2,
                tile_size - margin * 2,
            )

            pygame.draw.rect(
                self.screen,
                colour,
                rectangle,
                border_radius=max(2, tile_size // 4),
            )

    def _draw_hud(
        self,
        level: Level,
        player: Player,
        score: int,
        total_levels: int,
    ) -> None:
        """Draw score, lives, level and time."""

        text = (
            f"Score: {score}    "
            f"Lives: {player.lives}    "
            f"Level: {level.number}/{total_levels}    "
            f"Time: {int(level.remaining_time)}"
        )

        surface = self.small_font.render(
            text,
            True,
            WHITE,
        )

        rectangle = surface.get_rect(
            center=(self.screen.get_width() // 2, 20)
        )

        self.screen.blit(surface, rectangle)

    def _draw_cheat_status(
        self,
        player: Player,
        ghosts_frozen: bool,
    ) -> None:
        """Display active cheat modes."""

        active_cheats: list[str] = []

        if player.invincible:
            active_cheats.append("INVINCIBLE")

        if ghosts_frozen:
            active_cheats.append("GHOSTS FROZEN")

        if player.speed_boosted:
            active_cheats.append("SPEED BOOST")

        if not active_cheats:
            return

        text = "CHEAT: " + " | ".join(active_cheats)

        surface = self.small_font.render(
            text,
            True,
            YELLOW,
        )

        rectangle = surface.get_rect(
            center=(
                self.screen.get_width() // 2,
                self.screen.get_height() - 18,
            )
        )

        self.screen.blit(surface, rectangle)

    def _draw_centered_text(
        self,
        text: str,
        font: pygame.font.Font,
        colour: tuple[int, int, int],
        y: int,
    ) -> None:
        """Draw horizontally centred text."""

        surface = font.render(
            text,
            True,
            colour,
        )
        rectangle = surface.get_rect(
            center=(self.screen.get_width() // 2, y)
        )
        self.screen.blit(surface, rectangle)
