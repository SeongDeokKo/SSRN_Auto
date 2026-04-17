"""Base interfaces for data sources."""

from __future__ import annotations

from abc import ABC, abstractmethod

from ssrn_autobot.models import CandidatePaper


class SourceCollector(ABC):
    """Abstract interface for pluggable paper sources."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique source name."""

    @abstractmethod
    def collect(self) -> list[CandidatePaper]:
        """Return raw candidate papers from this source."""
