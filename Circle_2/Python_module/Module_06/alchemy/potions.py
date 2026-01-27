"""This module contains functions for creating alchemical potions."""
from .elements import create_fire, create_water, create_air, create_earth


def healing_potion() -> str:
    """Create a healing potion."""
    fire_result: str = create_fire()
    water_result: str = create_water()
    return f"Healing potion brewed with {fire_result} and {water_result}"


def strength_potion() -> str:
    """Create a strength potion."""
    earth_result: str = create_earth()
    fire_result: str = create_fire()
    return f"Strength potion brewed with {earth_result} and {fire_result}"


def invisibility_potion() -> str:
    """Create an invisibility potion."""
    air_result: str = create_air()
    water_result: str = create_water()
    return f"Invisibility potion brewed with {air_result} and {water_result}"


def wisdom_potion() -> str:
    """Create a wisdom potion."""
    fire: str = create_fire()
    water: str = create_water()
    air: str = create_air()
    earth: str = create_earth()
    return (f"Wisdom potion brewed with all elements: {fire}, {water}, "
            f"{air}, {earth}")
