# Risk Analysis

## External maze package incompatibility

### Risk

The assigned A-Maze-ing package may use an unexpected interface.

### Impact

The game may be unable to generate a level.

### Mitigation

Use a dedicated `MazeAdapter` class to isolate the external package from
the rest of the project.

---

## Invalid configuration file

### Risk

The configuration file may be missing, malformed or contain invalid
values.

### Impact

The application may crash or start with unusable settings.

### Mitigation

Validate every configuration value, use safe defaults and display clear
messages without Python tracebacks.

---

## Corrupted highscore file

### Risk

The highscore JSON file may contain invalid data.

### Impact

The main menu may fail to load.

### Mitigation

Ignore invalid entries and use an empty highscore list when the file
cannot be decoded.

---

## Large maze dimensions

### Risk

A maze may be too large for the game window.

### Impact

The maze may not be completely visible.

### Mitigation

Calculate the tile size dynamically based on the window and maze
dimensions.

---

## Ghost movement problems

### Risk

Ghosts may become blocked or move outside the maze.

### Impact

The gameplay may become non-functional.

### Mitigation

Only select directions leading to walkable positions.

---

## Unhandled exception

### Risk

An unexpected exception may stop the application.

### Impact

The project may be considered non-functional during evaluation.

### Mitigation

Catch expected exceptions, validate external data and close Pygame in a
`finally` block.

---

## Packaging failure

### Risk

PyInstaller may not include all required modules.

### Impact

The generated executable may fail on another computer.

### Mitigation

Test the packaged application and declare required hidden imports in the
PyInstaller specification.