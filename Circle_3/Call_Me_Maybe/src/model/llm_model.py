from llm_sdk import Small_LLM_Model
import numpy as np
import json


llm_model = Small_LLM_Model()
path = llm_model.get_path_to_vocabulary_json()
with open(path, 'r') as f:
    voc = json.load(f)
    for index, (token, token_id) in enumerate(voc.items()):
        # print(f"Token: '{token}' -> ID: {token_id}")
        if index == 4:
            break


def generate_json(prompt: str, max_tokens: int = 50, temp: float = 1.0) -> str:
    input_ids = llm_model._encode(prompt).tolist()[0]
    is_first = True
    len_prompt = len(input_ids)

    for _ in range(max_tokens):
        # temp = 0.2
        logits: list[float] = llm_model.get_logits_from_input_ids(input_ids)
        logits_np = np.array(logits)
        logits_np /= temp
        if is_first:
            logits_np = np.full(len(logits), float('-inf'))
            is_first = False
            logits_np[voc["{"]] = 0.0
        exps = np.exp(logits_np)
        probs = exps / np.sum(exps)

        best_token_id = int(np.random.choice(len(logits_np), p=probs))
        input_ids.append(best_token_id)
        final_txt = llm_model._decode([best_token_id])
        if "}" in final_txt:
            break

    final_txt = llm_model._decode(input_ids[len_prompt:])
    return final_txt


print(generate_json(
    "Génère un dictionnaire JSON avec les clés 'ville' et 'pays' : "))
