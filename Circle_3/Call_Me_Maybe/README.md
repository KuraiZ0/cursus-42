*This project has been created as part of the 42 curriculum by ialmani.*

# Call Me Maybe

> Constrained JSON decoding for reliable function calling with a small LLM (Qwen3-0.6B).

## Description

**Call Me Maybe** translates natural-language prompts into structured function calls. Given a question like *"What is the sum of 2 and 3?"*, the program does not answer `5` — it outputs a machine-readable function call:

```json
{"name": "fn_add_numbers", "parameters": {"a": 2.0, "b": 3.0}}
```

Small language models are unreliable at producing valid JSON on their own (often <30% success rate). Instead of hoping the model gets the format right, this project uses **constrained decoding**: a custom logits processor masks out every token that would break the JSON structure or the function schema, so the model can *only* produce valid, schema-compliant output — 100% of the time.

## Instructions

Requirements: Python 3.10+, [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python -m src
```

Optional arguments (defaults shown):

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

Makefile shortcuts:

```bash
make install   # uv sync
make run       # run the pipeline
make debug     # run under pdb
make lint      # flake8 + mypy
make clean     # remove caches
```

## Algorithm Explanation

The core of the project is `JSONStateMachine`, a finite-state automaton driven by a **stack** (not a single integer) so it can enter and leave nested sub-states, such as freely typing a string value, without losing track of where it needs to return to.

At every generation step:

1. `get_allowed(voc)` looks at the current state (`self.stack[-1]`) and returns the list of token ids that are legal right now — e.g. only the opening token `{"`, only digit tokens while inside a number, or only the function names still available.
2. Those ids are used to build a mask: every other logit is set to `-inf`, so sampling can never select an invalid token.
3. After a token is generated, `update(txt)` advances the state machine based on the text of that token.

A key difficulty: the tokenizer does not map one word to one token. Names like `fn_add_numbers` or `source_string` are split into several tokens (`fn`, `_add`, `_numbers`...). The state machine handles this with a **buffer**: it accumulates token fragments and, at each step, only allows tokens that keep the buffer a valid prefix of at least one known function or parameter name. Once a delimiter token is generated, the buffer is checked against the real name and the machine advances.

Numbers use a similar trick: digits are allowed one at a time, with a counter capping how many digits a single number can have (to prevent runaway generation), while still supporting arbitrarily large numbers within that cap.

## Design Decisions

- **Stack-based FSA** instead of a flat integer state, to support nested constructs (string values, repeated parameters) cleanly.
- **Prompt engineering for function selection**: the model is not told to "guess" — it receives an explicit list of available functions with their parameter names and types, followed by a clear instruction to pick the right one. This was the single biggest accuracy improvement in the project.
- **Separation of concerns**: `generate_json` only produces raw constrained text; `build_output` is a separate function that parses that text into a `FunctionCallOutput`, keeping generation and post-processing independent and easier to test.
- **Type-safe output**: after parsing, integer values are converted to `float` only when the schema declares `"float"` for that parameter, keeping `int`/`bool` parameters faithful to the original schema.

## Performance Analysis

- **Structural validity**: 100% — every generated output is valid, parseable JSON, by construction (not by retrying).
- **Function selection accuracy**: 14/14 correct on the provided test set, after adding explicit function/parameter descriptions to the prompt.
- **Speed**: the model is loaded once and reused for every prompt; generation for all test prompts completes well under the 5-minute budget on standard hardware.

## Challenges Faced

- **Tokenizer mismatch**: initial assumptions about token boundaries (e.g. that `{`, `"`, `:` were separate tokens) were wrong. Fixed by encoding real example JSON strings and inspecting the actual token sequence produced by the tokenizer, then rebuilding the FSA around it.
- **Multi-token names**: function and parameter names longer than one token broke naive state transitions. Solved with the buffer + prefix-matching technique described above.
- **Runaway number generation**: without a limit, the model would keep emitting digits until `max_tokens` was reached. Fixed with a digit counter that closes the number after a safe upper bound.
- **Weak function selection**: the model defaulted to the same function regardless of the prompt when it had no information about available functions. Fixed by enriching the prompt with an explicit function list and instruction.

## Testing Strategy

The state machine was validated incrementally and manually, outside of the LLM loop first: calling `.update()` with a hand-written sequence of tokens matching a known-valid JSON string, and checking the stack reached the expected final state. Once the FSA behaved correctly in isolation, it was connected to the real model and tested against the full `function_calling_tests.json` set, checking both JSON validity (`json.loads`) and correctness of the selected function and parameters against the intent of each prompt.

## Example Usage

```bash
uv run python -m src
```

Given `data/input/function_calling_tests.json` containing:

```json
[{"prompt": "What is the sum of 2 and 3?"}]
```

`data/output/function_calling_results.json` will contain:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {"a": 2.0, "b": 3.0}
  }
]
```

## Resources

- [Qwen3-0.6B model card](https://huggingface.co/Qwen/Qwen3-0.6B)
- [Constrained decoding / structured generation — general concept](https://huggingface.co/docs/transformers/main/en/internal/generation_utils#logitsprocessor)
- [pydantic documentation](https://docs.pydantic.dev/)

**AI usage**: Claude was used throughout this project strictly as a debugging and learning aid — never to generate ready-made solutions. It was used to help track down bugs (e.g. mismatched tokenizer assumptions, stack-handling errors in the FSA, JSON formatting issues) and to explain new concepts (constrained decoding, logits masking, tokenizer behavior) so they could be understood and re-implemented independently. All design decisions and code in this repository were written and understood by the author.