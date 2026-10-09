# Progress Tracking

## Completed

- [x] Project architecture
- [x] Python project configuration
- [x] Makefile
- [x] JSON configuration parser
- [x] Custom exceptions
- [x] Internal maze representation
- [x] Maze adapter structure
- [x] Player entity
- [x] Ghost entity
- [x] Collectible entity
- [x] Collision helpers
- [x] Level structure
- [x] Main game controller
- [x] Main menu
- [x] Pause menu
- [x] Highscore service
- [x] Name-entry screen
- [x] Cheat mode
- [x] Unit-test structure
- [x] Packaging structure

## Done during the final review (compared with the subject)

- [x] Connect the assigned `mazegenerator` package (`MazeAdapter` converts the
      wall-bit cells into a corridor/wall tile grid, `perfect=False`)
- [x] Seed handling: first level uses the configured seed (>= 1, because 0
      means "random" in the package); next levels use random seeds
- [x] Ghost behaviours: BFS shortest-path chase, flee when edible, one
      personality per ghost
- [x] Config: any file name accepted, `#` and `//` comments, sizes in cells
- [x] Highscore names restricted to ASCII letters, digits and spaces
- [x] `.gitignore`, `.flake8`, `make lint` now runs `flake8 .` and `mypy .`
- [x] Tests: adapter, ghost AI, config; `tes_level.py` renamed `test_level.py`
- [x] Acceptance test plan written
- [x] Run full lint / mypy (also `--strict`) validation
- [x] Run all unit tests

## Remaining

- [ ] Build the executable on the target platform (`make build`)
- [ ] Publish the build on itch.io (free, unlisted/private)
- [ ] Re-test with the maze package given at peer review
