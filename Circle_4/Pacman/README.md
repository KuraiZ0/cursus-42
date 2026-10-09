*This project has been created as part of the 42 curriculum by waibelfo.*

# Pac-Man 42

## Description

Pac-Man 42 is a Python recreation of the classic arcade game.

The player moves through procedurally generated mazes, collects pacgums,
uses super-pacgums to eat ghosts, completes multiple levels and attempts
to obtain the highest possible score.

The project uses object-oriented programming, a modular architecture,
persistent highscores, external maze generation and a graphical interface.

## Features

- Graphical main menu
- At least 10 configurable levels
- External A-Maze-ing maze generation
- Four autonomous ghosts
- Pacgums and super-pacgums
- Score and life system
- Timer for every level
- Pause menu
- Persistent Top 10 highscores
- Configuration file with comments
- Cheat mode for peer evaluation
- PyInstaller packaging support

## Instructions

### Requirements

- Python 3.10 or later
- uv
- The assigned A-Maze-ing package (`mazegenerator`, wheel provided in
  `mazegenerator-00001.zip`)

### Installation

```bash
make install
```

`make install` runs `uv sync`, then installs the assigned `mazegenerator`
wheel as-is (it is unzipped from `mazegenerator-*.zip` if needed). To use
another version of the package (for example at peer review):

```bash
uv pip install --reinstall path/to/mazegenerator-X.Y.Z-py3-none-any.whl
```

### Execution

```bash
make run
```

The program can also be started directly:

```bash
uv run python3 pac-man.py config.json
```

The program requires exactly one configuration file argument.

### Tests

```bash
make test
```

### Code validation

```bash
make lint
```

Run tests and lint together:

```bash
make check
```

### Debug mode

```bash
make debug
```

### Build executable

```bash
make build
```

## Controls

| Key | Action |
|---|---|
| Arrow keys | Move Pac-Man |
| W, A, S, D | Move Pac-Man |
| P or Escape | Pause or resume |
| Enter | Confirm menu option |
| F1 | Toggle invincibility |
| F2 | Skip the current level |
| F3 | Freeze or release ghosts |
| F4 | Add one life |
| F5 | Toggle speed boost |

## Configuration

The game uses a JSON configuration file.

Lines beginning with `#` (or `//`) are treated as comments and ignored.
The file may have any name; it only has to contain JSON.

Example:

```json
# Pac-Man configuration
{
    "highscore_filename": "highscores.json",
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "super_pacgum_duration": 8.0,
    "ghost_respawn_time": 5.0,
    "level_max_time": 90,
    "seed": 42,
    "levels": [
        {"width": 16, "height": 11},
        {"width": 18, "height": 12}
    ]
}
```

### Configuration keys

| Key | Default | Description |
|---|---:|---|
| `highscore_filename` | `highscores.json` | Highscore storage file |
| `lives` | `3` | Initial number of lives |
| `points_per_pacgum` | `10` | Points for a pacgum |
| `points_per_super_pacgum` | `50` | Points for a super-pacgum |
| `points_per_ghost` | `200` | Points for an edible ghost |
| `super_pacgum_duration` | `8.0` | Frightened mode duration |
| `ghost_respawn_time` | `5.0` | Ghost respawn delay |
| `level_max_time` | `90` | Time limit in seconds |
| `seed` | `42` | Seed used for the first level (minimum 1) |
| `levels` | 10 levels of 20x14 | Maze size **in cells** (5 to 30); at least 10 levels are always played |

`width` and `height` count maze cells, as in A-Maze-ing: the grid drawn on
screen has `2 * n + 1` tiles per side (walls included).

Invalid values are replaced or clamped to safe values and a warning is
printed. A missing file or a file that cannot be read stops the program with
a clear message (never a traceback).

Unknown configuration keys are ignored.

## Highscore

Highscores are stored in a JSON file.

Each entry contains:

```json
{
    "name": "PLAYER",
    "score": 1000
}
```

Player names:

- Must contain between 1 and 10 characters
- May contain ASCII letters, numbers and spaces
- Cannot contain special characters

Scores:

- Must be integers
- Cannot be negative

The entries are sorted from highest to lowest score.
Only the best 10 entries are kept.

A missing, empty or corrupted file is treated as "no highscore" (the game
never crashes); invalid entries inside a valid file are skipped. The list is
loaded at start-up, saved as soon as a name is validated at the end of a game
(win or lose) and the best five scores are shown in the main menu.

The JSON implementation was selected because it is simple, readable,
portable and easy to validate.

