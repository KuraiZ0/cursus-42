"""Generation stage: answer a question from retrieved chunks with Qwen3."""

from typing import Any, List, Tuple

from .models import Chunk

DEFAULT_MODEL = "Qwen/Qwen3-0.6B"

SYSTEM_PROMPT = (
    "You are an assistant answering questions about the vLLM codebase. "
    "Answer ONLY with information found in the provided context. "
    "Be concise: 1 to 4 sentences. Quote exact names (functions, flags, "
    "endpoints, classes) when they appear in the context. If the context "
    "does not contain the answer, say that you could not find it."
)


class AnswerGenerator:
    """Wrap Qwen3-0.6B (Hugging Face transformers) to produce answers."""

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        max_context_tokens: int = 3000,
        max_new_tokens: int = 256,
    ) -> None:
        """Load the tokenizer and the model (downloaded on first use).

        Args:
            model_name: Hugging Face model id.
            max_context_tokens: Token budget given to the retrieved chunks.
            max_new_tokens: Maximum length of the generated answer.
        """
        # Heavy imports are done here so that `index`/`search` stay fast.
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.tokenizer: Any = AutoTokenizer.from_pretrained(model_name)
        model: Any = AutoModelForCausalLM.from_pretrained(
            model_name, dtype=torch.float32
        )
        model.eval()  # inference mode: no dropout
        self.model: Any = model
        self.max_context_tokens = max_context_tokens
        self.max_new_tokens = max_new_tokens

    def build_context(self, passages: List[Tuple[Chunk, str]]) -> str:
        """Concatenate passages, best first, within the token budget.

        Each passage is preceded by its file path so the model knows
        where it comes from. A passage that does not fit is truncated.

        Args:
            passages: ``(chunk, text)`` pairs ranked by relevance.

        Returns:
            The context block inserted in the prompt.
        """
        blocks: List[str] = []
        budget = self.max_context_tokens
        for i, (chunk, text) in enumerate(passages, start=1):
            header = f"[{i}] {chunk.file_path}\n"
            ids = self.tokenizer.encode(header + text)
            if len(ids) > budget:
                if budget < 64:
                    break
                ids = ids[:budget]
            blocks.append(self.tokenizer.decode(ids))
            budget -= len(ids)
            if budget <= 0:
                break
        return "\n\n".join(blocks)

    def answer(self, question: str, passages: List[Tuple[Chunk, str]]) -> str:
        """Generate a grounded answer to ``question``.

        Args:
            question: The user question.
            passages: Retrieved ``(chunk, text)`` pairs, best first.

        Returns:
            The answer text.
        """
        context = self.build_context(passages)
        if not context:
            return "I could not find relevant information in the codebase."
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}",
            },
        ]
        prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,  # Qwen3: skip the <think> block
        )
        inputs = self.tokenizer(prompt, return_tensors="pt")
        with self.torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                repetition_penalty=1.1,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        new_tokens = output[0][inputs["input_ids"].shape[1]:]
        text = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        if "</think>" in text:
            text = text.split("</think>", 1)[1]
        return str(text).strip()
