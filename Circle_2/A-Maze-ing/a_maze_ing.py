"""
This script generates and solves mazes based on a configuration file.

It provides an interactive command-line interface to:
- Generate new mazes.
- Show or hide the solution path.
- Rotate display colors.
- Save the generated maze and its solution to a file.
"""
from typing import Any
import sys
from mazegen.generator import MazeGenerator
from mazegen.solver import MazeSolver


def clear() -> None:
    """Clear the terminal screen."""
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()


def parsing(file_path: str) -> dict[str, Any]:
    """
    Parse the configuration file for maze generation.

    Args:
        file_path (str): The path to the configuration file.

    Returns:
        dict[str, Any]: A dictionary containing the parsed configuration.

    Raises:
        SystemExit: If the configuration file is not found.
    """
    config: dict[str, Any] = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if (line.startswith("#") or not line):
                    continue
                parts: list[str] = line.split("=", 1)
                config[parts[0].strip()] = parts[1].strip()
    except FileNotFoundError:
        print("Config.txt isn't found in the directory.")
        exit(1)
    for k, v in config.items():
        match k:
            case "WIDTH" | "HEIGHT":
                config[k] = int(v)
            case "ENTRY" | "EXIT":
                config[k] = tuple(map(int, v.split(",")))
            case "PERFECT":
                config['PERFECT'] = True if v == "True" else False
    return config


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)
    config: dict[str, Any] = parsing(sys.argv[1])
    show_path = False
    colors: list[str] = ["37", "31", "32", "33", "34", "35", "36"]
    color_idx = 0

    maze = MazeGenerator(config['WIDTH'], config['HEIGHT'],
                         config['ENTRY'], config['EXIT'])
    maze.generate(animate=True)

    maze_solved = MazeSolver(maze.grid, maze.start, maze.end)
    path: str | None = maze_solved.solve()

    maze.save_to_file(config['OUTPUT_FILE'], path)

    while True:
        clear()
        print("\n" + "="*10 + " A-Maze-ing " + "="*10)
        maze.display((path or "") if show_path else "", colors[color_idx])

        print("\n1. Re-generate a new maze")
        print(f"2. {'Hide' if show_path else 'Show'} "
              f"path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")

        choice: str = input("\nChoice? (1-4): ")

        if choice == "1":
            maze = MazeGenerator(config['WIDTH'], config['HEIGHT'],
                                 config['ENTRY'], config['EXIT'])
            maze.generate(animate=True, delay=0.0005)
            solver = MazeSolver(maze.grid, maze.start, maze.end)
            path = solver.solve()
            maze.save_to_file(config['OUTPUT_FILE'], path)
        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            color_idx = (color_idx + 1) % len(colors)
        elif choice == "4":
            print("Goodbye young padawan!")
            break
        else:
            print("Invalid choice.")
