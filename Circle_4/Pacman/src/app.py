"""Main application and graphical loop."""

import pygame

from src.config import GameConfig
from src.constants import (
    FPS,
    GAME_TITLE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from src.exceptions import HighscoreError, PacmanError
from src.game.game import Game, GameStatus
from src.services.highscore import HighscoreService
from src.ui.input_handler import InputHandler
from src.ui.renderer import Renderer
from src.ui.screens import Screen


class App:
    """Control the complete Pac-Man application."""

    MAIN_MENU_OPTIONS = (
        "START GAME",
        "VIEW HIGHSCORES",
        "INSTRUCTIONS",
        "EXIT",
    )

    PAUSE_OPTIONS = (
        "RESUME",
        "RETURN TO MAIN MENU",
    )

    def __init__(self, config: GameConfig) -> None:
        """Initialise the application."""

        pygame.init()
        pygame.display.set_caption(GAME_TITLE)

        self.config = config
        self.is_running = True

        self.screen_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        self.clock = pygame.time.Clock()

        self.renderer = Renderer(self.screen_surface)
        self.input_handler = InputHandler()
        self.game = Game(config)

        self.highscore_service = HighscoreService(
            config.highscore_filename
        )
        self.highscores = self.highscore_service.load()

        self.current_screen = Screen.MAIN_MENU
        self.main_menu_index = 0
        self.pause_menu_index = 0

        self.player_name = ""
        self.name_error = ""

        self.player_move_timer = 0.0
        self.base_player_move_interval = 0.12

    def run(self) -> None:
        """Run the main application loop."""

        try:
            while self.is_running:
                delta_time = self.clock.tick(FPS) / 1000.0

                self._handle_events()
                self._update(delta_time)
                self._render()
        finally:
            pygame.quit()

    def _handle_events(self) -> None:
        """Handle all Pygame events."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(
        self,
        event: pygame.event.Event,
    ) -> None:
        """Handle one keyboard event."""

        if self.current_screen == Screen.MAIN_MENU:
            self._handle_main_menu_key(event.key)
        elif self.current_screen == Screen.GAME:
            self._handle_game_key(event.key)
        elif self.current_screen == Screen.PAUSE:
            self._handle_pause_key(event.key)
        elif self.current_screen == Screen.HIGHSCORES:
            self._handle_information_screen_key(event.key)
        elif self.current_screen == Screen.INSTRUCTIONS:
            self._handle_information_screen_key(event.key)
        elif self.current_screen in {
            Screen.GAME_OVER,
            Screen.VICTORY,
        }:
            self._handle_end_screen_key(event.key)
        elif self.current_screen == Screen.NAME_ENTRY:
            self._handle_name_entry_key(event)

    def _handle_main_menu_key(self, key: int) -> None:
        """Handle main menu keyboard input."""

        if self.input_handler.is_up_key(key):
            self.main_menu_index = (
                self.main_menu_index - 1
            ) % len(self.MAIN_MENU_OPTIONS)
            return

        if self.input_handler.is_down_key(key):
            self.main_menu_index = (
                self.main_menu_index + 1
            ) % len(self.MAIN_MENU_OPTIONS)
            return

        if key == pygame.K_ESCAPE:
            self.is_running = False
            return

        if not self.input_handler.is_confirm_key(key):
            return

        if self.main_menu_index == 0:
            self._start_game()
        elif self.main_menu_index == 1:
            self.current_screen = Screen.HIGHSCORES
        elif self.main_menu_index == 2:
            self.current_screen = Screen.INSTRUCTIONS
        elif self.main_menu_index == 3:
            self.is_running = False

    def _handle_game_key(self, key: int) -> None:
        """Handle gameplay keyboard input."""

        if self.input_handler.is_pause_key(key):
            self.game.toggle_pause()
            self.pause_menu_index = 0
            self.current_screen = Screen.PAUSE
            return

        direction = self.input_handler.get_direction(key)

        if direction is not None:
            self.game.request_player_direction(direction)
            self.game.move_player()
            self.player_move_timer = 0.0
            return

        if key == pygame.K_F1:
            self.game.toggle_invincibility()
        elif key == pygame.K_F2:
            self.game.skip_level()
        elif key == pygame.K_F3:
            self.game.toggle_ghost_freeze()
        elif key == pygame.K_F4:
            self.game.add_extra_life()
        elif key == pygame.K_F5:
            self.game.toggle_speed_boost()

    def _handle_pause_key(self, key: int) -> None:
        """Handle pause menu keyboard input."""

        if self.input_handler.is_up_key(key):
            self.pause_menu_index = (
                self.pause_menu_index - 1
            ) % len(self.PAUSE_OPTIONS)
            return

        if self.input_handler.is_down_key(key):
            self.pause_menu_index = (
                self.pause_menu_index + 1
            ) % len(self.PAUSE_OPTIONS)
            return

        if key in {pygame.K_ESCAPE, pygame.K_p}:
            self._resume_game()
            return

        if not self.input_handler.is_confirm_key(key):
            return

        if self.pause_menu_index == 0:
            self._resume_game()
        else:
            self.game.status = GameStatus.READY
            self.current_screen = Screen.MAIN_MENU

    def _handle_information_screen_key(
        self,
        key: int,
    ) -> None:
        """Return from instructions or highscores."""

        if (
            self.input_handler.is_confirm_key(key)
            or key == pygame.K_ESCAPE
        ):
            self.current_screen = Screen.MAIN_MENU

    def _handle_end_screen_key(self, key: int) -> None:
        """Handle victory or game-over input."""

        if self.input_handler.is_confirm_key(key):
            self.player_name = ""
            self.name_error = ""
            self.current_screen = Screen.NAME_ENTRY

    def _handle_name_entry_key(
        self,
        event: pygame.event.Event,
    ) -> None:
        """Handle player-name input."""

        if event.key == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
            self.name_error = ""
            return

        if event.key in {
            pygame.K_RETURN,
            pygame.K_KP_ENTER,
        }:
            self._save_highscore()
            return

        character = event.unicode

        if (
            len(self.player_name)
            < HighscoreService.MAX_NAME_LENGTH
            and (
                character.isalnum()
                or character == " "
            )
        ):
            self.player_name += character
            self.name_error = ""

    def _start_game(self) -> None:
        """Start a new game."""

        try:
            self.game.start()
        except PacmanError as error:
            print(f"Unable to start the game: {error}")
            self.current_screen = Screen.MAIN_MENU
            return

        self.player_move_timer = 0.0
        self.player_name = ""
        self.name_error = ""
        self.current_screen = Screen.GAME

    def _resume_game(self) -> None:
        """Resume the paused game."""

        self.game.toggle_pause()
        self.current_screen = Screen.GAME

    def _save_highscore(self) -> None:
        """Validate and save the final score."""

        try:
            self.highscore_service.add(
                name=self.player_name,
                score=self.game.score,
            )
        except HighscoreError as error:
            self.name_error = str(error)
            return

        self.highscores = self.highscore_service.load()
        self.game.status = GameStatus.READY
        self.current_screen = Screen.MAIN_MENU

    def _update(self, delta_time: float) -> None:
        """Update the active game state."""

        if self.current_screen != Screen.GAME:
            return

        self.player_move_timer += delta_time

        movement_interval = self.base_player_move_interval

        if self.game.player is not None:
            movement_interval /= self.game.player.speed

        while self.player_move_timer >= movement_interval:
            self.player_move_timer -= movement_interval
            self.game.move_player()

        self.game.update(delta_time)
        self._check_game_status()

    def _check_game_status(self) -> None:
        """Change screen after victory or defeat."""

        if self.game.status == GameStatus.LOST:
            self.current_screen = Screen.GAME_OVER
        elif self.game.status == GameStatus.WON:
            self.current_screen = Screen.VICTORY

    def _render(self) -> None:
        """Render the current application screen."""

        if self.current_screen == Screen.MAIN_MENU:
            self.renderer.draw_main_menu(
                highscores=self.highscores,
                options=self.MAIN_MENU_OPTIONS,
                selected_index=self.main_menu_index,
            )
        elif self.current_screen == Screen.GAME:
            self._render_game()
        elif self.current_screen == Screen.PAUSE:
            self._render_game()
            self.renderer.draw_pause(
                options=self.PAUSE_OPTIONS,
                selected_index=self.pause_menu_index,
            )
        elif self.current_screen == Screen.HIGHSCORES:
            self.renderer.draw_highscores(
                self.highscores
            )
        elif self.current_screen == Screen.INSTRUCTIONS:
            self.renderer.draw_instructions()
        elif self.current_screen == Screen.GAME_OVER:
            self.renderer.draw_end_screen(
                title="GAME OVER",
                score=self.game.score,
            )
        elif self.current_screen == Screen.VICTORY:
            self.renderer.draw_end_screen(
                title="YOU WIN!",
                score=self.game.score,
            )
        elif self.current_screen == Screen.NAME_ENTRY:
            self.renderer.draw_name_entry(
                name=self.player_name,
                score=self.game.score,
                error_message=self.name_error,
            )

        self.renderer.present()

    def _render_game(self) -> None:
        """Render the active level."""

        if (
            self.game.level is None
            or self.game.player is None
        ):
            return

        self.renderer.draw_game(
            level=self.game.level,
            player=self.game.player,
            ghosts=self.game.ghosts,
            score=self.game.score,
            total_levels=len(self.config.levels),
            ghosts_frozen=self.game.ghosts_frozen,
        )
