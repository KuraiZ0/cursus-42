"""Main entry point for the Fly-In simulation."""

import arcade
from display import SimulationWindow


if __name__ == "__main__":
    file_path = "maps/hard/03_ultimate_challenge.txt"
    window = SimulationWindow(file_path)
    arcade.run()
