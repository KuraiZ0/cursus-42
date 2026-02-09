"""A module for mastering Python decorators."""
from functools import wraps
import time
from typing import Any


def spell_timer(func: callable) -> callable:
    """Decorator that measures and displays execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper that surrounds the original function."""
        print(f"Casting {func.__name__}...")
        start_time: float = time.perf_counter()
        fun = func(*args, **kwargs)
        end_time: float = time.perf_counter() - start_time
        print(f"Spell completed in {end_time:.4f} seconds")
        return fun
    return wrapper


def power_validator(min_power: int) -> callable:
    """Check that the first argument is greater than or equal to min_power."""
    def decorator(func: callable) -> callable:
        """Decorator who receives the function to validate."""
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """Check the power before running."""
            power: Any = kwargs.get('power')
            if power is None and len(args) >= 3:
                power = args[2]
            if power is None:
                return "No power level provided."
            if power >= min_power:
                return func(*args, **kwargs)
            else:
                return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> callable:
    def decorator(func: callable) -> callable:

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            n = 1
            while max_attempts >= n:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    print(f"Spell failed, retrying... "
                          f"(attempts {n}/{max_attempts})")
                    n += 1
            return (f"Spell casting failed "
                    f"after {max_attempts} attempts.")
        return wrapper
    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Static method that checks if name is valid"""
        space_or_letter = all(
            char.isalpha() or char.isspace() for char in name)
        if len(name) >= 3 and space_or_letter:
            return True
        else:
            return False

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"
