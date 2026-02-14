

# =========================
# File: a_maze_ing.py
# =========================
"""
Main program for A-Maze-ing.

Usage
-----
python3 a_maze_ing.py config.txt

Config keys (mandatory)
-----------------------
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True

Optional
--------
SEED=1234
DISPLAY=NONE | TERMINAL
"""

from __future__ import annotations

import curses
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

from mazegen import Dir, MazeError, MazeGenerator

Coord = Tuple[int, int]


@dataclass(frozen=True)
class Config:
    width: int
    height: int
    entry: Coord
    exit: Coord
    output_file: Path
    perfect: bool
    seed: Optional[int]
    display: str


class ConfigError(Exception):
    """Raised for configuration parsing/validation errors."""


def _parse_bool(value: str) -> bool:
    v: str = value.strip().lower()
    if v in {"true", "1", "yes", "y"}:
        return True
    if v in {"false", "0", "no", "n"}:
        return False
    raise ConfigError(f"Invalid boolean value: {value!r}")


def _parse_int(value: str) -> int:
    try:
        return int(value.strip())
    except ValueError as exc:
        raise ConfigError(f"Invalid integer value: {value!r}") from exc


def _parse_coord(value: str) -> Coord:
    parts: list[str] = value.strip().split(",")
    if len(parts) != 2:
        raise ConfigError(
            f"Invalid coordinate format: {value!r} (expected x,y)")
    return _parse_int(parts[0]), _parse_int(parts[1])


