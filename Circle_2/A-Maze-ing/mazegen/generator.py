"""This module provides the MazeGenerator class for creating mazes."""
from typing import Any
from random import seed as sd, choice
import time
import sys


class MazeGenerator:
    """Generates a maze using a recursive backtracking algorithm."""

    def __init__(
         self, width: int, height: int, start: tuple, end: tuple,
         seed: int | None = None) -> None:
        """
        Initialize the MazeGenerator with specified dimensions.

        Args:
            width (int): The width of the maze.
            height (int): The height of the maze.
            start (tuple): The (x, y) coordinates of the starting cell.
            end (tuple): The (x, y) coordinates of the ending cell.
            seed (int | None): An optional seed for the random number.
        """
        self.width = width
        self.height = height
        self.seed = seed
        sd(self.seed)
        self.grid: list[list[int]] = [[15 for _ in range(width)]
                                      for _ in range(height)]
        self.visited: list[list[bool]] = [[False for _ in range(width)]
                                          for _ in range(height)]
        # FIX: utiliser les paramètres start/end au lieu de les hardcoder
        self.start = start
        self.end = end

        self._reserve_42()

    def _reserve_42(self) -> None:
        """Reserve 42 pattern in the maze grid by marking cells as visited."""
        if self.width < 7 or self.height < 5:
            print("Error: Maze too small for the '42' pattern.")
            return
        x_off: int = (self.width - 7) // 2
        y_off: int = (self.height - 5) // 2

        four: list[tuple[int, int]] = [
            (0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1),
            (2, 2), (2, 3), (2, 4)]
        two: list[tuple[int, int]] = [
            (4, 0), (5, 0), (6, 0), (6, 1), (6, 2), (5, 2),
            (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]

        for dx, dy in four + two:
            self.visited[y_off + dy][x_off + dx] = True

    def _break_wall(self, x1: int, x2: int, y1: int, y2: int) -> None:
        """Break the wall between two adjacent cells."""
        # Nord=1, Est=2, Sud=4, Ouest=8
        dx: int = x2 - x1
        dy: int = y2 - y1
        if dx == 1:
            self.grid[y1][x1] -= 2
            self.grid[y2][x2] -= 8
        elif dx == -1:
            self.grid[y1][x1] -= 8
            self.grid[y2][x2] -= 2
        elif dy == 1:
            self.grid[y1][x1] -= 4
            self.grid[y2][x2] -= 1
        elif dy == -1:
            self.grid[y1][x1] -= 1
            self.grid[y2][x2] -= 4

    def _neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return a list of unvisited neighbors for a given cell."""
        neighbors: list[tuple[int, int]] = []
        candidates: list[tuple[int, int]] = [
            (x, y - 1),  # Nord
            (x, y + 1),  # Sud
            (x + 1, y),  # Est
            (x - 1, y)   # Ouest
        ]
        for nx, ny in candidates:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[ny][nx]:
                    neighbors.append((nx, ny))
        return neighbors

    def _display_frame(self, current: tuple[int, int] | None,
                       stack_set: set[tuple[int, int]],
                       color: str = "37") -> None:
        """Display a frame of the generation animation."""
        C: str = f"\033[{color}m"
        R = "\033[0m"

        lines: list[str] = []
        lines.append(C + "  " + "____" * self.width + R)
        for y in range(self.height):
            line_a: str = C + "| " + R
            line_b: str = C + "| " + R
            for x in range(self.width):
                val: int = self.grid[y][x]
                if (x, y) == self.start:
                    sym = "\033[92m S \033[0m"
                elif (x, y) == self.end:
                    sym = "\033[91m E \033[0m"
                elif (x, y) == current:
                    sym = "\033[93m @ \033[0m"
                elif (x, y) in stack_set:
                    sym = "\033[35m · \033[0m"
                elif self.visited[y][x]:
                    sym = "   "
                else:
                    sym = C + "███" + R
                line_a += sym + (C + "|" + R if val & 2 else " ")
                line_b += (C + "___" + R if val & 4 else "   ")
                line_b += (C + "|" + R if val & 2 else " ")
            lines.append(line_a)
            lines.append(line_b)

        total_lines: int = self.height * 2 + 1
        sys.stdout.write(f"\033[{total_lines}A")
        sys.stdout.write("\n".join(lines) + "\n")
        sys.stdout.flush()

    def generate(
            self, start_x: int = None, start_y: int = None,
            animate: bool = False, delay: float = 0.01) -> None:
        """
        Generate the maze using a recursive backtracking algorithm.

        Args:
            start_x (int, optional): The starting X coordinate for generation.
            start_y (int, optional): The starting Y coordinate for generation.
            animate (bool, optional): If True, displays the generation process.
            delay (float, optional): Delay in seconds between animation frames.
        """
        if start_x is None or start_y is None:
            start_x, start_y = self.start
        stack: list[tuple[int, int]] = [(start_x, start_y)]
        self.visited[start_y][start_x] = True

        if animate:
            print("\033[2J\033[H", end="")
            print("\n  \033[1mGénération en cours...\033[0m\n")
            total_lines: int = self.height * 2 + 1
            print("\n" * total_lines, end="")

        step = 0
        while stack:
            cur_x, cur_y = stack[-1]
            possible_neighbors: list[Any] = self._neighbors(cur_x, cur_y)
            if possible_neighbors:
                nx, ny = choice(possible_neighbors)
                self._break_wall(cur_x, nx, cur_y, ny)
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

            if animate:
                step += 1
                skip = max(1, (self.width * self.height) // 200)
                if step % skip == 0 or not stack:
                    stack_set = set(stack)
                    current = stack[-1] if stack else None
                    self._display_frame(current, stack_set)
                    time.sleep(delay)

        if animate:
            self._display_frame(None, set())
            print("\n  \033[92m✓ Génération terminée !\033[0m")
            time.sleep(0.1)

    def display(self, path_str: str = "", color: str = "37", char: str = "#"):
        """
        Display the maze in the console, optionally showing a path.

        Args:
            path_str (str, optional): A string representing the path.
            color (str, optional): ANSI color code for the maze walls.
            char (str, optional): Character to use for drawing the path.
        """
        C: str = f"\033[{color}m"
        R = "\033[0m"
        path_coords: set[Any] = set()
        if path_str:
            cx, cy = self.start
            path_coords.add((cx, cy))
            mv: dict[str, tuple[int, int]] = {
                'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
            for m in path_str:
                dx, dy = mv[m]
                cx, cy = cx + dx, cy + dy
                path_coords.add((cx, cy))

        print(C + "  " + "____" * self.width + R)
        for y in range(self.height):
            line_a: str = C + "| " + R
            line_b: str = C + "| " + R
            for x in range(self.width):
                val: int = self.grid[y][x]
                if (x, y) == self.start:
                    sym = "\033[92m S \033[0m"
                elif (x, y) == self.end:
                    sym = "\033[91m E \033[0m"
                elif (x, y) in path_coords:
                    sym: str = f"\033[94m {char} \033[0m"
                else:
                    sym = "   "

                line_a += sym + (C + "|" + R if val & 2 else " ")
                line_b += (C + "___" + R if val & 4 else "   ")
                line_b += (C + "|" + R if val & 2 else " ")
            print(line_a)
            print(line_b)

    def save_to_file(self, filename: str, path_str: str | None) -> None:
        """
        Save the generated maze to a file.

        Args:
            filename (str): The name of the file to save the maze to.
            path_str (str | None): An string representing the path to save.
        """
        try:
            with open(filename, 'w') as f:
                for row in self.grid:
                    hex_row = "".join(hex(cell)[2:].upper() for cell in row)
                    f.write(hex_row + "\n")

                f.write("\n")

                f.write(f"{self.start[0]},{self.start[1]}\n")
                f.write(f"{self.end[0]},{self.end[1]}\n")

                f.write(f"{path_str if path_str else ''}\n")

        except IOError as e:
            print(f"Error writing to {filename}: {e}")
