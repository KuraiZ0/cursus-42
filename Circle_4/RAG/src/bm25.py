"""A BM25 index implemented with numpy, stored column by column.

BM25 score of a document ``d`` for a query ``q``::

    score(d, q) = sum over terms t of q of
        idf(t) * tf(t, d) * (k1 + 1)
               / (tf(t, d) + k1 * (1 - b + b * |d| / avgdl))

    idf(t) = ln(1 + (N - df(t) + 0.5) / (df(t) + 0.5))

Everything that does not depend on the query is precomputed at indexing
time: for each term we store the list of documents containing it and
the corresponding weight. A query then only sums a few numpy slices.
"""

import json
import math
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
import numpy.typing as npt


class BM25Index:
    """Okapi BM25 over a list of tokenized documents."""

    def __init__(self, k1: float = 1.2, b: float = 0.75) -> None:
        """Create an empty index.

        Args:
            k1: Term-frequency saturation (higher = repeated words count
                more).
            b: Length normalization (0 = none, 1 = full).
        """
        self.k1 = k1
        self.b = b
        self.vocab: Dict[str, int] = {}
        self.n_docs = 0
        # CSC-like layout: postings of term t live in
        # doc_ids[term_ptr[t]:term_ptr[t + 1]] (same slice for weights).
        self.term_ptr: npt.NDArray[np.int64] = np.zeros(1, dtype=np.int64)
        self.doc_ids: npt.NDArray[np.int32] = np.zeros(0, dtype=np.int32)
        self.weights: npt.NDArray[np.float32] = np.zeros(0, dtype=np.float32)

    def build(self, documents: Sequence[List[str]]) -> None:
        """Compute the BM25 weights of every (term, document) pair.

        Args:
            documents: One list of tokens per document.
        """
        self.n_docs = len(documents)
        lengths = np.array([len(d) for d in documents], dtype=np.float64)
        avgdl = float(lengths.mean()) if self.n_docs else 0.0
        postings: Dict[str, List[Tuple[int, int]]] = {}
        for doc_id, tokens in enumerate(documents):
            for term, tf in Counter(tokens).items():
                postings.setdefault(term, []).append((doc_id, tf))

        self.vocab = {term: i for i, term in enumerate(sorted(postings))}
        ptr = [0]
        all_docs: List[int] = []
        all_weights: List[float] = []
        for term in sorted(postings):
            plist = postings[term]
            df = len(plist)
            idf = math.log(1.0 + (self.n_docs - df + 0.5) / (df + 0.5))
            for doc_id, tf in plist:
                norm = self.k1 * (
                    1.0 - self.b + self.b * lengths[doc_id] / avgdl
                )
                all_docs.append(doc_id)
                all_weights.append(idf * tf * (self.k1 + 1.0) / (tf + norm))
            ptr.append(len(all_docs))
        self.term_ptr = np.array(ptr, dtype=np.int64)
        self.doc_ids = np.array(all_docs, dtype=np.int32)
        self.weights = np.array(all_weights, dtype=np.float32)

    def scores(self, query_tokens: Sequence[str]) -> npt.NDArray[np.float32]:
        """Score every document against a tokenized query.

        Args:
            query_tokens: Tokens of the query (unknown ones are ignored).

        Returns:
            An array of ``n_docs`` scores.
        """
        result = np.zeros(self.n_docs, dtype=np.float32)
        for term, qtf in Counter(query_tokens).items():
            idx = self.vocab.get(term)
            if idx is None:
                continue
            lo, hi = self.term_ptr[idx], self.term_ptr[idx + 1]
            result[self.doc_ids[lo:hi]] += qtf * self.weights[lo:hi]
        return result

    def top_k(
        self, query_tokens: Sequence[str], k: int
    ) -> List[Tuple[int, float]]:
        """Return the ``k`` best documents with a strictly positive score.

        Args:
            query_tokens: Tokens of the query.
            k: Number of results wanted.

        Returns:
            ``(doc_id, score)`` pairs, best first.
        """
        if k <= 0 or self.n_docs == 0:
            return []
        scores = self.scores(query_tokens)
        k = min(k, self.n_docs)
        best = np.argpartition(-scores, k - 1)[:k]
        best = best[np.argsort(-scores[best], kind="stable")]
        return [(int(i), float(scores[i])) for i in best if scores[i] > 0]

    def save(self, directory: Path, name: str) -> None:
        """Write the index to ``directory`` (``<name>.npz`` + vocab JSON).

        Args:
            directory: Destination folder (created if needed).
            name: Base name of the files.
        """
        directory.mkdir(parents=True, exist_ok=True)
        np.savez(
            directory / f"{name}.npz",
            term_ptr=self.term_ptr,
            doc_ids=self.doc_ids,
            weights=self.weights,
        )
        meta = {
            "k1": self.k1,
            "b": self.b,
            "n_docs": self.n_docs,
            "vocab": list(self.vocab),
        }
        with open(directory / f"{name}_vocab.json", "w") as handle:
            json.dump(meta, handle)

    @classmethod
    def load(cls, directory: Path, name: str) -> "BM25Index":
        """Read an index written by :meth:`save`.

        Args:
            directory: Folder containing the files.
            name: Base name of the files.

        Returns:
            The loaded index.
        """
        with open(directory / f"{name}_vocab.json") as handle:
            meta = json.load(handle)
        index = cls(k1=float(meta["k1"]), b=float(meta["b"]))
        index.n_docs = int(meta["n_docs"])
        index.vocab = {term: i for i, term in enumerate(meta["vocab"])}
        with np.load(directory / f"{name}.npz") as arrays:
            index.term_ptr = arrays["term_ptr"]
            index.doc_ids = arrays["doc_ids"]
            index.weights = arrays["weights"]
        return index
