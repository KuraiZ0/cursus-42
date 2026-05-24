"""Main entry point for the Fly-In simulation."""
import arcade
import sys
from view.display import SimulationWindow


def main():
    """Execute the sim."""
    if len(sys.argv) < 2:
        print("Error: No map file provided.")
        print("Usage: python3 main.py <chemin_vers_la_map>")
        sys.exit(1)
    file_path: str = sys.argv[1]
    try:
        SimulationWindow(file_path)
        arcade.run()
    except Exception as e:
        print(f"Error loading: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
