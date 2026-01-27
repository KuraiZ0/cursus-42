"""This module contains functions for validating alchemical ingredients."""


def validate_ingredients(ingredients: str) -> str:
    """
    Validate the ingredients for a spell.

    Args:
        ingredients: A string containing the ingredients.

    Returns:
        A string indicating whether the ingredients are valid or not.
    """
    valid_elements = ["fire", "water", "earth", "air"]
    for element in valid_elements:
        if element in ingredients:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
