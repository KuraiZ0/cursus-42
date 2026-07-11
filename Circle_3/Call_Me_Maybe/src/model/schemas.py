"""Pydantic schemas and state-machine logic for JSON-constrained generation."""

from pydantic import BaseModel
from typing import Any
import numpy as np


class FunctionDefinition(BaseModel):
    """Schema for a single callable function's metadata."""

    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]


class FunctionCallOutput(BaseModel):
    """Schema for the output produced by one function-call inference."""

    prompt: str
    fn_name: str
    args: dict[str, Any]


class PromptTest(BaseModel):
    """Schema for a single test prompt."""

    prompt: str


class JSONStateMachine:
    """State machine tracking valid token positions in a JSON function call."""

    def __init__(self, fn_dict: dict[str, FunctionDefinition]) -> None:
        """Initialise the state machine for a set of function definitions.

        Parameters
        ----------
        fn_dict : dict[str, FunctionDefinition]
            Mapping from function name to its definition.
        """
        self.stack = [0]
        self.fn_dict = fn_dict
        self.fn_names = list(self.fn_dict.keys())
        self.curr_fn = ""
        self.curr_param = ""
        self.curr_param_type = ""
        self.curr_fn_buffer = ""
        self.curr_param_buffer = ""
        self.dig_count = 0
        self.used_params: set[str] = set()

    def get_allowed(self, voc: dict) -> list[Any]:
        """Return a list of token ids that are valid at the current state.

        Parameters
        ----------
        voc : dict
            Vocabulary mapping token strings to token ids.

        Returns
        -------
        list[Any]
            Token ids allowed by the current state.
        """
        liste = []
        match self.stack[-1]:
            case 0:
                liste.append(voc['{"'])
            case 1:
                liste.append(voc["name"])
            case 2:
                liste.append(voc['":'])
            case 3:
                liste.append(voc['Ġ"'])
            case 4:
                if self.curr_fn_buffer in self.fn_dict:
                    liste.append(voc['",'])
                for token_str, token_id in voc.items():
                    candidate = self.curr_fn_buffer + token_str
                    if any(
                         name.startswith(candidate) for name in self.fn_dict):
                        liste.append(token_id)
            case 5:
                liste.append(voc['Ġ"'])
            case 6:
                liste.append(voc["parameters"])
            case 7:
                liste.append(voc['":'])
            case 8:
                liste.append(voc['Ġ{"'])
            case 9:
                curr_param_dict = self.fn_dict[self.curr_fn].parameters
                remaining: set[str] = {
                    p for p in curr_param_dict
                    if p not in self.used_params}
                if self.curr_param_buffer in remaining:
                    liste.append(voc['":'])
                for token_str, token_id in voc.items():
                    candidate = self.curr_param_buffer + token_str
                    if any(p.startswith(candidate) for p in remaining):
                        liste.append(token_id)
            case 11:
                param_type = self.fn_dict[
                    self.curr_fn].parameters[self.curr_param]["type"]
                match param_type:
                    case "float" | "int":
                        liste.append(voc['Ġ'])
                    case "str":
                        liste.append(voc['Ġ"'])
                    case "bool":
                        liste.append(voc["Ġtrue"])
                        liste.append(voc["Ġfalse"])
            case 111:
                liste.extend(voc[t] for t in voc if t.isdigit())
                self.dig_count += 1
            case 12:
                if self.dig_count < 18:
                    liste.extend(voc[t] for t in voc if t.isdigit())
                liste.append(voc["}}"])
                remaining = (
                    set(self.fn_dict[self.curr_fn].parameters)
                    - self.used_params
                )
                if remaining:
                    liste.append(voc[','])
            case 91:
                liste.append(voc['"'])
                for tkn_str, tkn_id in voc.items():
                    if '"' not in tkn_str:
                        liste.append(tkn_id)
            case 13:
                liste.append(voc["}}"])
                remaining = (
                    set(self.fn_dict[self.curr_fn].parameters)
                    - self.used_params
                )
                if remaining:
                    liste.append(voc[','])
            case 131:
                liste.append(voc['Ġ"'])
        return liste

    def update(self, txt: str) -> None:
        """Advance the state machine by one decoded token.

        Parameters
        ----------
        txt : str
            The decoded string of the last generated token.
        """
        match self.stack[-1]:
            case 0:
                if txt == '{"':
                    self.stack = [1]
            case 1:
                if txt == "name":
                    self.stack = [2]
            case 2:
                if txt == '":':
                    self.stack = [3]
            case 3:
                if txt == 'Ġ"':
                    self.curr_fn_buffer = ""
                    self.stack = [4]
            case 4:
                if txt != '",':
                    self.curr_fn_buffer += txt
                else:
                    if self.curr_fn_buffer in self.fn_dict:
                        self.curr_fn = self.curr_fn_buffer
                        self.stack = [5]
            case 5:
                if txt == 'Ġ"':
                    self.stack = [6]
            case 6:
                if txt == "parameters":
                    self.stack = [7]
            case 7:
                if txt == '":':
                    self.stack = [8]
            case 8:
                if txt == 'Ġ{"':
                    self.curr_param_buffer = ""
                    self.stack = [9]
            case 9:
                if txt != '":':
                    self.curr_param_buffer += txt
                else:
                    if self.curr_param_buffer in self.fn_dict[
                            self.curr_fn].parameters:
                        self.curr_param = self.curr_param_buffer
                        self.used_params.add(self.curr_param)
                        self.curr_param_type = self.fn_dict[
                            self.curr_fn].parameters[self.curr_param]["type"]
                        self.dig_count = 0
                        self.stack = [11]
            case 11:
                if self.curr_param_type == "bool" and (
                        txt in ["Ġtrue", "Ġfalse"]):
                    self.stack = [13]
                elif self.curr_param_type == "str" and txt == 'Ġ"':
                    self.stack.append(91)
                elif (self.curr_param_type == "float"
                      or self.curr_param_type == "int") and txt == 'Ġ':
                    self.stack = [111]
            case 111:
                if txt.isdigit():
                    self.dig_count += 1
                    self.stack = [12]
            case 12:
                if txt.isdigit():
                    self.dig_count += 1
                else:
                    self.stack = [13]
                    self.update(txt)
            case 91:
                if txt == '"':
                    self.stack = [13]
            case 13:
                if txt == "}}":
                    self.stack = [14]
                elif txt == ',':
                    self.stack = [131]
            case 131:
                if txt == 'Ġ"':
                    self.curr_param_buffer = ""
                    self.stack = [9]


