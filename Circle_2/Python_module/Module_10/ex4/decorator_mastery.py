"""A module for mastering Python decorators."""

from functools import wraps
import time
from typing import Any


def spell_timer(func: callable) -> callable:
    """Measure and display the execution time of a function.

    Args:
        func: The function to be timed.

    Returns:
        The wrapper function that executes the timed function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Execute the original function and time it.

        Args:
            *args: Positional arguments passed to the original function.
            **kwargs: Keyword arguments passed to the original function.

        Returns:
            The result of the original function.
        """
        print(f"Casting {func.__name__}...")
        start_time: float = time.perf_counter()
        fun = func(*args, **kwargs)
        end_time: float = time.perf_counter() - start_time
        print(f"Spell completed in {end_time:.4f} seconds")
        return fun

    return wrapper


def power_validator(min_power: int) -> callable:
    """Check if a spell's power meets a minimum requirement.

    Args:
        min_power: The minimum power level required to cast the spell.

    Returns:
        A decorator function that takes the spell function as an argument.
    """

    def decorator(func: callable) -> callable:
        """Wrap the function to be validated.

        Args:
            func: The function to which the power validation will be applied.

        Returns:
            The wrapper function that performs the power check.
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """Check the power level before executing the decorated function.

            Args:
                *args: Positional arguments for the decorated function.
                **kwargs: Keyword arguments for the decorated function.
                Expects 'power' as a kwarg.

            Returns:
                The result of the decorated function if power is sufficient,
                or an error message.
            """
            power: Any = kwargs.get("power")
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
    """Retry a spell (function) multiple times if it fails.

    Args:
        max_attempts: The maximum number of times to retry the spell.

    Returns:
        A decorator function that takes the spell function as an argument.
    """

    def decorator(func: callable) -> callable:
        """Wrap the function to be retried.

        Args:
            func: The function to which the retry logic will be applied.

        Returns:
            The wrapper function that implements the retry mechanism.
        """

        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            """Attempt to execute the decoratedfunction multiple times.

            Args:
                *args: Positional arguments for the decorated function.
                **kwargs: Keyword arguments for the decorated function.

            Returns:
                The result of the decorated function if successful,
                or an error message if all attempts fail.
            """
            n = 1
            while max_attempts >= n:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    print(
                        f"Spell failed, retrying... " f"(attempts {n}/{max_attempts})"
                    )
                    n += 1
            return f"Spell casting failed " f"after {max_attempts} attempts."

        return wrapper

    return decorator


class MageGuild:
    """Providing utility methods and spell casting."""

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """I used Static method for checks if name is valid."""
        space_or_letter = all(char.isalpha() or char.isspace() for char in name)
        if len(name) >= 3 and space_or_letter:
            return True
        else:
            return False

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        """Cast a spell if the power requirement is met.

        Args:
            spell_name: The name of the spell to cast.
            power: The power level used for casting the spell.

        Returns:
            A string indicating successful spell casting or insufficient power.
        """
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":

    print("\nTesting spell timer...\n")
