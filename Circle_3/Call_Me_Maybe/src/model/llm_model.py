"""High-level inference functions for JSON-constrained generation."""

from src.model.schemas import (
    FunctionDefinition, JSONLogitsProcessor, FunctionCallOutput)
from src.llm_sdk import Small_LLM_Model
import numpy as np
import json


llm_model = Small_LLM_Model()


def get_allowed_tokens(curr_txt: str, voc: dict) -> list[int]:
    """Return token ids that are valid given the current generated text prefix.

    Parameters
    ----------
    curr_txt : str
        Text generated so far.
    voc : dict
        Vocabulary mapping token strings to token ids.

    Returns
    -------
    list[int]
        List of valid next token ids.
    """
    if not curr_txt:
        return [voc["{"]]
    if curr_txt == "{":
        return [voc['"']]
    return list(voc.values())


def load_fn_def(filepath: str) -> dict[str, FunctionDefinition]:
    """Load and validate function definitions from a JSON file.

    Parameters
    ----------
    filepath : str
        Path to the JSON file containing function definitions.

    Returns
    -------
    dict[str, FunctionDefinition]
        Mapping from function name to its parsed definition.

    Raises
    ------
    FileNotFoundError
        If filepath does not exist.
    ValueError
        If the JSON file is malformed.
    """
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError as fne:
        raise FileNotFoundError(f"JSON not found: {filepath}") from fne
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON file malformed: {filepath}") from e
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
    verbose: bool = False,
) -> str:
    """Generate a JSON function call for prompt using constrained decoding.

    Parameters
    ----------
    prompt : str
        Natural-language question to answer with a function call.
    json_processor : JSONLogitsProcessor
        Logits processor that enforces valid JSON structure.
    fn_dict : dict
        Mapping from function name to FunctionDefinition.
    max_tokens : int
        Maximum number of tokens to generate.
    temp : float
        Sampling temperature (lower = more deterministic).
    verbose : bool
        If True, print the FSA state and chosen token at every step.

    Returns
    -------
    str
        Generated JSON string representing the function call.
    """
    fn_txt = ""
    for fn in fn_dict.values():
        param_txt = ""
        for arg_name, arg_type in fn.parameters.items():
            param_txt += arg_name + " (" + arg_type["type"] + "), "
        fn_txt += (fn.name + " " + param_txt + " "
                   + fn.description + "\n")
    full_prompt = (
        "Available functions:\n" + fn_txt +
        "\nUse the correct function for this question and output "
        "the matching JSON.\nQuestion: " + prompt + "\n")
    input_ids = llm_model._encode(full_prompt).tolist()[0]
    len_prompt = len(input_ids)

    for step in range(max_tokens):
        logits: list[float] = llm_model.get_logits_from_input_ids(input_ids)
        masked_logits = json_processor.call(input_ids, logits)
        logits_np = masked_logits / temp
        exps = np.exp(logits_np)
        probs = exps / np.sum(exps)

        best_token_id = int(np.random.choice(len(logits_np), p=probs))
        input_ids.append(best_token_id)
        final_txt = llm_model._decode([best_token_id])

        if verbose:
            n_allowed = int(np.sum(np.isfinite(masked_logits)))
            stack = json_processor.state_machine.stack
            print(f"step {step + 1:2d} | stack={stack!s:12} | "
                  f"allowed={n_allowed:<6} | chosen={final_txt!r}")

        if "}" in final_txt:
            break

    final_txt = llm_model._decode(input_ids[len_prompt:])
    return final_txt


def build_output(
        prompt: str, json_txt: str, fn_dict: dict) -> FunctionCallOutput:
    """Parse a generated JSON string and wrap it in a FunctionCallOutput.

    Parameters
    ----------
    prompt : str
        The original natural-language prompt.
    json_txt : str
        JSON string produced by generate_json.
    fn_dict : dict
        Mapping from function name to FunctionDefinition.

    Returns
    -------
    FunctionCallOutput
        Structured object containing the prompt, function name, and parameters.
    """
    try:
        data = json.loads(json_txt)
    except json.JSONDecodeError as js:
        raise json.JSONDecodeError(js)
    for k, v in data['parameters'].items():
        if isinstance(v, int):
            if fn_dict[data['name']].parameters[k]["type"] == "float":
                data['parameters'][k] = float(v)
    name = data['name']
    parameters = data['parameters']
    fn_output = FunctionCallOutput(
        prompt=prompt, fn_name=name, args=parameters)
    return fn_output
