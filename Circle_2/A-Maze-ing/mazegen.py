# =========================
# File: mazegen.py
# =========================
"""
Maze generator reusable module.

Example
-------
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    seed=1234,
    perfect=True,
)
maze = gen.generate()
print("\\n".join(maze.to_hex_lines()))
print(gen.shortest_path_directions())
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from random import Random
from typing import Dict, List, Optional, Set, Tuple

Coord = Tuple[int, int]


class MazeError(Exception):
    """Raised for maze generation and validation errors."""


class Dir(Enum):
    """Cardinal directions with wall-bit mapping and deltas."""
    N = (0, -1, 1 << 0)
    E = (1, 0, 1 << 1)
    S = (0, 1, 1 << 2)
    W = (-1, 0, 1 << 3)

    @property
    def dx(self) -> int:
        return int(self.value[0])

    @property
    def dy(self) -> int:
        return int(self.value[1])

    @property
    def bit(self) -> int:
        return int(self.value[2])

    @property
    def letter(self) -> str:
        return self.name

    def opposite(self) -> "Dir":
        if self is Dir.N:
            return Dir.S
        if self is Dir.S:
            return Dir.N
        if self is Dir.E:
            return Dir.W
        return Dir.E


@dataclass(frozen=True)
class Maze:
    """
    Maze structure as per-cell wall bitmask.

    Each cell stores 4 bits:
      bit0 N, bit1 E, bit2 S, bit3 W
    bit=1 => wall closed, bit=0 => open.

    Blocked cells (e.g. "42" pattern) are represented by mask=0xF.
    """
    width: int
    height: int
    walls: List[List[int]]  # walls[y][x]
    entry: Coord
    exit: Coord
    blocked: Set[Coord]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def is_blocked(self, x: int, y: int) -> bool:
        return (x, y) in self.blocked

    def wall_mask(self, x: int, y: int) -> int:
        return self.walls[y][x] & 0xF

    def is_open_edge(self, x: int, y: int, d: Dir) -> bool:
        if self.is_blocked(x, y):
            return False
        nx, ny = x + d.dx, y + d.dy
        if not self.in_bounds(nx, ny) or self.is_blocked(nx, ny):
            return False
        return (self.wall_mask(x, y) & d.bit) == 0

    def to_hex_lines(self) -> List[str]:
        """Return maze as list of strings, one row per line, hex per cell."""
        return ["".join(format(self.wall_mask(x, y), "X") for x in range(self.width))
                for y in range(self.height)]


def _parse_digit_pattern_5x5(digit: str) -> List[str]:
    """Return 5x5 bitmap for '4' or '2'. '1' means blocked cell."""
    if digit == "4":
        return [
            "10010",
            "10010",
            "11110",
            "00010",
            "00010",
        ]
    if digit == "2":
        return [
            "11110",
            "00010",
            "11110",
            "10000",
            "11110",
        ]
    raise MazeError(f"Unsupported digit for pattern: {digit}")


def build_42_blocked_cells(width: int, height: int, entry: Coord, exit: Coord) -> Set[Coord]:
    """
    Build a centered "42" pattern as blocked cells (fully closed).
    Returns empty set if maze too small or pattern would conflict.
    """
    pat4 = _parse_digit_pattern_5x5("4")
    pat2 = _parse_digit_pattern_5x5("2")

    pat_h = 5
    pat_w = 5 + 1 + 5
    if width < pat_w or height < pat_h:
        return set()

    ox = (width - pat_w) // 2
    oy = (height - pat_h) // 2

    blocked: Set[Coord] = set()
    for dy in range(pat_h):
        for dx in range(5):
            if pat4[dy][dx] == "1":
                blocked.add((ox + dx, oy + dy))
        for dx in range(5):
            if pat2[dy][dx] == "1":
                blocked.add((ox + 6 + dx, oy + dy))

    if entry in blocked or exit in blocked:
        return set()

    return blocked


class MazeGenerator:
    """
    Maze generator with reproducible randomness.

    Parameters
    ----------
    width, height:
        Maze size in cells.
    entry, exit:
        Coordinates (x, y) inside bounds; must be different.
    seed:
        Random seed for reproducibility.
    perfect:
        If True, maze is perfect (unique path between any two open cells).
        If False, extra openings are added carefully.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: Coord,
        exit: Coord,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.seed = seed
        self.perfect = perfect

        self._rng = Random(seed)
        self._maze: Optional[Maze] = None
        self._validate_params()

    def _validate_params(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise MazeError("WIDTH and HEIGHT must be positive integers.")
        ex, ey = self.entry
        ox, oy = self.exit
        if not (0 <= ex < self.width and 0 <= ey < self.height):
            raise MazeError("ENTRY out of bounds.")
        if not (0 <= ox < self.width and 0 <= oy < self.height):
            raise MazeError("EXIT out of bounds.")
        if self.entry == self.exit:
            raise MazeError("ENTRY and EXIT must be different.")

    def generate(self) -> Maze:
        """
        Generate a new maze and store it internally.

        Returns
        -------
        Maze
            Generated maze.
        """
        blocked = build_42_blocked_cells(self.width, self.height, self.entry, self.exit)
        if blocked and not self._open_cells_connected(blocked):
            blocked = set()

        walls: List[List[int]] = [[0xF for _ in range(self.width)] for _ in range(self.height)]
        for bx, by in blocked:
            walls[by][bx] = 0xF

        open_cells = [(x, y) for y in range(self.height) for x in range(self.width) if (x, y) not in blocked]
        if not open_cells:
            raise MazeError("All cells are blocked; cannot generate maze.")

        start = self.entry if self.entry in open_cells else open_cells[0]
        self._carve_perfect_maze(walls, blocked, start)

        if not self.perfect:
            self._add_imperfections(walls, blocked)

        self._maze = Maze(
            width=self.width,
            height=self.height,
            walls=walls,
            entry=self.entry,
            exit=self.exit,
            blocked=blocked,
        )

        if not self._path_exists():
            raise MazeError("Generated maze has no path from ENTRY to EXIT (unexpected).")

        return self._maze

    def maze(self) -> Maze:
        """Return last generated maze, or raise if not generated yet."""
        if self._maze is None:
            raise MazeError("Maze not generated yet. Call generate() first.")
        return self._maze

    def shortest_path_directions(self) -> str:
        """Return shortest path from entry to exit as a string of N/E/S/W."""
        maze = self.maze()
        path = self._bfs_path(maze.entry, maze.exit)
        return "".join(d.letter for d in path)

    def _neighbors(self, x: int, y: int, blocked: Set[Coord]) -> List[Tuple[Dir, int, int]]:
        out: List[Tuple[Dir, int, int]] = []
        for d in (Dir.N, Dir.E, Dir.S, Dir.W):
            nx, ny = x + d.dx, y + d.dy
            if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in blocked:
                out.append((d, nx, ny))
        return out

    def _open_cells_connected(self, blocked: Set[Coord]) -> bool:
        open_cells = {(x, y) for y in range(self.height) for x in range(self.width) if (x, y) not in blocked}
        if not open_cells:
            return False

        start = self.entry if self.entry in open_cells else next(iter(open_cells))
        stack = [start]
        seen = {start}

        while stack:
            x, y = stack.pop()
            for _, nx, ny in self._neighbors(x, y, blocked):
                if (nx, ny) not in seen:
                    seen.add((nx, ny))
                    stack.append((nx, ny))

        return seen == open_cells

    def _carve_open(self, walls: List[List[int]], x: int, y: int, d: Dir) -> None:
        nx, ny = x + d.dx, y + d.dy
        walls[y][x] &= ~d.bit
        walls[ny][nx] &= ~d.opposite().bit

    def _carve_perfect_maze(self, walls: List[List[int]], blocked: Set[Coord], start: Coord) -> None:
        visited: Set[Coord] = {start}
        stack: List[Coord] = [start]

        while stack:
            x, y = stack[-1]
            nbrs = [(d, nx, ny) for (d, nx, ny) in self._neighbors(x, y, blocked) if (nx, ny) not in visited]
            if not nbrs:
                stack.pop()
                continue
            d, nx, ny = self._rng.choice(nbrs)
            self._carve_open(walls, x, y, d)
            visited.add((nx, ny))
            stack.append((nx, ny))

        open_cells = {(x, y) for y in range(self.height) for x in range(self.width) if (x, y) not in blocked}
        if visited != open_cells:
            raise MazeError("Open cells are not fully reachable; blocked pattern likely disconnected space.")

    def _edge_is_closed(self, walls: List[List[int]], x: int, y: int, d: Dir) -> bool:
        return (walls[y][x] & d.bit) != 0

    def _would_create_open_3x3(self, walls: List[List[int]]) -> bool:
        for ty in range(self.height - 2):
            for tx in range(self.width - 2):
                if self._region_is_fully_open(walls, tx, ty):
                    return True
        return False

    def _region_is_fully_open(self, walls: List[List[int]], tx: int, ty: int) -> bool:
        for y in range(ty, ty + 3):
            for x in range(tx, tx + 2):
                if (walls[y][x] & Dir.E.bit) != 0:
                    return False
        for y in range(ty, ty + 2):
            for x in range(tx, tx + 3):
                if (walls[y][x] & Dir.S.bit) != 0:
                    return False
        return True

    def _add_imperfections(self, walls: List[List[int]], blocked: Set[Coord]) -> None:
        candidates: List[Tuple[int, int, Dir]] = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in blocked:
                    continue
                for d in (Dir.E, Dir.S):
                    nx, ny = x + d.dx, y + d.dy
                    if 0 <= nx < self.width and 0 <= ny < self.height and (nx, ny) not in blocked:
                        if self._edge_is_closed(walls, x, y, d):
                            candidates.append((x, y, d))

        self._rng.shuffle(candidates)
        target = max(1, (self.width * self.height) // 25)
        opened = 0

        for x, y, d in candidates:
            if opened >= target:
                break

            old_a = walls[y][x]
            nx, ny = x + d.dx, y + d.dy
            old_b = walls[ny][nx]

            self._carve_open(walls, x, y, d)
            if self._would_create_open_3x3(walls):
                walls[y][x] = old_a
                walls[ny][nx] = old_b
                continue

            opened += 1

    def _bfs_path(self, start: Coord, goal: Coord) -> List[Dir]:
        maze = self.maze()
        if start in maze.blocked or goal in maze.blocked:
            raise MazeError("ENTRY or EXIT is blocked; cannot pathfind.")

        queue: List[Coord] = [start]
        prev: Dict[Coord, Tuple[Coord, Dir]] = {}
        seen: Set[Coord] = {start}
        qi = 0

        while qi < len(queue):
            x, y = queue[qi]
            qi += 1
            if (x, y) == goal:
                break

            for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                if not maze.is_open_edge(x, y, d):
                    continue
                nx, ny = x + d.dx, y + d.dy
                if (nx, ny) in seen:
                    continue
                seen.add((nx, ny))
                prev[(nx, ny)] = ((x, y), d)
                queue.append((nx, ny))

        if goal not in seen:
            raise MazeError("No path found from ENTRY to EXIT.")

        path_rev: List[Dir] = []
        cur = goal
        while cur != start:
            p, d = prev[cur]
            path_rev.append(d)
            cur = p
        path_rev.reverse()
        return path_rev

    def _path_exists(self) -> bool:
        try:
            _ = self.shortest_path_directions()
            return True
        except MazeError:
            return False


