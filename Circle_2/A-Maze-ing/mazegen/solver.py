"""Module for solving mazes using BFS algorithm."""
from collections import deque
from typing import Optional


class MazeSolver:
    """Class to find the shortest path in a hexadecimal maze."""

    def __init__(self, grid: list[list[int]], start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        """Initialize the solver with grid, start and end points."""
        self.grid = grid
        self.start = start
        self.end = end
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0

    def solve(self) -> Optional[str]:
        """Solve the maze and return the path as a string (N, E, S, W)."""
        queue: deque[tuple[int, int, str]] = deque([(self.start[0],
                                                    self.start[1], "")])
        visited: set[tuple[int, int]] = {self.start}

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == self.end:
                return path

            val: int = self.grid[y][x]
            directions: list[tuple[int, int, str, int]] = [
                (0, -1, 'N', 1),  # Nord
                (1, 0, 'E', 2),   # Est
                (0, 1, 'S', 4),   # Sud
                (-1, 0, 'W', 8)   # Ouest
            ]

            for dx, dy, char, mask in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited and (val & mask) == 0:
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + char))
        return None
