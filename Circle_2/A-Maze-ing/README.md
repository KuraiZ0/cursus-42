*This project has been created as part of the 42 curriculum by your_login.*

# A-Maze-ing 🌀

## Description

A-Maze-ing is a procedural maze generator and solver built entirely in Python, with no external dependencies. The program reads a configuration file, generates a perfect maze using a depth-first search (recursive backtracker) algorithm, solves it with BFS to find the shortest path, and displays the result in the terminal with ANSI colors and a live generation animation.

The maze always embeds a hidden **"42"** pattern formed by fully closed cells, visible in the terminal rendering. The generated maze and its solution are saved to an output file in a hexadecimal bitmask format.

**Key features:**
- Procedural maze generation with DFS (perfect mazes — exactly one path between any two cells)
- BFS solver returning the optimal shortest path
- Live terminal animation during generation
- Interactive menu: regenerate, show/hide path, rotate colors, quit
- Saves maze and solution to a file
- Hidden "42" pattern embedded in every maze
- Reusable `mazegen` module installable via pip

---

## Project Structure

```
.
├── a_maze_ing.py         # Entry point, CLI parsing, interactive menu
├── config.txt            # Default configuration file
├── Makefile              # Build, run, lint, debug targets
├── pyproject.toml        # Package metadata for pip
├── README.md             # This file
└── mazegen/
    ├── __init__.py
    ├── generator.py      # MazeGenerator — DFS generation, display, animation
    └── solver.py         # MazeSolver — BFS pathfinding
```

---

## Instructions

### Requirements

- Python 3.10 or later
- A terminal with ANSI escape code support

No external Python dependencies are required to run the program.

### Installation

```bash
# Clone the repository
git clone <your_repo_url>
cd a-maze-ing

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install linting tools
make install
```

### Run

```bash
make        # Run with default config.txt
# or
python3 a_maze_ing.py config.txt
```

### Other Makefile targets

```bash
make debug        # Run with pdb debugger
make lint         # Run flake8 + mypy (standard)
make lint-strict  # Run flake8 + mypy --strict
make clean        # Remove __pycache__, .mypy_cache, etc.
make build        # Build the pip-installable package
make install-pkg  # Build and install the package locally
```

---

## Configuration File

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored.

### Mandatory keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Number of columns in the maze | `WIDTH=20` |
| `HEIGHT` | Number of rows in the maze | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether to generate a perfect maze | `PERFECT=True` |

### Optional keys

| Key | Description | Example |
|-----|-------------|---------|
| `SEED` | Random seed for reproducibility | `SEED=42` |

### Example `config.txt`

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

> **Note:** In this implementation, only perfect mazes are supported (a single unique path between every pair of cells). The `PERFECT` key is parsed and accepted but the generation always produces a perfect maze. This is a deliberate design choice: the recursive backtracker algorithm inherently produces perfect mazes, and adding random loops would reduce algorithmic clarity and maze quality for the use case.

---

## Maze Generation Algorithm

### Algorithm chosen: Recursive Backtracker (Depth-First Search)

