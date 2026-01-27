"""This module demonstrates different ways to import modules in Python."""
import alchemy.transmutation


def absolute() -> None:
    """Demonstrates absolute imports."""
    from alchemy.transmutation.basic import lead_to_gold, stone_to_gem
    print("Testing Absolute Imports (from basic.py)")
    print(f"lead_to_gold(): {lead_to_gold()}")
    print(f"stone_to_gem(): {stone_to_gem()}")


def relative() -> None:
    """Demonstrates relative imports."""
    from alchemy.transmutation.advanced import (
        philosophers_stone, elixir_of_life)
    print("Testing Relative Imports (from advanced.py)")
    print(f"philosophers_stone(): {philosophers_stone()}")
    print(f"elixir_of_life(): {elixir_of_life()}")


def package() -> None:
    """Demonstrates package access."""
    print("Testing Package Access:")
    print("alchemy.transmutation.lead_to_gold():"
          f" {alchemy.transmutation.lead_to_gold()}")
    print("alchemy.transmutation.philosophers_stone():"
          f" {alchemy.transmutation.philosophers_stone()}")


if __name__ == "__main__":
    print("=== Pathway Debate Mastery ===\n")
    absolute()
    print()
    relative()
    print()
    package()
    print()
    print("Both pathways work! Absolute: clear, Relative: concise")
