"""Temporary A-Maze-ing replacement for local testing."""

import random


def generate_maze(
    width: int,
    height: int,
    seed: int,
    perfect: bool = False,
) -> list[list[int]]:
    """Generate a temporary open maze for development."""

    del perfect

    random.seed(seed)

    grid = [
        [0 for _ in range(width)]
        for _ in range(height)
    ]

    for row in range(1, height - 1):
        for column in range(1, width - 1):
            grid[row][column] = 1

    for row in range(2, height - 2, 4):
        for column in range(2, width - 2):
            if random.random() < 0.75:
                grid[row][column] = 0

        opening = random.randint(1, width - 2)
        grid[row][opening] = 1

    return grid
