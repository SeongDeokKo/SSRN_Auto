"""CLI entrypoint for ssrn_autobot."""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from ssrn_autobot.collector.base import SourceCollector
from ssrn_autobot.collector.mock_source import MockSource
from ssrn_autobot.collector.ssrn_placeholder import SSRNPlaceholderSource
from ssrn_autobot.config import load_config, write_example_config
from ssrn_autobot.database import Database
from ssrn_autobot.logging_utils import setup_logging
from ssrn_autobot.processing.dedup import deduplicate_papers
from ssrn_autobot.processing.normalize import normalize_candidate
from ssrn_autobot.processing.scoring import score_paper
from ssrn_autobot.processing.summarizer import summarize_paper
from ssrn_autobot.processing.tagging import apply_tags
from ssrn_autobot.publisher.markdown_digest import write_daily_digest
from ssrn_autobot.utils import normalize_title

LOGGER = logging.getLogger("ssrn_autobot")


def _source_registry() -> dict[str, SourceCollector]:
    return {
        "mock": MockSource(),
        "ssrn_placeholder": SSRNPlaceholderSource(),
    }


def cmd_init_config(args: argparse.Namespace) -> int:
    """Initialize example config file."""
    out = Path(args.config)
    if out.exists() and not args.force:
        LOGGER.error("Config already exists at %s (use --force to overwrite)", out)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    write_example_config(out)
    LOGGER.info("Wrote config file to %s", out)
    return 0


def _collect_and_process(config_path: Path) -> tuple[Database, list]:
    cfg = load_config(config_path)
    setup_logging(cfg.log_level)
    db = Database(cfg.database_path)
    db.init_schema()

    registry = _source_registry()
    normalized = []

    for source_name in cfg.sources:
        collector = registry.get(source_name)
        if not collector:
            LOGGER.warning("Unknown source '%s' skipped.", source_name)
            continue
        try:
            candidates = collector.collect()
        except Exception as exc:  # pragma: no cover
            LOGGER.exception("Source '%s' failed: %s", source_name, exc)
            continue

        LOGGER.info("Collected %s candidates from %s", len(candidates), source_name)
        normalized.extend(normalize_candidate(c) for c in candidates)

    deduped = deduplicate_papers(normalized)
    LOGGER.info("Deduplicated papers: %s -> %s", len(normalized), len(deduped))

    processed = []
    for paper in deduped:
        paper.score = score_paper(paper)
        apply_tags(paper)
        summarize_paper(paper)
        db.upsert_paper(paper, normalize_title(paper.title))
        processed.append(paper)

    return db, sorted(processed, key=lambda p: p.score, reverse=True)


def cmd_run(args: argparse.Namespace) -> int:
    """Run full ingest/process and write digest."""
    cfg = load_config(Path(args.config))
    setup_logging(cfg.log_level)
    db, papers = _collect_and_process(Path(args.config))
    top = papers[: cfg.top_n]
    digest_path = write_daily_digest(cfg.digest_output_dir, top)
    LOGGER.info("Run complete. Top papers: %s. Digest: %s", len(top), digest_path)
    _ = db
    return 0


def cmd_digest(args: argparse.Namespace) -> int:
    """Write digest from existing DB records."""
    cfg = load_config(Path(args.config))
    setup_logging(cfg.log_level)
    db = Database(cfg.database_path)
    db.init_schema()
    top = db.fetch_top_papers(limit=cfg.top_n)
    digest_path = write_daily_digest(cfg.digest_output_dir, top)
    LOGGER.info("Digest written from DB records: %s", digest_path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Construct CLI parser."""
    parser = argparse.ArgumentParser(prog="ssrn_autobot", description="Local SSRN-oriented research digest assistant")
    parser.add_argument("--config", default="config.yaml", help="Path to YAML config file")

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init-config", help="Write an example config file")
    p_init.add_argument("--force", action="store_true", help="Overwrite existing config")
    p_init.set_defaults(func=cmd_init_config)

    p_run = subparsers.add_parser("run", help="Collect/process papers and write digest")
    p_run.set_defaults(func=cmd_run)

    p_digest = subparsers.add_parser("digest", help="Write digest from DB only")
    p_digest.set_defaults(func=cmd_digest)

    return parser


def main() -> int:
    """CLI main."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
