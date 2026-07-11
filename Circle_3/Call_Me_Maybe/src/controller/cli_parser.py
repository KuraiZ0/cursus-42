"""CLI argument parsing utilities for the function-calling pipeline."""

from src.model.schemas import PromptTest
from typing import Any
import json


def parsing(input_path: str) -> list[PromptTest]:
    """Parse a JSON file of test prompts and return PromptTest objects.

    Parameters
    ----------
    input_path : str
        Path to the JSON file containing prompt test cases.

    Returns
    -------
    list[PromptTest]
        Parsed prompt test objects.

    Raises
    ------
    FileNotFoundError
        If input_path does not exist.
    """
    prompt_list: list[Any] = []

    try:
        with open(input_path, 'r') as f:
            tests = json.load(f)
    except FileNotFoundError as fne:
        raise FileNotFoundError(f"Input file missing: {input_path}") from fne
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON file malformed: {input_path}") from e
    for line in tests:
        prompt_list.append(PromptTest(**line))
    return prompt_list
