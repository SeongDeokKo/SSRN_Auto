"""Placeholder SSRN source module.

This module intentionally avoids brittle scraping logic.
TODO:
- Add stable integration with SSRN API/feed if/when available.
- Add robots.txt and ToS-compliant fetch policy.
- Add retry/backoff and caching for network robustness.
"""

from __future__ import annotations

from ssrn_autobot.collector.base import SourceCollector
from ssrn_autobot.models import CandidatePaper


class SSRNPlaceholderSource(SourceCollector):
    """Placeholder source that returns no data."""

    @property
    def name(self) -> str:
        return "ssrn_placeholder"

    def collect(self) -> list[CandidatePaper]:
        return []
