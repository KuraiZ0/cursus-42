"""This module contains basic transmutation functions."""
from alchemy.elements import create_fire, create_earth


def lead_to_gold() -> str:
    """Transmutes lead to gold."""
    fire_result: str = create_fire()
    return f"Lead transmuted to gold using {fire_result}"


def stone_to_gem() -> str:
    """Transmutes stone to gem."""
    earth_result: str = create_earth()
    return f"Stone transmuted to gem using {earth_result}"
