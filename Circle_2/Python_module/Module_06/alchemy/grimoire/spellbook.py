"""This module contains functions for recording alchemical spells."""


def record_spell(spell_name: str, ingredients: str) -> str:
    """
    Record a spell in the spellbook.

    Args:
        spell_name: The name of the spell.
        ingredients: The ingredients for the spell.

    Returns:
        A string indicating whether the spell was recorded or not.
    """
    from .validator import validate_ingredients
    validation_result: str = validate_ingredients(ingredients)
    if "VALID" in validation_result:
        return f"Spell recorded: {spell_name} ({validation_result})"
    else:
        return f"Spell rejected: {spell_name} ({validation_result})"
