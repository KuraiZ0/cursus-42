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
    capacity_info = "--capacity-info" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--capacity-info"]
    file_path: str = args[0]
    try:
        SimulationWindow(file_path, capacity_info)
        arcade.run()
    except Exception as e:
        print(f"Error loading: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
