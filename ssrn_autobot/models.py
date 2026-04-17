"""Core data models for ssrn_autobot."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Paper:
    """Normalized paper record used across the pipeline."""

    source: str
    external_id: str | None
    title: str
    authors: list[str] = field(default_factory=list)
    abstract: str = ""
    url: str = ""
    posted_date: str | None = None
    collected_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    topic_labels: list[str] = field(default_factory=list)
    project_labels: list[str] = field(default_factory=list)
    score: float = 0.0
    summary: str = ""
    why_it_matters: str = ""
    action: str = ""

    def text_blob(self) -> str:
        """Return lower-cased searchable text for scoring and tagging."""
        return f"{self.title} {self.abstract}".lower().strip()


@dataclass
class CandidatePaper:
    """Raw source-level candidate that may need normalization."""

    source: str
    payload: dict[str, Any]
