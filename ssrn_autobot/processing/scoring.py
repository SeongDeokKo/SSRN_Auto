"""Rule-based paper scoring."""

from __future__ import annotations

from ssrn_autobot.models import Paper
from ssrn_autobot.taxonomy import IRRELEVANT_KEYWORDS, TOPIC_KEYWORDS


def score_paper(paper: Paper) -> float:
    """Score a paper with transparent weighted keyword matching."""
    text = paper.text_blob()
    score = 0.0

    for _, (keywords, weight) in TOPIC_KEYWORDS.items():
        matches = sum(1 for kw in keywords if kw in text)
        if matches:
            score += weight + (matches - 1) * (weight * 0.25)

    penalty_hits = sum(1 for kw in IRRELEVANT_KEYWORDS if kw in text)
    score -= penalty_hits * 15

    return round(score, 2)
