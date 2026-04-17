"""SQLite persistence layer."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from ssrn_autobot.models import Paper


class Database:
    """Simple SQLite wrapper for storing and retrieving papers."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_schema(self) -> None:
        """Initialize DB schema if not present."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT NOT NULL,
                    external_id TEXT,
                    title TEXT NOT NULL,
                    title_norm TEXT NOT NULL,
                    authors_json TEXT NOT NULL,
                    abstract TEXT NOT NULL,
                    url TEXT NOT NULL,
                    posted_date TEXT,
                    collected_at TEXT NOT NULL,
                    topic_labels_json TEXT NOT NULL,
                    project_labels_json TEXT NOT NULL,
                    score REAL NOT NULL,
                    summary TEXT NOT NULL,
                    why_it_matters TEXT NOT NULL,
                    action TEXT NOT NULL,
                    UNIQUE(source, external_id),
                    UNIQUE(title_norm)
                )
                """
            )

    def upsert_paper(self, paper: Paper, title_norm: str) -> None:
        """Insert or replace by external id or normalized title constraints."""
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO papers (
                    source, external_id, title, title_norm, authors_json, abstract, url,
                    posted_date, collected_at, topic_labels_json, project_labels_json,
                    score, summary, why_it_matters, action
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(title_norm) DO UPDATE SET
                    source=excluded.source,
                    external_id=COALESCE(excluded.external_id, papers.external_id),
                    title=excluded.title,
                    authors_json=excluded.authors_json,
                    abstract=excluded.abstract,
                    url=excluded.url,
                    posted_date=excluded.posted_date,
                    collected_at=excluded.collected_at,
                    topic_labels_json=excluded.topic_labels_json,
                    project_labels_json=excluded.project_labels_json,
                    score=excluded.score,
                    summary=excluded.summary,
                    why_it_matters=excluded.why_it_matters,
                    action=excluded.action
                """,
                (
                    paper.source,
                    paper.external_id,
                    paper.title,
                    title_norm,
                    json.dumps(paper.authors),
                    paper.abstract,
                    paper.url,
                    paper.posted_date,
                    paper.collected_at,
                    json.dumps(paper.topic_labels),
                    json.dumps(paper.project_labels),
                    paper.score,
                    paper.summary,
                    paper.why_it_matters,
                    paper.action,
                ),
            )

    def fetch_top_papers(self, limit: int = 10) -> list[Paper]:
        """Fetch top scored papers from DB."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT * FROM papers
                ORDER BY score DESC, collected_at DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

        papers: list[Paper] = []
        for row in rows:
            papers.append(
                Paper(
                    source=row["source"],
                    external_id=row["external_id"],
                    title=row["title"],
                    authors=json.loads(row["authors_json"]),
                    abstract=row["abstract"],
                    url=row["url"],
                    posted_date=row["posted_date"],
                    collected_at=row["collected_at"],
                    topic_labels=json.loads(row["topic_labels_json"]),
                    project_labels=json.loads(row["project_labels_json"]),
                    score=float(row["score"]),
                    summary=row["summary"],
                    why_it_matters=row["why_it_matters"],
                    action=row["action"],
                )
            )
        return papers
