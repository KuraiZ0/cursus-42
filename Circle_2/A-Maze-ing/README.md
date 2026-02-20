# A-Maze-ing 🌀

A procedural maze generator and solver built in Python. Mazes are generated using a **depth-first search** (recursive backtracker) algorithm, solved with **BFS** for the shortest path, and displayed directly in the terminal with ANSI colors and a live generation animation.

---

## Features

- Procedural maze generation with DFS (perfect mazes, no loops)
- BFS solver returning the optimal path
- Live terminal animation during generation
- Interactive menu: show/hide path, rotate colors, regenerate
- Saves the maze and solution to a file
- Hidden **42** pattern embedded in every maze

---

## Project Structure

```
.
├── a_maze_ing.py       # Entry point, CLI parsing, interactive menu
├── config.txt          # Configuration file
├── Makefile            # Build, run, lint, debug targets
└── mazegen/
    ├── generator.py    # MazeGenerator — DFS generation + display + animation
    └── solver.py       # MazeSolver — BFS pathfinding
```

---

## Configuration

Edit `config.txt` to customize the maze:

```
WIDTH=20          # Number of columns
HEIGHT=15         # Number of rows
ENTRY=0,0         # Start position (x,y)
EXIT=19,14        # End position (x,y)
OUTPUT_FILE=maze.txt  # Output file for the saved maze
PERFECT=True      # Perfect maze (no loops)
```

---

## Usage

```bash
python3 a_maze_ing.py config.txt
```

Or with the Makefile:

```bash
make        # Run the program
make debug  # Run with pdb debugger
make lint   # Run flake8 + mypy
make clean  # Remove cache files
```

---

## Interactive Menu

Once the maze is generated, a menu lets you:

| Option | Action |
|--------|--------|
| `1` | Regenerate a new maze (with animation) |
| `2` | Toggle the solution path display |
| `3` | Cycle through terminal colors |
| `4` | Quit |

---

## Output File Format

The saved `maze.txt` contains:
1. Each row of the grid encoded as hexadecimal values (bitmask per cell)
2. A blank line separator
3. Start coordinates
4. End coordinates
5. The solution path as a string of directions (`N`, `E`, `S`, `W`)

---

## Wall Encoding

Each cell is stored as a 4-bit bitmask:

| Bit | Value | Wall |
|-----|-------|------|
| 0   | 1     | North |
| 1   | 2     | East  |
| 2   | 4     | South |
| 3   | 8     | West  |

A cell value of `15` (0b1111) means all four walls are intact.

---

## Requirements

- Python 3.10+
- A terminal with ANSI escape code support

No external dependencies.

---

## Linting

```bash
make lint         # flake8 + mypy (standard)
make lint-strict  # mypy --strict
```
