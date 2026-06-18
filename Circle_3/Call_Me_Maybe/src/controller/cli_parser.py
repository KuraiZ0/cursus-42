from src.models.schemas import PromptTest
from src.models.schemas import FunctionDefinition
from typing import Any
import argparse
import json


def parsing() -> tuple[list[FunctionDefinition], list[PromptTest]]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json")
    parser.add_argument(
        "--input", default="data/input/function_calling_tests.json")
    parser.add_argument(
        "--output", default="data/output/function_calling_results.json")
    args = parser.parse_args()

    fn_list: list[Any] = []
    prompt_list: list[Any] = []
    with open(args.functions_definition, 'r') as f:
        calling = json.load(f)
        for line in calling:
            fn_list.append(FunctionDefinition(**line))

    with open(args.input, 'r') as f:
        tests = json.load(f)
        for line in tests:
            prompt_list.append(PromptTest(**line))
    return fn_list, prompt_list