def load_config(path: Path) -> Config:
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    if not path.is_file():
        raise ConfigError(f"Config path is not a file: {path}")

    raw: Dict[str, str] = {}
    try:
        with path.open("r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                if "=" not in s:
                    raise ConfigError(f"Bad syntax at line {line_no}: expected KEY=VALUE")
                k, v = s.split("=", 1)
                key = k.strip().upper()
                val = v.strip()
                if not key:
                    raise ConfigError(f"Empty key at line {line_no}")
                raw[key] = val
    except OSError as exc:
        raise ConfigError(f"Cannot read config file: {exc}") from exc

    missing = [k for k in ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"] if k not in raw]
    if missing:
        raise ConfigError(f"Missing mandatory keys: {', '.join(missing)}")

    width = _parse_int(raw["WIDTH"])
    height = _parse_int(raw["HEIGHT"])
    entry = _parse_coord(raw["ENTRY"])
    exit_ = _parse_coord(raw["EXIT"])
    output_file = Path(raw["OUTPUT_FILE"]).expanduser()
    perfect = _parse_bool(raw["PERFECT"])

    seed = None
    if "SEED" in raw and raw["SEED"].strip():
        seed = _parse_int(raw["SEED"])

    display = raw.get("DISPLAY", "NONE").strip().upper()
    if display not in {"NONE", "TERMINAL"}:
        raise ConfigError("DISPLAY must be NONE or TERMINAL")

    return Config(
        width=width,
        height=height,
        entry=entry,
        exit=exit_,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        display=display,
    )


def write_output_file(cfg: Config, gen: MazeGenerator) -> None:
    maze = gen.maze()
    hex_lines = maze.to_hex_lines()
    path_dirs = gen.shortest_path_directions()

    out = []
    out.extend(hex_lines)
    out.append("")
    out.append(f"{cfg.entry[0]},{cfg.entry[1]}")
    out.append(f"{cfg.exit[0]},{cfg.exit[1]}")
    out.append(path_dirs)

    try:
        cfg.output_file.parent.mkdir(parents=True, exist_ok=True)
        with cfg.output_file.open("w", encoding="utf-8", newline="\n") as f:
            for line in out:
                f.write(line + "\n")
    except OSError as exc:
        raise ConfigError(f"Cannot write output file: {exc}") from exc


@dataclass
class RenderState:
    show_path: bool = True
    color_idx: int = 0
    highlight_42: bool = True


def _maze_to_canvas(gen: MazeGenerator, show_path: bool) -> list[list[str]]:
    maze = gen.maze()
    w, h = maze.width, maze.height
    cw, ch = 2 * w + 1, 2 * h + 1
    canvas: list[list[str]] = [["#" for _ in range(cw)] for _ in range(ch)]

    for y in range(h):
        for x in range(w):
            cx, cy = 2 * x + 1, 2 * y + 1
            if (x, y) in maze.blocked:
                continue
            canvas[cy][cx] = " "
            for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                if maze.is_open_edge(x, y, d):
                    canvas[cy + d.dy][cx + d.dx] = " "

    ex, ey = maze.entry
    ox, oy = maze.exit
    canvas[2 * ey + 1][2 * ex + 1] = "E"
    canvas[2 * oy + 1][2 * ox + 1] = "X"

    if show_path:
        try:
            path = gen.shortest_path_directions()
            x, y = maze.entry
            cx, cy = 2 * x + 1, 2 * y + 1
            for ch_dir in path:
                d = Dir[ch_dir]
                canvas[cy + d.dy][cx + d.dx] = "."
                cx += 2 * d.dx
                cy += 2 * d.dy
                if canvas[cy][cx] == " ":
                    canvas[cy][cx] = "."
        except Exception:
            pass

    return canvas


def _init_colors() -> None:
    curses.start_color()
    curses.use_default_colors()
    for i, fg in enumerate([curses.COLOR_WHITE, curses.COLOR_CYAN, curses.COLOR_GREEN, curses.COLOR_YELLOW]):
        curses.init_pair(i + 1, fg, -1)
    curses.init_pair(20, curses.COLOR_MAGENTA, -1)


def _draw(stdscr: "curses._CursesWindow", gen: MazeGenerator, st: RenderState) -> None:
    stdscr.clear()
    _init_colors()

    canvas = _maze_to_canvas(gen, st.show_path)
    maxy, maxx = stdscr.getmaxyx()

    wall_pair = curses.color_pair((st.color_idx % 4) + 1)
    hi_pair = curses.color_pair(20)
    maze = gen.maze()

    for y, row in enumerate(canvas):
        if y >= maxy - 3:
            break
        for x, ch in enumerate(row):
            if x >= maxx - 1:
                break

            attr = 0
            if ch == "#":
                attr = wall_pair
            elif ch == ".":
                attr = curses.A_BOLD
            elif ch in {"E", "X"}:
                attr = curses.A_BOLD | curses.A_UNDERLINE

            if st.highlight_42 and ch == "#":
                if (x % 2 == 1) and (y % 2 == 1):
                    gx, gy = (x - 1) // 2, (y - 1) // 2
                    if (gx, gy) in maze.blocked:
                        attr = hi_pair | curses.A_BOLD

            stdscr.addch(y, x, ch, attr)

    help_line = "r=regen  p=path  c=colors  t=highlight42  q=quit"
    stdscr.addstr(min(maxy - 2, len(canvas) + 1), 0, help_line[: maxx - 1])
    stdscr.refresh()


def run_tui(gen: MazeGenerator) -> None:
    def _loop(stdscr: "curses._CursesWindow") -> None:
        curses.curs_set(0)
        stdscr.nodelay(False)
        st = RenderState()

        while True:
            _draw(stdscr, gen, st)
            key = stdscr.getch()

            if key in (ord("q"), ord("Q")):
                return
            if key in (ord("p"), ord("P")):
                st.show_path = not st.show_path
            elif key in (ord("c"), ord("C")):
                st.color_idx = (st.color_idx + 1) % 4
            elif key in (ord("t"), ord("T")):
                st.highlight_42 = not st.highlight_42
            elif key in (ord("r"), ord("R")):
                gen.generate()

    curses.wrapper(_loop)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 2

    cfg_path = Path(argv[1])
    try:
        cfg = load_config(cfg_path)
        gen = MazeGenerator(
            width=cfg.width,
            height=cfg.height,
            entry=cfg.entry,
            exit=cfg.exit,
            seed=cfg.seed,
            perfect=cfg.perfect,
        )
        gen.generate()
        write_output_file(cfg, gen)
        print(f"Wrote maze to: {cfg.output_file}")

        if cfg.display == "TERMINAL":
            run_tui(gen)

        return 0

    except (ConfigError, MazeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))