## Maze Generation

The project does not implement its own maze generator: it uses the assigned
`mazegenerator` package (class `MazeGenerator`), installed as-is.

`MazeAdapter` (`src/game/maze_adapter.py`) adapts the project to the package:

1. It calls `MazeGenerator(size=(width, height), perfect=False, seed=seed)`.
   `PERFECT` is `False`, so the maze has loops and no dead ends.
2. The package returns `generator.maze`: for each cell, an integer whose four
   low bits are the walls (North = 1, East = 2, South = 4, West = 8).
3. The adapter expands this into a grid of `2 * height + 1` rows and
   `2 * width + 1` columns: every cell is a corridor tile, and the tile
   between two cells is a corridor only if the wall between them is open.
   The isolated "42" cells (value 15) stay walls.
4. Any failure (package missing, wrong interface, bad data) becomes a
   `MazeError`, displayed cleanly.

The first level uses the seed from the configuration file; the following
levels use random seeds. Seed `0` is never used because it means "random"
for the package.

## Implementation

The game is divided into several independent components:

- Configuration loading and validation
- Application state and graphical loop
- Maze representation
- Maze package adapter
- Player and ghost entities
- Collectibles
- Collision handling
- Level progression
- Highscore persistence
- Rendering and keyboard input

Ghost behaviour (`Game._choose_ghost_direction`): every move, a ghost follows
the shortest path (breadth-first search distances) to its target and never
turns back unless it is in a dead end. When edible, it flees from the player.

- Blinky targets the player
- Pinky targets four tiles ahead of the player
- Inky moves randomly 40 % of the time
- Clyde chases from afar but retreats to his corner when closer than 8 tiles

The player starts in the middle of the maze, super-pacgums and ghosts are in
the four corners, and every other corridor tile holds a pacgum.

The game uses a state-based application flow:

```text
MAIN MENU
    |
    v
GAME
    |
    +----> PAUSE
    |
    v
VICTORY / GAME OVER
    |
    v
NAME ENTRY
    |
    v
MAIN MENU
```

## General Software Architecture

```text
pac-man.py
    |
    v
App
    |
    +---- Renderer
    +---- InputHandler
    +---- HighscoreService
    |
    v
Game
    |
    +---- Level
    |       |
    |       +---- Maze
    |       +---- Collectibles
    |
    +---- Player
    +---- Ghosts
    |
    v
MazeAdapter
    |
    v
External A-Maze-ing package
```

### Main modules

#### `src/app.py`

Controls the application loop and visible screens.

#### `src/config.py`

Loads the JSON file, removes comments and validates values.

#### `src/game/game.py`

Controls gameplay, score, lives, levels, ghosts and cheats.

#### `src/game/maze.py`

Provides the internal wall and corridor representation.

#### `src/game/maze_adapter.py`

Connects the game to the external maze package.

#### `src/entities/`

Contains the player, ghosts and collectible classes.

#### `src/services/highscore.py`

Loads, validates, sorts and saves the Top 10 scores.

#### `src/ui/`

Contains rendering, screen states and input handling.

## Project Management

Project-management documents are stored in:

```text
project_management/
```

The directory contains:

- Initial planning
- Actual progress tracking
- Architecture decisions
- Risk analysis
- Acceptance tests

## Packaging

The executable is generated with PyInstaller:

```bash
make build
```

Generated files are placed in:

```text
dist/
```

The `dist/` folder also receives `config.json`, `highscores.json` and
`INSTRUCTIONS.txt` (controls, cheat keys and configuration).

The packaged game must be uploaded as a free private or unlisted build to
a public gaming platform such as Itch.io (for example with `butler push
dist/ <user>/<game>:linux`).

## Resources

### Technical resources

- Python documentation: https://docs.python.org/3/
- Pygame documentation: https://pyga.me/docs/
- mypy documentation: https://mypy.readthedocs.io/
- pytest documentation: https://docs.pytest.org/
- uv documentation: https://docs.astral.sh/uv/
- PyInstaller documentation: https://pyinstaller.org/

### AI usage

AI was used to assist with:

- Breaking the subject into smaller implementation steps
- Proposing the initial project architecture
- Explaining Python and object-oriented programming concepts
- Suggesting validation cases for the configuration parser
- Suggesting unit-test scenarios
- Reviewing documentation structure
- Identifying possible edge cases and error conditions

AI-generated suggestions must be reviewed, tested and understood before
being included in the final project.

The student remains responsible for the implementation, testing,
technical decisions and ability to explain the complete project.