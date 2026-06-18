from pydantic import BaseModel
from typing import Any


class FunctionDefinition(BaseModel):
    fn_name: str
    args_names: list[str]
    args_types: dict[str, str]
    return_type: str


class PromptTest(BaseModel):
    prompt: str


class FunctionCallOutput(BaseModel):
    prompt: str
    name: str
    parameters: dict[str, Any]
