from src.model.schemas import (
    FunctionDefinition, JSONLogitsProcessor, FunctionCallOutput)
from src.llm_sdk import Small_LLM_Model
import numpy as np
import json


llm_model = Small_LLM_Model()


def get_allowed_tokens(curr_txt: str, voc: dict) -> list[int]:
    if not curr_txt:
        return [voc["{"]]
    if curr_txt == "{":
        return [voc['"']]
    return list(voc.values())


def load_fn_def(filepath: str) -> dict[str, FunctionDefinition]:
    with open(filepath, "r") as file:
        data = json.load(file)
    valid = {}
    for f in data:
        params = {}
        for arg_name, arg_type in f["args_types"].items():
            params[arg_name] = {"type": arg_type}
        converted = {
            "name": f["fn_name"],
            "description": "",
            "parameters": params,
            "returns": {"type": f["return_type"]},
        }
        valid[converted["name"]] = FunctionDefinition(**converted)
    return valid


def generate_json(
    prompt: str,
    json_processor: JSONLogitsProcessor,
    fn_dict: dict,
    max_tokens: int = 50,
    temp: float = 0.2,
) -> str:
    fn_txt = ""
    for fn in fn_dict.values():
        fn_txt += (fn.name + " " + str(fn.parameters) + " "
                   + fn.description + "\n")
    full_prompt = fn_txt + "\n" + prompt
    input_ids = llm_model._encode(full_prompt).tolist()[0]
    len_prompt = len(input_ids)

    for _ in range(max_tokens):
        logits: list[float] = llm_model.get_logits_from_input_ids(input_ids)
        masked_logits = json_processor.call(input_ids, logits)
        logits_np = masked_logits / temp
        exps = np.exp(logits_np)
        probs = exps / np.sum(exps)

        best_token_id = int(np.random.choice(len(logits_np), p=probs))
        input_ids.append(best_token_id)
        final_txt = llm_model._decode([best_token_id])
        if "}" in final_txt:
            break

    final_txt = llm_model._decode(input_ids[len_prompt:])
    return final_txt


def build_output(prompt: str, json_txt: str) -> FunctionCallOutput:
    data = json.loads(json_txt)
    name = data['name']
    parameters = data['parameters']
    fn_output = FunctionCallOutput(
        prompt=prompt, name=name, parameters=parameters)
    return fn_output
