# Acceptance Tests

Legend: OK = passed, FIXED = bug found then corrected.

| # | Feature | Procedure | Expected result | Status |
|---|---|---|---|---|
| 1 | Usage | `python3 pac-man.py` (no argument) | Usage message, no traceback | OK |
| 2 | Missing config | `python3 pac-man.py nope.json` | Clear error message | OK |
| 3 | Invalid JSON | file containing `{ not json` | Warning, defaults used | OK |
| 4 | Invalid values | `"lives": "x"`, `"level_max_time": -5` | Warning, defaults / clamp | OK |
| 5 | Unknown keys | add `"foo": 1` | Ignored | OK |
| 6 | Comments | lines starting with `#` or `//` | Ignored | OK |
| 7 | Maze generation | start a game | Maze from `mazegenerator`, fully connected | FIXED (placeholder generator replaced) |
| 8 | Fixed seed | two runs, level 1 | Identical maze | OK |
| 9 | Random levels | two runs, level 2 | Different mazes | FIXED (seeded RNG) |
| 10 | Level layout | level 1 | Player in the centre, 4 ghosts and 4 super-pacgums in corners | OK |
| 11 | Movement | arrows / WASD | Moves in corridors only | OK |
| 12 | Scoring | eat pacgum / super / ghost | +10 / +50 / +200 | OK |
| 13 | Ghosts | observe | Chase the player, flee when edible, respawn after 5 s | FIXED (greedy AI got stuck on walls) |
| 14 | Lives | touch a ghost | -1 life, respawn in the centre | OK |
| 15 | Level timer | wait 90 s | Life lost, timer reset | OK |
| 16 | Pause | P / ESC | Resume or back to main menu | OK |
| 17 | Cheat mode | F1..F5 | Invincible / skip / freeze / +life / speed | OK |
| 18 | Victory | skip 10 levels with F2 | Victory screen, name entry | OK |
| 19 | Game over | lose all lives | Game-over screen, name entry | OK |
| 20 | Highscores | enter name (max 10, alnum + space) | Saved, Top 10 sorted, shown in menu | OK |
| 21 | Corrupted highscore file | write garbage in the file | Ignored, no crash | OK |
| 22 | Lint | `make lint`, `make lint-strict` | No error | OK |
| 23 | Unit tests | `make test` | All pass | OK |
| 24 | Binary highscore file | write non UTF-8 bytes in the file | Ignored, game starts | FIXED (UnicodeDecodeError stopped the program) |
| 25 | Non-finite durations | `"super_pacgum_duration": NaN` / `Infinity` | Warning, default used | FIXED (accepted silently) |
| 26 | Unwritable highscore | highscore path is a directory | Error shown, ESC returns to the menu | FIXED (player stuck on name entry) |
| 27 | Invincibility | F1 then touch a ghost | No life lost, player not moved | FIXED (player was sent back to the centre) |
| 28 | Generator failure mid-game | generator raises on level 2+ | Game-over screen, no exit | FIXED (program closed) |
| 29 | Difficulty | play level 1 then level 5 | Ghosts noticeably faster | OK |
| 30 | Maze connectivity | 1160 mazes (sizes 5-30, 29 seeds) | Every pacgum reachable, 4 corners | OK |
