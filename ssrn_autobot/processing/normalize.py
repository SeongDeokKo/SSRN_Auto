"""Normalization utilities converting raw candidates to Paper objects."""

from __future__ import annotations

from ssrn_autobot.models import CandidatePaper, Paper


def normalize_candidate(candidate: CandidatePaper) -> Paper:
    """Normalize a source candidate payload into the common Paper schema."""
    payload = candidate.payload
    authors = payload.get("authors", [])
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]

    return Paper(
        source=candidate.source,
        external_id=payload.get("external_id"),
        title=str(payload.get("title", "")).strip(),
        authors=list(authors),
        abstract=str(payload.get("abstract", "")).strip(),
        url=str(payload.get("url", "")).strip(),
        posted_date=payload.get("posted_date"),
    )
