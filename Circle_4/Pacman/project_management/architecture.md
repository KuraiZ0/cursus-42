# Software Architecture

## Overview

The project uses a modular object-oriented architecture.

```text
pac-man.py
    |
    v
App
    |
    +---- InputHandler
    +---- Renderer
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