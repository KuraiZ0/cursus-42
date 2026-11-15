"""Pydantic data models exchanged between the stages of the RAG pipeline."""

import uuid
from typing import List

from pydantic import BaseModel, Field


class MinimalSource(BaseModel):
    """A location in the corpus: a file and a character range inside it."""

    file_path: str
    first_character_index: int
    last_character_index: int


class UnansweredQuestion(BaseModel):
    """A question without its answer (input of the search stage)."""

    question_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    question: str


class AnsweredQuestion(UnansweredQuestion):
    """A question with its reference answer and ground-truth sources."""

    sources: List[MinimalSource]
    answer: str


class RagDataset(BaseModel):
    """A dataset of questions, answered or not."""

    rag_questions: List[AnsweredQuestion | UnansweredQuestion]


class MinimalSearchResults(BaseModel):
    """The ranked sources retrieved for one question."""

    question_id: str
    question: str
    retrieved_sources: List[MinimalSource]


class MinimalAnswer(MinimalSearchResults):
    """Search results for one question plus the generated answer."""

    answer: str


class StudentSearchResults(BaseModel):
    """Output of ``search_dataset``: search results for a whole dataset."""

    search_results: List[MinimalSearchResults]
    k: int


class StudentSearchResultsAndAnswer(BaseModel):
    """Output of ``answer_dataset``: search results with their answers."""

    search_results: List[MinimalAnswer]
    k: int


class Chunk(BaseModel):
    """One indexed piece of a corpus file (persisted in the index)."""

    file_path: str
    first_character_index: int
    last_character_index: int
    kind: str  # "python" or "text"
    title: str = ""  # markdown heading breadcrumb or python def/class names

    def to_source(self) -> MinimalSource:
        """Convert the chunk to the minimal source format of the grader.

        Returns:
            The ``MinimalSource`` covering the same character range.
        """
        return MinimalSource(
            file_path=self.file_path,
            first_character_index=self.first_character_index,
            last_character_index=self.last_character_index,
        )
