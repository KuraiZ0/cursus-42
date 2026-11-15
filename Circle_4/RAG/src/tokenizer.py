"""Tokenization shared by indexing and querying.

The same function must be applied to chunks and to questions, otherwise
the words would never match. Code identifiers are kept whole *and* split
into their parts, so that a question can match either a verbatim
identifier (``load_lora_adapter``) or a paraphrase ("load a LoRA adapter").
"""

import re
from typing import List

WORD_RE = re.compile(r"[A-Za-z0-9_]+")
CAMEL_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

STOPWORDS = frozenset(
    """
    a an and are as at be been but by can could did do does doing done for
    from had has have how i if in into is it its itself me my of on or our
    should so than that the their them then there these they this those to
    was we were what when where which while who whom why will with would
    you your vllm s t use used using uses
    """.split()
)


def stem(word: str) -> str:
    """Reduce a lowercase word to a crude stem (plurals, -ing, -ed).

    It is not a real linguistic stemmer: it only has to map
    "adapters"/"adapter" or "loading"/"load" to the same string, and it
    is applied identically to the corpus and to the questions.

    Args:
        word: A lowercase token.

    Returns:
        The stemmed token.
    """
    if len(word) <= 3 or not word.isalpha():
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def split_identifier(identifier: str) -> List[str]:
    """Split a code identifier on underscores and camelCase boundaries.

    Args:
        identifier: For example ``"LoRAModelManager"`` or ``"max_num_seqs"``.

    Returns:
        The non-empty parts, e.g. ``["max", "num", "seqs"]`` or
        ``["Lo", "RA", "Model", "Manager"]``.
    """
    parts: List[str] = []
    for piece in identifier.split("_"):
        if piece:
            parts.extend(p for p in CAMEL_RE.split(piece) if p)
    return parts


def tokenize(text: str) -> List[str]:
    """Turn a text (question or chunk) into a list of index terms.

    Args:
        text: Any string.

    Returns:
        Lowercased, stemmed terms without stopwords. A compound
        identifier yields its full form plus each of its parts.
    """
    tokens: List[str] = []
    for match in WORD_RE.finditer(text):
        word = match.group(0).strip("_")
        if not word:
            continue
        parts = split_identifier(word)
        if len(parts) > 1:
            tokens.append(word.lower())
        for part in parts:
            low = part.lower()
            if len(low) < 2 or low in STOPWORDS:
                continue
            tokens.append(stem(low))
    return tokens
