"""Heuristic local summarizer."""

from __future__ import annotations

from ssrn_autobot.models import Paper


def summarize_paper(paper: Paper) -> Paper:
    """Create deterministic summary, why-it-matters, and action strings."""
    lead = paper.abstract.strip().split(".")[0].strip()
    summary = lead if lead else "Paper appears relevant to asset pricing research priorities."

    main_topics = ", ".join(paper.topic_labels[:2]) if paper.topic_labels else "broad asset pricing topics"
    paper.summary = summary + "."
    paper.why_it_matters = f"Connects to {main_topics} and may improve current research workflows."

    if paper.score >= 20:
        paper.action = "Read full paper now and log key methodology/results."
    elif paper.score >= 8:
        paper.action = "Add to reading queue and compare with current working notes."
    else:
        paper.action = "Keep as low-priority background unless project needs change."

    return paper
