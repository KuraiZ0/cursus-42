"""Lightweight wrapper around a Hugging Face causal language model."""

import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedTokenizerBase,
    PreTrainedModel,
    logging,
)
from huggingface_hub import hf_hub_download


logging.set_verbosity_error()


class Small_LLM_Model:
    """Wrap a lightweight Hugging Face causal-LM for experimentation.

    Parameters
    ----------
    model_name : str
        Identifier of the model on the Hub.
    device : str or None
        Computation device. Auto-selects mps > cuda > cpu when None.
    dtype : torch.dtype or None
        Numerical precision. Defaults to float16 on GPU/MPS, float32 on CPU.
    trust_remote_code : bool
        Whether to trust remote code from the model repository.
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
        *,
        device: str | None = None,
        dtype: torch.dtype | None = None,
        trust_remote_code: bool = True,
    ) -> None:
        """Initialize the model and tokenizer on the selected device."""
        self._model_name = model_name

        if device is None:
            if torch.backends.mps.is_available():
                device = "mps"
            elif torch.cuda.is_available():
                device = "cuda"
            else:
                device = "cpu"
        self._device = device

        if dtype is None:
            dtype = (
                torch.float16
                if self._device in ["cuda", "mps"]
                else torch.float32
            )
        self._dtype = dtype

        self._tokenizer: PreTrainedTokenizerBase = (
            AutoTokenizer.from_pretrained(  # type: ignore[assignment]
                model_name, trust_remote_code=trust_remote_code
            )
        )
        if self._tokenizer.pad_token_id is None:
            self._tokenizer.pad_token_id = self._tokenizer.eos_token_id

        self._model: PreTrainedModel = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=self._dtype,
            device_map="auto" if self._device == "cuda" else None,
            trust_remote_code=trust_remote_code,
        )
        self._model.to(self._device).eval()  # type: ignore[arg-type]

        for p in self._model.parameters():
            p.requires_grad = False

    def _encode(self, text: str) -> torch.Tensor:
        """Tokenise text and return a 2-D input_ids tensor on the device."""
        ids = self._tokenizer.encode(text, add_special_tokens=False)
        return torch.tensor([ids], device=self._device, dtype=torch.long)

    def _decode(self, ids: torch.Tensor | list[int]) -> str:
        """Decode token ids back to a string, stripping special tokens."""
        if isinstance(ids, torch.Tensor):
            ids = ids.tolist()
        return self._tokenizer.decode(  # type: ignore[return-value]
            ids, skip_special_tokens=True
        )

    def get_logits_from_input_ids(self, input_ids: list[int]) -> list[float]:
        """Return raw next-token logits for the given sequence of token ids.

        Parameters
        ----------
        input_ids : list[int]
            Sequence of token ids to condition on.

        Returns
        -------
        list[float]
            Raw (pre-softmax) logits for the next token.
        """
        input_tensor = torch.tensor(
            [input_ids], device=self._device, dtype=torch.long
        )
        with torch.no_grad():
            out = self._model(input_ids=input_tensor)
        logits = out.logits[0, -1].tolist()
        return [float(x) for x in logits]

    def get_path_to_vocabulary_json(self) -> str:
        """Download and return the local path to the vocabulary JSON file."""
        vocab_file_name = self._tokenizer.vocab_files_names.get(
            'vocab_file', "vocab.json"
        )
        vocab_path = hf_hub_download(
            repo_id=self._model_name,
            filename=vocab_file_name,
        )
        return vocab_path
