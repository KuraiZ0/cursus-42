"""Adapter for the external A-Maze-ing package."""

import importlib
from types import ModuleType
from typing import Any, Callable, cast

from src.exceptions import MazeError
from src.game.maze import Maze


class MazeAdapter:
    """Adapt an external maze generator to the internal Maze class."""

    def __init__(self, package_name: str = "amazeing") -> None:
        """Initialise the maze adapter."""

        self.package_name = package_name

    def generate(
        self,
        width: int,
        height: int,
        seed: int,
    ) -> Maze:
        """Generate and convert a maze using the external package."""

        module = self._load_package()
        generator = self._find_generator(module)

        try:
            raw_maze = self._call_generator(
                generator=generator,
                width=width,
                height=height,
                seed=seed,
            )
            grid = self._extract_grid(raw_maze)
            normalised_grid = self._normalise_grid(grid)

            return Maze.from_integer_grid(normalised_grid)

        except MazeError:
            raise

        except Exception as error:
            raise MazeError(
                f"The external maze generator failed: {error}"
            ) from error

    def _load_package(self) -> ModuleType:
        """Import the external maze package."""

        try:
            return importlib.import_module(self.package_name)

        except ImportError as error:
            raise MazeError(
                "Unable to import the assigned A-Maze-ing package "
                f"'{self.package_name}'."
            ) from error

    def _find_generator(
        self,
        module: ModuleType,
    ) -> Callable[..., Any]:
        """Find a supported maze generation function."""

        function_names = (
            "generate_maze",
            "generate",
            "create_maze",
        )

        for function_name in function_names:
            generator = getattr(
                module,
                function_name,
                None,
            )

            if callable(generator):
                return cast(
                    Callable[..., Any],
                    generator,
                )

        generator_class = getattr(
            module,
            "MazeGenerator",
            None,
        )

        if callable(generator_class):
            instance = generator_class()

            generate_method = getattr(
                instance,
                "generate",
                None,
            )

            if callable(generate_method):
                return cast(
                    Callable[..., Any],
                    generate_method,
                )

        raise MazeError(
            "No compatible generator function was found in the "
            "A-Maze-ing package."
        )

    def _call_generator(
        self,
        generator: Callable[..., Any],
        width: int,
        height: int,
        seed: int,
    ) -> Any:
        """Call the external generator using supported signatures."""

        attempts = (
            {
                "width": width,
                "height": height,
                "seed": seed,
                "perfect": False,
            },
            {
                "width": width,
                "height": height,
                "seed": seed,
                "PERFECT": False,
            },
            {
                "rows": height,
                "columns": width,
                "seed": seed,
                "perfect": False,
            },
        )

        last_error: TypeError | None = None

        for arguments in attempts:
            try:
                return generator(**arguments)

            except TypeError as error:
                last_error = error

        try:
            return generator(
                width,
                height,
                seed,
                False,
            )

        except TypeError as error:
            last_error = error

        raise MazeError(
            "The A-Maze-ing generator interface is not supported."
        ) from last_error

    def _extract_grid(self, raw_maze: Any) -> Any:
        """Extract a grid from the external generator result."""

        if isinstance(raw_maze, (list, tuple)):
            return raw_maze

        method_names = (
            "to_grid",
            "get_grid",
            "export_grid",
        )

        for method_name in method_names:
            method = getattr(
                raw_maze,
                method_name,
                None,
            )

            if callable(method):
                return method()

        attribute_names = (
            "grid",
            "maze",
            "matrix",
            "cells",
        )

        for attribute_name in attribute_names:
            value = getattr(
                raw_maze,
                attribute_name,
                None,
            )

            if value is not None:
                return value

        raise MazeError(
            "Unable to extract a grid from the generated maze."
        )

    def _normalise_grid(
        self,
        raw_grid: Any,
    ) -> list[list[int]]:
        """Convert external maze values to zero and one."""

        if not isinstance(raw_grid, (list, tuple)):
            raise MazeError(
                "The generated maze grid is invalid."
            )

        grid: list[list[int]] = []

        for raw_row in raw_grid:
            if not isinstance(raw_row, (list, tuple)):
                raise MazeError(
                    "A generated maze row is invalid."
                )

            row = [
                self._normalise_cell(cell)
                for cell in raw_row
            ]

            grid.append(row)

        return grid

    def _normalise_cell(self, value: Any) -> int:
        """Convert one external cell value."""

        if isinstance(value, bool):
            return 1 if value else 0

        if isinstance(value, int):
            return 0 if value == 0 else 1

        if isinstance(value, str):
            cleaned_value = value.strip().lower()

            wall_values = {
                "#",
                "wall",
                "w",
                "0",
                "blocked",
            }

            corridor_values = {
                "",
                ".",
                "1",
                "path",
                "corridor",
                "c",
                "floor",
            }

            if cleaned_value in wall_values:
                return 0

            if cleaned_value in corridor_values:
                return 1

        raise MazeError(
            f"Unsupported external maze cell value: {value!r}"
        )