The maze is generated using an **iterative depth-first search** with an explicit stack (to avoid Python's recursion limit on large grids).

**How it works:**

1. Start at the entry cell and mark it as visited.
2. Push it onto the stack.
3. While the stack is not empty:
   - Look at the current cell (top of stack).
   - If it has unvisited neighbors, choose one at random, break the wall between them, mark the neighbor as visited, and push it onto the stack.
   - If it has no unvisited neighbors, pop from the stack (backtrack).
4. Repeat until all reachable cells have been visited.

The "42" pattern cells are pre-marked as visited before generation starts, which causes the DFS to naturally carve around them, leaving them as isolated walled blocks that form the visible pattern.

### Why this algorithm?

- **Simplicity:** The logic is clean, easy to understand, and easy to audit — important for a school project where code comprehension matters.
- **Perfect mazes by design:** DFS always produces a spanning tree of the grid, which means exactly one path exists between any two cells. This satisfies the `PERFECT=True` requirement without any extra logic.
- **Visual quality:** DFS mazes have long, winding corridors, which produces an aesthetically pleasing and challenging result compared to algorithms like Prim's (which tend to create shorter, bushier passages).
- **Reproducibility:** By seeding Python's `random` module, the same maze is always generated from the same seed, satisfying the reproducibility requirement.
- **Animation-friendly:** The iterative stack approach makes it trivial to display the generation progress frame by frame.

---

## Output File Format

The output file contains:

1. One line per row of the maze. Each cell is encoded as a single uppercase hexadecimal digit representing a 4-bit bitmask of its closed walls.
2. A blank line separator.
3. The entry coordinates (`x,y`).
4. The exit coordinates (`x,y`).
5. The shortest path from entry to exit as a string of direction letters (`N`, `E`, `S`, `W`).

### Wall bitmask encoding

| Bit | Value | Wall direction |
|-----|-------|---------------|
| 0 (LSB) | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

A set bit (1) means the wall is **closed**. A clear bit (0) means the wall is **open**.

**Example:** `F` (binary `1111`) = all four walls closed. `6` (binary `0110`) = East and South walls closed, North and West open.

### Example output

```
9515...
EBAB...
...

0,0
19,14
SSEENNWWEE...
```

---

## Interactive Menu

Once the maze is generated and displayed, the following menu is available:

| Option | Action |
|--------|--------|
| `1` | Regenerate a new maze (with animation) |
| `2` | Toggle the solution path display |
| `3` | Cycle through terminal colors |
| `4` | Quit |

---

## Reusable Module

The maze generation logic is packaged as a standalone, reusable Python module called `mazegen`. It can be installed via pip from the built package at the root of the repository.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or
pip install mazegen-1.0.0.tar.gz
```

### Building the package from source

```bash
python3 -m pip install --upgrade build
python3 -m build
# Output: dist/mazegen-1.0.0-py3-none-any.whl and dist/mazegen-1.0.0.tar.gz
```

### Usage example

```python
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver

# Instantiate the generator
maze = MazeGenerator(
    width=20,
    height=15,
    start=(0, 0),
    end=(19, 14),
    seed=42          # Optional: omit for a random maze each time
)

# Generate the maze (set animate=True for terminal animation)
maze.generate(animate=False)

# Access the grid: a list of lists of integers (bitmask per cell)
grid = maze.grid  # grid[row][col] → int (0–15)

# Display the maze in the terminal
maze.display()

# Solve the maze
solver = MazeSolver(maze.grid, maze.start, maze.end)
path = solver.solve()  # Returns a string like "SSEENNEE..." or None

# Display the maze with the solution path highlighted
maze.display(path_str=path)

# Save to file
maze.save_to_file("maze.txt", path)
```

### Custom parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `start` | `tuple[int, int]` | Entry cell as (x, y) |
| `end` | `tuple[int, int]` | Exit cell as (x, y) |
| `seed` | `int \| None` | Random seed (optional, default `None`) |

### Accessing the maze structure

After calling `maze.generate()`, the following attributes are available:

- `maze.grid` — `list[list[int]]`: the full grid, one integer per cell (bitmask of walls)
- `maze.start` — `tuple[int, int]`: entry coordinates
- `maze.end` — `tuple[int, int]`: exit coordinates
- `maze.width`, `maze.height` — dimensions

The solver returns the path as a direction string (`"NNEESS..."`) or `None` if no path exists.

---

## Team & Project Management

### Team

| Login | Role |
|-------|------|
| `your_login` | Sole contributor — generator, solver, display, CLI, packaging |

### Planning

**Anticipated planning:**
- Day 1–2: Algorithm research and DFS implementation
- Day 3: Wall encoding and output file format
- Day 4: Terminal display and animation
- Day 5: BFS solver
- Day 6: Interactive menu, config parsing, error handling
- Day 7: Packaging, README, linting

**How it evolved:**
The core generation and display were faster to implement than expected. More time than anticipated was spent on the animation system (frame skipping, cursor positioning with ANSI codes) and ensuring the "42" pattern was correctly carved into the maze without breaking DFS connectivity. Packaging with pyproject.toml also required some iteration.

### What worked well

- The iterative DFS was straightforward to implement and debug.
- Pre-marking the "42" pattern cells as visited before generation is an elegant approach that requires zero special-casing in the main algorithm.
- ANSI terminal rendering gives a clean visual result without any external dependencies.

### What could be improved

- The `PERFECT=False` case (non-perfect maze with loops) is not implemented. Supporting it would require a post-processing step to randomly remove walls after generation.
- The "42" pattern detection could be more robust for very small grids.
- A seed could be added to the configuration file for easier reproducibility from the CLI.
- Unit tests with pytest would improve confidence in edge cases (small mazes, entry/exit at corners, etc.).

### Tools used

- **Python 3.10+** — main language
- **flake8** — style linting (PEP 8)
- **mypy** — static type checking
- **pdb** — debugging
- **build** — Python package builder
- **Claude (Anthropic)** — used as an AI assistant (see Resources section)

---

## Resources

### References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [BFS shortest path — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python type hints — PEP 484](https://peps.python.org/pep-0484/)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

### AI usage

**Claude (Anthropic)** was used during this project for the following tasks:

- **Debugging:** Identifying issues in the ANSI cursor positioning logic for the animation (the `\033[{n}A` escape sequence to move the cursor up by N lines).
- **Type annotations:** Reviewing function signatures to ensure mypy compliance, particularly around `Optional` types and generic containers.
- **Documentation:** Drafting and structuring docstrings (Google style) for all classes and methods.
- **README:** Assistance in structuring and writing this README to meet the subject's requirements.

All AI-generated content was reviewed, tested, and understood before being integrated. No logic or algorithm was blindly copy-pasted — the core DFS and BFS implementations were written and debugged manually.