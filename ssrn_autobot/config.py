"""Configuration loading for ssrn_autobot."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class AppConfig:
    """Application-level configuration loaded from YAML."""

    database_path: Path = Path("data/ssrn_autobot.db")
    digest_output_dir: Path = Path("output/digests")
    sources: list[str] = field(default_factory=lambda: ["mock"])
    top_n: int = 10
    log_level: str = "INFO"


def load_config(path: Path) -> AppConfig:
    """Load app config from YAML file path."""
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AppConfig(
        database_path=Path(data.get("database_path", "data/ssrn_autobot.db")),
        digest_output_dir=Path(data.get("digest_output_dir", "output/digests")),
        sources=data.get("sources", ["mock"]),
        top_n=int(data.get("top_n", 10)),
        log_level=str(data.get("log_level", "INFO")),
    )


def write_example_config(path: Path) -> None:
    """Write an example config YAML to disk."""
    content = """database_path: data/ssrn_autobot.db
digest_output_dir: output/digests
sources:
  - mock
top_n: 10
log_level: INFO
"""
    path.write_text(content, encoding="utf-8")
