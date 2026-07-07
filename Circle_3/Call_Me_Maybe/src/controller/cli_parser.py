from src.model.schemas import PromptTest
from typing import Any
import json


def parsing(input_path: str) -> list[PromptTest]:
    prompt_list: list[Any] = []

    with open(input_path, 'r') as f:
        tests = json.load(f)
        for line in tests:
            prompt_list.append(PromptTest(**line))
    return prompt_list
