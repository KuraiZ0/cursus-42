"""Our own recall@k, for iterating (the official score is the moulinette).

A reference source counts as found when a retrieved source is in the same
file and their character ranges overlap with an IoU (intersection over
union) of at least 0.05, as described in the subject.
"""

from typing import Dict, List

from .models import MinimalSource

MIN_IOU = 0.05


def iou(a: MinimalSource, b: MinimalSource) -> float:
    """Intersection over union of two character ranges of the same file.

    Args:
        a: First source.
        b: Second source.

    Returns:
        A value in ``[0, 1]``, 0 when the files differ.
    """
    if a.file_path != b.file_path:
        return 0.0
    inter = min(a.last_character_index, b.last_character_index) - max(
        a.first_character_index, b.first_character_index
    )
    if inter <= 0:
        return 0.0
    union = max(a.last_character_index, b.last_character_index) - min(
        a.first_character_index, b.first_character_index
    )
    return inter / union if union > 0 else 0.0


def recall_at_k(
    retrieved: List[MinimalSource], expected: List[MinimalSource], k: int
) -> float:
    """Share of the expected sources found in the first ``k`` results.

    Args:
        retrieved: Ranked retrieved sources.
        expected: Ground-truth sources.
        k: Cut-off.

    Returns:
        A value in ``[0, 1]`` (1 when nothing is expected).
    """
    if not expected:
        return 1.0
    top = retrieved[:k]
    found = sum(
        1 for gold in expected if any(iou(gold, r) >= MIN_IOU for r in top)
    )
    return found / len(expected)


def evaluate_results(
    retrieved: Dict[str, List[MinimalSource]],
    expected: Dict[str, List[MinimalSource]],
    ks: List[int],
) -> Dict[int, float]:
    """Average recall@k over all ground-truth questions.

    Args:
        retrieved: question_id -> ranked retrieved sources.
        expected: question_id -> ground-truth sources.
        ks: Cut-offs to report.

    Returns:
        k -> mean recall@k. A question absent from ``retrieved`` scores 0.
    """
    if not expected:
        return {k: 0.0 for k in ks}
    return {
        k: sum(
            recall_at_k(retrieved.get(qid, []), gold, k)
            for qid, gold in expected.items()
        ) / len(expected)
        for k in ks
    }
