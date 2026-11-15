"""Unit tests of the pure components (no index or model needed)."""

from pathlib import Path
from typing import List, Tuple

from src.bm25 import BM25Index
from src.chunking import chunk_python, chunk_text
from src.evaluate import iou, recall_at_k
from src.models import MinimalSource
from src.tokenizer import tokenize

PY = '''"""Doc."""
import os


def first(a: int) -> int:
    """First."""
    return a + 1


class Thing:
    """A class."""

    def method(self) -> None:
        """M."""
        print("x" * 80)
''' * 20

MD = "# Title\n\nIntro text.\n\n## Part A\n\n" + "word " * 300 + \
    "\n\n## Part B\n\n```bash\n# not a heading\n```\n\n" + "other " * 300


def _check_cover(text: str, spans: List[Tuple[Tuple[int, int], str]],
                 max_size: int) -> None:
    previous = 0
    for (a, b), _ in spans:
        assert 0 <= a < b <= len(text)
        assert b - a <= max_size
        assert a >= previous
        assert text[previous:a].strip() == ""  # only whitespace dropped
        previous = b


def test_python_chunks_respect_limit() -> None:
    for size in (100, 500, 2000):
        spans = chunk_python(PY, size)
        _check_cover(PY, spans, size)


def test_python_chunks_cut_on_definitions() -> None:
    spans = chunk_python(PY, 300)
    starts = [PY[a:a + 6] for (a, _), _ in spans]
    assert any(s.startswith("def") or s.startswith("class") for s in starts)


def test_broken_python_still_chunked() -> None:
    text = "def broken(:\n    pass\n" * 200
    _check_cover(text, chunk_python(text, 200), 200)


def test_markdown_chunks_and_titles() -> None:
    spans = chunk_text(MD, 1000)
    _check_cover(MD, spans, 1000)
    titles = [t for _, t in spans]
    assert any("Part B" in t for t in titles)
    assert not any("not a heading" in t for t in titles)


def test_tokenize_identifiers() -> None:
    tokens = tokenize("Use max_num_seqs with LoRAModelManager!")
    assert "max_num_seqs" in tokens and "num" in tokens
    assert "manager" in tokens and "use" not in tokens
    assert tokenize("") == []


def test_bm25_ranks_relevant_first(tmp_path: Path) -> None:
    docs = [tokenize(t) for t in (
        "load a lora adapter at runtime",
        "tensor parallel size of the model",
        "speculative decoding with a draft model",
    )]
    index = BM25Index()
    index.build(docs)
    assert index.top_k(tokenize("How to load LoRA adapters?"), 2)[0][0] == 0
    index.save(tmp_path, "t")
    loaded = BM25Index.load(tmp_path, "t")
    assert loaded.top_k(tokenize("draft model"), 1)[0][0] == 2
    assert loaded.top_k(tokenize("zzzz"), 3) == []
    assert loaded.top_k(tokenize("model"), 0) == []


def test_recall_and_iou() -> None:
    gold = MinimalSource(file_path="f", first_character_index=100,
                         last_character_index=200)
    hit = MinimalSource(file_path="f", first_character_index=0,
                        last_character_index=1000)
    other = MinimalSource(file_path="g", first_character_index=100,
                          last_character_index=200)
    assert abs(iou(gold, hit) - 0.1) < 1e-9
    assert iou(gold, other) == 0.0
    assert recall_at_k([other, hit], [gold], 1) == 0.0
    assert recall_at_k([other, hit], [gold], 2) == 1.0