class JSONLogitsProcessor:
    """Mask invalid tokens at each step using the JSON state machine."""

    def __init__(self, state_machine: JSONStateMachine,
                 voc: dict, id_to_txt: dict) -> None:
        """Initialise the processor with a state machine and vocabularies.

        Parameters
        ----------
        state_machine : JSONStateMachine
            The finite state machine tracking JSON structure.
        voc : dict
            Vocabulary mapping token strings to token ids.
        id_to_txt : dict
            Reverse vocabulary mapping token ids to token strings.
        """
        self.state_machine = state_machine
        self.voc = voc
        self.id_to_txt = id_to_txt
        self.is_first_call = True

    def call(self, input_ids: list[int], logits: list[float]) -> np.ndarray:
        """Mask logits so only state-machine-allowed tokens have finite values.

        Parameters
        ----------
        input_ids : list[int]
            Full sequence of token ids generated so far.
        logits : list[float]
            Raw next-token logits from the language model.

        Returns
        -------
        np.ndarray
            Logits with -inf at positions not allowed by the state machine.
        """
        if self.is_first_call:
            self.is_first_call = False
        else:
            last_id = int(input_ids[-1])
            txt = self.id_to_txt[last_id]
            self.state_machine.update(txt)
        allowed_ids = self.state_machine.get_allowed(self.voc)
        mask = np.full(len(logits), float("-inf"))
        for allowed_id in allowed_ids:
            mask[allowed_id] = logits[allowed_id]
        return mask
