"""Mock source with local sample records for MVP testing."""

from __future__ import annotations

from ssrn_autobot.collector.base import SourceCollector
from ssrn_autobot.models import CandidatePaper


class MockSource(SourceCollector):
    """In-memory stub source returning sample papers."""

    @property
    def name(self) -> str:
        return "mock"

    def collect(self) -> list[CandidatePaper]:
        samples = [
            {
                "external_id": "MOCK-001",
                "title": "Pricing Kernel Identification with Weak Factors",
                "authors": ["A. Researcher", "B. Coauthor"],
                "abstract": "We study stochastic discount factor identification under weak factor structures and no-arbitrage restrictions.",
                "url": "https://example.org/mock-001",
                "posted_date": "2026-04-15",
            },
            {
                "external_id": "MOCK-002",
                "title": "Dividend Strips and the Term Structure of Equity Risk Premia",
                "authors": ["C. Author"],
                "abstract": "This paper analyzes horizon-specific expected returns and equity duration using dividend strips.",
                "url": "https://example.org/mock-002",
                "posted_date": "2026-04-14",
            },
            {
                "external_id": "MOCK-003",
                "title": "Covariance Shrinkage via Random Matrix Methods for GMV Portfolios",
                "authors": ["D. Quant"],
                "abstract": "High-dimensional covariance estimation with POET-style shrinkage improves global minimum variance allocation.",
                "url": "https://example.org/mock-003",
                "posted_date": "2026-04-13",
            },
            {
                "external_id": "MOCK-004",
                "title": "Implied Cost of Capital, Profitability, and Investment in Valuation",
                "authors": ["E. Accounting"],
                "abstract": "We bridge accounting and finance through implied cost of capital metrics and cross-sectional returns.",
                "url": "https://example.org/mock-004",
                "posted_date": "2026-04-12",
            },
            {
                "external_id": "MOCK-005",
                "title": "Pure IVOL and Option-Implied Signals in Expected Returns",
                "authors": ["F. Derivatives"],
                "abstract": "Idiosyncratic volatility interacts with variance risk premium and derivatives-implied information.",
                "url": "https://example.org/mock-005",
                "posted_date": "2026-04-11",
            },
            {
                "external_id": "MOCK-006",
                "title": "Dynamic Asset Allocation for Life-Cycle Investors",
                "authors": ["G. Planner"],
                "abstract": "Robust portfolio choice and strategic asset allocation over the life cycle.",
                "url": "https://example.org/mock-006",
                "posted_date": "2026-04-10",
            },
            {
                "external_id": "MOCK-007",
                "title": "Target Date Fund Glide Path Design under Sequence Risk",
                "authors": ["H. Retirement"],
                "abstract": "We propose retirement portfolio design principles for target date funds.",
                "url": "https://example.org/mock-007",
                "posted_date": "2026-04-09",
            },
            {
                "external_id": "MOCK-008",
                "title": "A Clinical Trial Design for Oncology Treatment",
                "authors": ["I. NonFinance"],
                "abstract": "A placebo-controlled clinical trial with survival analysis in oncology.",
                "url": "https://example.org/mock-008",
                "posted_date": "2026-04-08",
            },
            {
                "external_id": "MOCK-009",
                "title": "Anomalies, Return Predictability, and Risk-Based Explanations",
                "authors": ["J. AssetPricing"],
                "abstract": "We reassess anomalies and mispricing using alternative risk factor models.",
                "url": "https://example.org/mock-009",
                "posted_date": "2026-04-07",
            },
        ]
        return [CandidatePaper(source=self.name, payload=x) for x in samples]
