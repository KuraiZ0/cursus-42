# 🚁 Fly-In

[![42 Project](https://img.shields.io/badge/42-Fly--In-00babc?style=flat-square&logo=42)](https://github.com/KuraiZ0/cursus-42/tree/main/Circle_3/Fly-In)
[![Circle](https://img.shields.io/badge/Circle-3-orange?style=flat-square)]()
[![Language](https://img.shields.io/badge/Language-Python-yellow?style=flat-square)]()
[![Status](https://img.shields.io/badge/Status-In_Progress-blue?style=flat-square)]()
[![Maps](https://img.shields.io/badge/Maps-10_included-purple?style=flat-square)](./maps)

> Route multiple drones through a zoned airspace from start to end in the fewest turns possible.

## 📋 Table of Contents

- [Description](#-description)
- [How It Works](#-how-it-works)
- [Map Format](#-map-format)
- [Zone Types](#-zone-types)
- [Project Structure](#-project-structure)
- [Installation & Usage](#-installation--usage)
- [Maps](#-maps)

## 🎯 Description

**Fly-In** is a drone pathfinding simulation project at 42 Brussels. Given a map of interconnected zones and a number of drones, the program must route all drones from a start zone to an end zone in the **minimum number of simulation turns**, while respecting zone capacity constraints.

Key constraints:
- Multiple drones move simultaneously each turn
- Each zone has a max capacity (`max_drones`)
- Each connection has a max throughput (`max_link_capacity`)
- Some zones are `restricted` (slow), `blocked` (impassable), or `priority` (preferred)

## ⚙️ How It Works

```
Map file (zones + connections)
        ↓
  Parse & build graph
        ↓
  Find all paths (BFS/flow)
        ↓
  Schedule drones to minimize turns
        ↓
  Output: turn-by-turn drone movements
```

Each turn, every drone either moves to an adjacent zone or waits. The simulation ends when all drones reach the end zone.

## 🗂️ Map Format

Maps are plain text files with the following structure:

```
##start
start_zone
##end
end_zone
nb_drones N

zone1 max_drones
zone2 max_drones
...

zone1-zone2 max_link_capacity
zone1-zone3 max_link_capacity
...
```

## 🍿 Zone Types

| Type | Movement | Notes |
|------|----------|-------|
| `normal` | 1 turn | Standard zone |
| `restricted` | 2 turns | Slower, but passable |
| `priority` | 1 turn | Preferred by algorithm |
| `blocked` | — | Impassable |

## 📂 Project Structure

```
Fly-In/
├── en.subject.pdf     # Project subject
└── maps/              # Test maps by difficulty
    ├── easy/          # 3 maps — basic navigation
    ├── medium/        # 3 maps — dead ends, loops, priority
    ├── hard/          # 3 maps — extreme capacity, maze
    └── challenger/    # 1 map  — “The Impossible Dream” (25 drones)
```

## 🚀 Installation & Usage

```bash
git clone https://github.com/KuraiZ0/cursus-42.git
cd cursus-42/Circle_3/Fly-In

# Run the simulation
python3 fly_in.py maps/easy/01_linear_path.txt

# With visual output
python3 fly_in.py --visual maps/medium/01_dead_end_trap.txt
```

## 🗺️ Maps

See [`maps/README.md`](./maps/README.md) for the full list of maps and their challenge types.

| Difficulty | Maps | Drones | Description |
|------------|------|--------|-------------|
| 🟢 Easy | 3 | 2–4 | Basic navigation |
| 🟡 Medium | 3 | 4–6 | Dead ends, loops, priority zones |
| 🔴 Hard | 3 | 8–15 | Maze, capacity hell, ultimate challenge |
| ⚫ Challenger | 1 | 25 | Record to beat: **41 turns** |

**Status**: In Progress 🔧 | **Author**: [ialmani](https://profile.intra.42.fr/users/ialmani)
