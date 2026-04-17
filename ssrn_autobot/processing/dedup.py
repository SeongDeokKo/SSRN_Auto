"""Deduplication logic for papers."""

from __future__ import annotations

from ssrn_autobot.models import Paper
from ssrn_autobot.utils import normalize_title


def deduplicate_papers(papers: list[Paper]) -> list[Paper]:
    """Deduplicate by external_id first, then by normalized title."""
    seen_ids: set[str] = set()
    seen_titles: set[str] = set()
    unique: list[Paper] = []

    for paper in papers:
        title_norm = normalize_title(paper.title)
        if paper.external_id:
            key = f"{paper.source}:{paper.external_id}"
            if key in seen_ids:
                continue
            seen_ids.add(key)

        if title_norm in seen_titles:
            continue
        seen_titles.add(title_norm)
        unique.append(paper)

    return unique
