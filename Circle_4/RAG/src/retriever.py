"""Retrieval stage: load the persisted index and rank chunks for a query."""

import json
from pathlib import Path
from typing import Dict, List, Tuple

from .bm25 import BM25Index
from .indexer import CHUNKS_FILE, INDEX_NAME, read_text
from .models import Chunk
from .tokenizer import tokenize


class Retriever:
    """Rank the indexed chunks of the corpus for a natural-language query."""

    def __init__(self, index_dir: str) -> None:
        """Load the index produced by the ``index`` command.

        Args:
            index_dir: Folder containing the index (``data/processed``).

        Raises:
            FileNotFoundError: If the index has not been built.
            ValueError: If the index files are corrupted.
        """
        directory = Path(index_dir)
        if not (directory / CHUNKS_FILE).is_file():
            raise FileNotFoundError(
                f"no index in {index_dir}: run the `index` command first"
            )
        try:
            with open(directory / CHUNKS_FILE) as handle:
                data = json.load(handle)
            self.chunks = [Chunk(**c) for c in data["chunks"]]
            self.bm25 = BM25Index.load(directory, INDEX_NAME)
        except (KeyError, TypeError, json.JSONDecodeError) as err:
            raise ValueError(f"corrupted index in {index_dir}: {err}")
        if self.bm25.n_docs != len(self.chunks):
            raise ValueError("index and chunk list do not match: re-index")
        self._files: Dict[str, str] = {}

    def search(self, query: str, k: int) -> List[Tuple[Chunk, float]]:
        """Return the top-``k`` chunks for ``query``.

        Args:
            query: The question.
            k: Number of chunks wanted.

        Returns:
            ``(chunk, score)`` pairs, best first. Empty if no query word
            is known by the index.
        """
        hits = self.bm25.top_k(tokenize(query), k)
        return [(self.chunks[i], score) for i, score in hits]

    def chunk_text(self, chunk: Chunk) -> str:
        """Read back the content of a chunk from the corpus.

        Args:
            chunk: A chunk returned by :meth:`search`.

        Returns:
            Its text, or an empty string if the file is unreadable.
        """
        if chunk.file_path not in self._files:
            try:
                self._files[chunk.file_path] = read_text(Path(chunk.file_path))
            except OSError:
                self._files[chunk.file_path] = ""
        content = self._files[chunk.file_path]
        return content[chunk.first_character_index:
                       chunk.last_character_index]
