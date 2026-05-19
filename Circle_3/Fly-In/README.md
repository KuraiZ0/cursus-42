*This project has been created as part of the 42 curriculum by ialmani*

# 🚁 Fly-In

[![42 Project](https://img.shields.io/badge/42-Fly--In-00babc?style=flat-square&logo=42)](https://github.com/KuraiZ0/cursus-42/tree/main/Circle_3/Fly-In)
[![Circle](https://img.shields.io/badge/Circle-3-orange?style=flat-square)]()
[![Language](https://img.shields.io/badge/Language-Python-yellow?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-Finished-green?style=flat-square)]()
[![Maps](https://img.shields.io/badge/Maps-10_included-purple?style=flat-square)](./maps)

## 📋 Table of Contents

- [Description](#-description)
- [Algorithm & Implementation Strategy](#-algorithm--implementation-strategy)
- [Visual Representation](#-visual-representation)
- [Instructions](#-instructions)
- [Map Format & Zone Types](#-map-format--zone-types)
- [Resources](#-resources)

## 🎯 Description

**Fly-In** is a drone pathfinding simulation project developed for the 42 curriculum. The core objective is to design an efficient system that routes a fleet of drones from a central starting base to a target location in the **absolute minimum number of simulation turns**. 

The simulation navigates a dynamic network of interconnected zones, respecting strict constraints such as zone capacity (`max_drones`), connection throughput, and specific movement delays (`restricted` zones take 2 turns, `normal` take 1).

## 🧠 Algorithm & Implementation Strategy

To solve the routing problem efficiently and minimize the total turn count, the project relies on a modular architecture:
1. **Parser:** Safely reads the map, validates coordinates, and builds a fully connected network graph of `Zone` objects.
2. **Pathfinding (BFS):** The algorithm explores the graph to find all possible valid paths from the start hub to the end goal. It evaluates path lengths and prioritizes routes containing `priority` zones.
3. **Scheduler Engine:** The core logic evaluates the network state turn-by-turn. It efficiently manages a queue of drones, checks upcoming zone and connection capacities, and coordinates simultaneous movements without creating deadlocks or exceeding throughput limits. 

## 👁️ Visual Representation

To enhance user experience and provide clear debugging feedback, a fully graphical UI was implemented using the `arcade` library. 
- **Dynamic Camera:** The visual engine calculates a dynamic bounding box and automatically scales/centers the map to fit any screen size perfectly, regardless of the map's width or height.
- **Visual Clarity:** Drones and zones are rendered using custom 2D sprites. Colored texts and clean connection lines make it easy to follow the paths.
- **Live HUD:** A real-time heads-up display tracks the current Turn count, the Score (drones arrived), and the current simulation Mode (Auto/Manual), making the algorithm's efficiency instantly readable.

## 🚀 Instructions

### Prerequisites
Ensure you have Python 3.10+ installed.

### Installation
Use the provided Makefile to install the required dependencies (`flake8`, `mypy`, and `arcade`):
```bash
make install
```

### Execution
Run the simulation by providing a map file. You can adjust the `MAIN` and `CONFIG` variables in the Makefile if needed, or simply run it directly:
```bash
python3 main.py maps/hard/02_capacity_hell.txt
```

### Other Commands
- `make lint` : Runs Flake8 and Mypy with project-required flags to ensure perfect type safety.
- `make clean` : Cleans up python caches.

## 🗂️ Map Format & Zone Types

Maps are structured plain text files. The simulation supports `normal` (1 turn), `restricted` (2 turns), `priority` (1 turn, preferred), and `blocked` (impassable) zones.

Example:
```text
nb_drones: 5
start_hub: start 0 0 [color=blue]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
connection: start-roof1
```

## 📚 Resources

During the development of this project, the following resources were consulted:
- [Python 3.10 Documentation (Typing)](https://docs.python.org/3/library/typing.html)
- [Arcade Library Documentation](https://api.arcade.academy/en/latest/) for 2D graphics rendering.
- [PEP 257](https://peps.python.org/pep-0257/) for Docstring conventions.

**AI Usage:**
AI assistance was utilized as a sparring partner and tutor during this project. Specifically, it was used to:
- Debug mathematical rendering offsets for the `arcade` graphical interface (camera scale and aspect ratio).
- Format this README to adhere strictly to the 42 curriculum guidelines.