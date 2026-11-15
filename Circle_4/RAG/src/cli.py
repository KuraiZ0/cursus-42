"""Command-line interface (Python Fire): ``uv run python -m src <command>``.

Every command validates its arguments and turns expected failures
(missing file, malformed JSON, k <= 0, empty query...) into a short error
message instead of a traceback.
"""

import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import ValidationError
from tqdm import tqdm

from .evaluate import evaluate_results
from .generator import DEFAULT_MODEL, AnswerGenerator
from .indexer import build_index, read_text
from .models import (
    AnsweredQuestion,
    Chunk,
    MinimalAnswer,
    MinimalSearchResults,
    MinimalSource,
    RagDataset,
    StudentSearchResults,
    StudentSearchResultsAndAnswer,
)
from .retriever import Retriever

DEFAULT_RAW_DIR = "data/raw"
DEFAULT_INDEX_DIR = "data/processed"
MAX_CHUNK_SIZE = 2000


class CliError(Exception):
    """An expected user error, reported without traceback."""


def _check_k(k: Any) -> int:
    """Validate the ``k`` argument (a strictly positive integer)."""
    if isinstance(k, bool) or not isinstance(k, int) or k <= 0:
        raise CliError(f"--k must be a positive integer, got {k!r}")
    return k


def _check_query(query: Any) -> str:
    """Validate a query: Fire may hand us ints, tuples or empty strings."""
    if isinstance(query, (list, tuple)):
        query = " ".join(str(q) for q in query)
    text = str(query).strip() if query is not None else ""
    if not text:
        raise CliError("the query is empty")
    return text


def _load_json(path: str) -> Any:
    """Read a JSON file, converting errors to :class:`CliError`."""
    file = Path(path)
    if not file.is_file():
        raise CliError(f"file not found: {path}")
    try:
        with open(file, encoding="utf-8") as handle:
            return json.load(handle)
    except json.JSONDecodeError as err:
        raise CliError(f"malformed JSON in {path}: {err}")
    except (OSError, UnicodeDecodeError) as err:
        raise CliError(f"cannot read {path}: {err}")


def _save(model: Any, save_directory: str, name: str) -> Path:
    """Write a pydantic model as JSON in ``save_directory/name``."""
    out_dir = Path(save_directory)
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / name
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(model.model_dump_json(indent=2))
    except OSError as err:
        raise CliError(f"cannot write in {save_directory}: {err}")
    return out


def _source_text(source: MinimalSource, cache: Dict[str, str]) -> str:
    """Read the text covered by a source (used by ``answer_dataset``)."""
    if source.file_path not in cache:
        try:
            cache[source.file_path] = read_text(Path(source.file_path))
        except OSError:
            cache[source.file_path] = ""
    return cache[source.file_path][
        source.first_character_index:source.last_character_index
    ]


