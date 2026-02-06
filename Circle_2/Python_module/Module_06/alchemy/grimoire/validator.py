"""This module contains functions for validating alchemical ingredients."""


def validate_ingredients(ingredients: str) -> str:
    """
    Validate the ingredients for a spell.

    Args:
        ingredients: A string containing the ingredients.

    Returns:
        A string indicating whether the ingredients are valid or not.
    """
    valid_elements: list[str] = ["fire", "water", "earth", "air"]
    for ingredient in ingredients.split():
        if ingredient not in valid_elements:
            return f"{ingredients} - INVALID"
    return f"{ingredients} - VALID"
