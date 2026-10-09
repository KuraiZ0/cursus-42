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
- The assigned A-Maze-ing package

### Installation

```bash
make install
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

Lines beginning with `#` are treated as comments and ignored.

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
        {
            "width": 21,
            "height": 21
        }
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
| `seed` | `42` | Seed used for the first level |
| `levels` | 10 default levels | Maze dimensions |

Invalid values are replaced or clamped to safe values.

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
- May contain letters, numbers and spaces
- Cannot contain special characters

Scores:

- Must be integers
- Cannot be negative

The entries are sorted from highest to lowest score.
Only the best 10 entries are kept.

The JSON implementation was selected because it is simple, readable,
portable and easy to validate.

## Maze Generation

The project does not implement its own maze generator.

`MazeAdapter` loads the external A-Maze-ing package and attempts to adapt
its result to the internal `Maze` representation.

The generator is called with:

- Level width
- Level height
- A seed
- `PERFECT` or `perfect` set to `False`

The first level uses the fixed seed from the configuration file.

The following levels use randomly generated seeds.

The adapter accepts several possible function names and result formats so
that the project can be connected to the package assigned during the
project.

The assigned package must not be modified.

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

The packaged game must be uploaded as a free private or unlisted build to
a public gaming platform such as Itch.io.

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