class RagCLI:
    """RAG against the machine: index, search and answer over vLLM."""

    def __init__(self, index_dir: str = DEFAULT_INDEX_DIR) -> None:
        """Configure the CLI.

        Args:
            index_dir: Where the index is stored / read.
        """
        self._index_dir = str(index_dir)
        self._retriever: Optional[Retriever] = None

    def _get_retriever(self) -> Retriever:
        """Load the index once, lazily."""
        if self._retriever is None:
            try:
                self._retriever = Retriever(self._index_dir)
            except (FileNotFoundError, ValueError, OSError) as err:
                raise CliError(str(err))
        return self._retriever

    def index(
        self,
        max_chunk_size: int = MAX_CHUNK_SIZE,
        raw_dir: str = DEFAULT_RAW_DIR,
    ) -> None:
        """Chunk ``raw_dir`` and save the index under ``index_dir``.

        Args:
            max_chunk_size: Maximum chunk length (1 to 2000 characters).
            raw_dir: Root of the corpus.
        """
        if (isinstance(max_chunk_size, bool)
                or not isinstance(max_chunk_size, int)
                or not 1 <= max_chunk_size <= MAX_CHUNK_SIZE):
            raise CliError(
                f"--max_chunk_size must be an integer in [1, "
                f"{MAX_CHUNK_SIZE}], got {max_chunk_size!r}"
            )
        try:
            build_index(str(raw_dir), self._index_dir, max_chunk_size)
        except (FileNotFoundError, OSError) as err:
            raise CliError(str(err))
        print(f"Ingestion complete! Indices saved under {self._index_dir}/")

    def search(self, query: Any, k: int = 10) -> None:
        """Print the top-``k`` sources for one query.

        Args:
            query: The question.
            k: Number of sources.
        """
        text = _check_query(query)
        k = _check_k(k)
        hits = self._get_retriever().search(text, k)
        if not hits:
            print("No relevant source found for this query.")
            return
        for rank, (chunk, score) in enumerate(hits, start=1):
            print(f"{rank:2d}. [{score:6.2f}] {chunk.file_path} "
                  f"[{chunk.first_character_index}:"
                  f"{chunk.last_character_index}]")

    def _search_all(
        self, dataset_path: str, k: int
    ) -> Tuple[StudentSearchResults, float]:
        """Run the search over every question of a dataset."""
        data = _load_json(dataset_path)
        try:
            dataset = RagDataset.model_validate(data)
        except ValidationError as err:
            raise CliError(f"invalid dataset {dataset_path}: {err}")
        retriever = self._get_retriever()
        start = time.perf_counter()
        results: List[MinimalSearchResults] = []
        for question in tqdm(dataset.rag_questions, desc="Searching",
                             unit="question"):
            hits = retriever.search(question.question, k)
            results.append(MinimalSearchResults(
                question_id=question.question_id,
                question=question.question,
                retrieved_sources=[c.to_source() for c, _ in hits],
            ))
        elapsed = time.perf_counter() - start
        return StudentSearchResults(search_results=results, k=k), elapsed

    def search_dataset(
        self,
        dataset_path: str,
        k: int = 10,
        save_directory: str = "data/output/search_results",
    ) -> None:
        """Search every question of a dataset and save the results.

        Args:
            dataset_path: JSON file following ``RagDataset``.
            k: Number of sources per question.
            save_directory: Output folder (file keeps the dataset name).
        """
        k = _check_k(k)
        results, elapsed = self._search_all(str(dataset_path), k)
        print(f"Searched {len(results.search_results)} questions "
              f"in {elapsed:.2f}s")
        out = _save(results, str(save_directory), Path(dataset_path).name)
        print(f"Saved student_search_results to {out}")

    def answer(
        self,
        query: Any,
        k: int = 10,
        model_name: str = DEFAULT_MODEL,
        context_chunks: int = 5,
    ) -> None:
        """Retrieve context for one query and generate an answer.

        Args:
            query: The question.
            k: Number of sources retrieved (and printed).
            model_name: Generation model.
            context_chunks: How many of the best sources go to the model.
        """
        text = _check_query(query)
        k = _check_k(k)
        retriever = self._get_retriever()
        hits = retriever.search(text, k)
        for rank, (chunk, _) in enumerate(hits, start=1):
            print(f"{rank:2d}. {chunk.file_path} "
                  f"[{chunk.first_character_index}:"
                  f"{chunk.last_character_index}]")
        generator = AnswerGenerator(str(model_name))
        passages = [(c, retriever.chunk_text(c))
                    for c, _ in hits[:max(1, int(context_chunks))]]
        print("\nAnswer:\n" + generator.answer(text, passages))

    def answer_dataset(
        self,
        student_search_results_path: str,
        save_directory: str = "data/output/search_results_and_answer",
        model_name: str = DEFAULT_MODEL,
        context_chunks: int = 5,
    ) -> None:
        """Generate an answer for every question of a search-results file.

        Args:
            student_search_results_path: Output of ``search_dataset``.
            save_directory: Output folder (file keeps the input name).
            model_name: Generation model.
            context_chunks: How many of the best sources go to the model.
        """
        path = str(student_search_results_path)
        data = _load_json(path)
        try:
            results = StudentSearchResults.model_validate(data)
        except ValidationError as err:
            raise CliError(f"invalid search results {path}: {err}")
        print(f"Loaded {len(results.search_results)} questions")
        generator = AnswerGenerator(str(model_name))
        cache: Dict[str, str] = {}
        answers: List[MinimalAnswer] = []
        for item in tqdm(results.search_results, desc="Answering",
                         unit="question"):
            passages = [
                (Chunk(**s.model_dump(), kind=""), _source_text(s, cache))
                for s in item.retrieved_sources[:max(1, int(context_chunks))]
            ]
            answers.append(MinimalAnswer(
                **item.model_dump(),
                answer=generator.answer(item.question, passages),
            ))
        print(f"Processed {len(answers)} of {len(results.search_results)} "
              f"questions")
        output = StudentSearchResultsAndAnswer(search_results=answers,
                                               k=results.k)
        out = _save(output, str(save_directory), Path(path).name)
        print(f"Saved student_search_results_and_answer to {out}")

    def evaluate(
        self,
        student_search_results_path: str,
        dataset_path: str,
        k: int = 10,
        max_context_length: int = MAX_CHUNK_SIZE,
    ) -> None:
        """Print our own recall@1/3/5/10 against a ground-truth dataset.

        Args:
            student_search_results_path: Output of ``search_dataset``.
            dataset_path: ``AnsweredQuestions`` dataset.
            k: Maximum number of sources considered per question.
            max_context_length: Maximum allowed source length.
        """
        k = _check_k(k)
        try:
            results = StudentSearchResults.model_validate(
                _load_json(str(student_search_results_path)))
            dataset = RagDataset.model_validate(_load_json(str(dataset_path)))
        except ValidationError as err:
            raise CliError(f"invalid input: {err}")
        too_long = [
            s for r in results.search_results for s in r.retrieved_sources
            if s.last_character_index - s.first_character_index
            > max_context_length
        ]
        if too_long:
            print(f"Warning: {len(too_long)} sources are longer than "
                  f"{max_context_length} characters")
        retrieved = {r.question_id: r.retrieved_sources[:k]
                     for r in results.search_results}
        expected = {q.question_id: q.sources for q in dataset.rag_questions
                    if isinstance(q, AnsweredQuestion)}
        if not expected:
            raise CliError(f"{dataset_path} has no answered question")
        ks = sorted({x for x in (1, 3, 5, 10, k) if x <= k})
        scores = evaluate_results(retrieved, expected, ks)
        print(f"Evaluated {len(expected)} questions")
        print("  ".join(f"Recall@{x}: {scores[x]:.3f}" for x in ks))
