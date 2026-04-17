"""Markdown digest writer."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from ssrn_autobot.models import Paper


def write_daily_digest(output_dir: Path, papers: list[Paper], as_of: date | None = None) -> Path:
    """Write a readable markdown digest file and return its path."""
    as_of = as_of or date.today()
    output_dir.mkdir(parents=True, exist_ok=True)
    digest_path = output_dir / f"digest-{as_of.isoformat()}.md"

    lines = [
        f"# SSRN Autobot Daily Digest ({as_of.isoformat()})",
        "",
        f"Generated papers: **{len(papers)}**",
        "",
        "## Top Papers",
        "",
    ]

    for idx, paper in enumerate(papers, start=1):
        topics = ", ".join(paper.topic_labels) if paper.topic_labels else "n/a"
        lines.extend(
            [
                f"### {idx}. {paper.title}",
                f"- **Score:** {paper.score}",
                f"- **Source:** {paper.source}",
                f"- **Posted date:** {paper.posted_date or 'n/a'}",
                f"- **Topic labels:** {topics}",
                f"- **Why it matters:** {paper.why_it_matters}",
                f"- **Action:** {paper.action}",
                f"- **URL:** {paper.url}",
                f"- **Summary:** {paper.summary}",
                "",
            ]
        )

    digest_path.write_text("\n".join(lines), encoding="utf-8")
    return digest_path
