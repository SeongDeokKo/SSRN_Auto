"""Topic and project tagging."""

from __future__ import annotations

from ssrn_autobot.models import Paper
from ssrn_autobot.taxonomy import PROJECT_LABEL_RULES, TOPIC_KEYWORDS


def apply_tags(paper: Paper) -> Paper:
    """Apply topic and project labels using keyword matches."""
    text = paper.text_blob()

    topic_labels: list[str] = []
    for topic_name, (keywords, _) in TOPIC_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            topic_labels.append(topic_name)

    project_labels: list[str] = []
    for project_name, keywords in PROJECT_LABEL_RULES.items():
        if any(kw in text for kw in keywords):
            project_labels.append(project_name)

    paper.topic_labels = topic_labels
    paper.project_labels = project_labels
    return paper
