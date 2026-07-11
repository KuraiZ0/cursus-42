"""Entry point for the function-calling inference pipeline."""

from src.model.schemas import JSONLogitsProcessor, JSONStateMachine
from src.model.llm_model import (
    generate_json, load_fn_def, build_output, llm_model)
from src.controller.cli_parser import parsing
from dotenv import load_dotenv
import argparse
import json
import os

load_dotenv()


path = llm_model.get_path_to_vocabulary_json()
with open(path, "r") as f:
    voc = json.load(f)
    for index, (token, token_id) in enumerate(voc.items()):
        if index == 4:
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json")
    parser.add_argument(
        "--input", default="data/input/function_calling_tests.json")
    parser.add_argument(
        "--output", default="data/output/function_calling_results.json")
    args = parser.parse_args()
    fn_dict = load_fn_def(args.functions_definition)
    prompt_list = parsing(args.input)
    id_to_txt = {v: k for k, v in voc.items()}
    state_machine = JSONStateMachine(fn_dict)
    json_processor = JSONLogitsProcessor(state_machine, voc, id_to_txt)
    result = []
    for prompt in prompt_list:
        json_txt = generate_json(
            prompt.prompt, json_processor, fn_dict, verbose=False)
        print(json_txt)
        state_machine = JSONStateMachine(fn_dict)
        json_processor = JSONLogitsProcessor(state_machine, voc, id_to_txt)
        output = build_output(prompt.prompt, json_txt, fn_dict)
        result.append(output)
    result_dict = [obj.model_dump() for obj in result]
    try:
        directory = os.path.dirname(args.output)
        os.makedirs(directory, exist_ok=True)
        with open(args.output, 'w') as f:
            json.dump(result_dict, f, indent=2)
    except FileNotFoundError:
        raise FileNotFoundError("Output files doesn't exist.")
