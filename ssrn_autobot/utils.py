"""General utility helpers."""

from __future__ import annotations

import re


_NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")


def normalize_title(title: str) -> str:
    """Normalize a title for deduplication matching."""
    cleaned = _NON_ALNUM_RE.sub(" ", title.lower()).strip()
    return " ".join(cleaned.split())
