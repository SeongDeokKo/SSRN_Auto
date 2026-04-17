# ssrn-autobot

A local Python MVP research assistant for SSRN-related working paper monitoring in asset pricing.

## Purpose

`ssrn-autobot` scans source collectors (mock now, SSRN placeholder ready), normalizes records, deduplicates, scores relevance, tags papers by topics/projects, stores everything in SQLite, and writes a daily markdown digest.

The design is intentionally modular so you can plug in real SSRN collection and LLM summarization later without rewriting the core pipeline.

## Folder structure

```text
ssrn_autobot/
  __init__.py
  __main__.py
  config.py
  logging_utils.py
  models.py
  taxonomy.py
  database.py
  utils.py
  collector/
    base.py
    mock_source.py
    ssrn_placeholder.py
  processing/
    normalize.py
    dedup.py
    scoring.py
    tagging.py
    summarizer.py
  publisher/
    markdown_digest.py
tests/
  test_scoring.py
  test_dedup.py
requirements.txt
config.example.yaml
```

## Pipeline overview

1. **Config load** from YAML (`config.py`).
2. **Collect** from enabled sources (`collector/*`).
3. **Normalize** into `Paper` dataclass (`processing/normalize.py`).
4. **Deduplicate** by external ID and normalized title (`processing/dedup.py`).
5. **Score** via transparent weighted keywords (`processing/scoring.py`).
6. **Tag** topic + project labels (`processing/tagging.py`).
7. **Summarize** with local heuristic templates (`processing/summarizer.py`).
8. **Persist** to SQLite (`database.py`).
9. **Publish** daily markdown digest (`publisher/markdown_digest.py`).

## Conda setup (Windows / Anaconda Prompt)

From Anaconda Prompt:

```bash
cd C:\path\to\SSRN_Auto
conda create -n ssrn-autobot python=3.11 -y
conda activate ssrn-autobot
pip install -r requirements.txt
```

## First run

```bash
python -m ssrn_autobot init-config
```

This creates `config.yaml`. You can also copy `config.example.yaml` to `config.yaml` and edit paths/sources.

Then run the full pipeline:

```bash
python -m ssrn_autobot run
```

Outputs:
- SQLite DB at `data/ssrn_autobot.db` (default)
- Digest markdown in `output/digests/` (default)

Generate digest only from current DB:

```bash
python -m ssrn_autobot digest
```

## CLI commands

- `python -m ssrn_autobot init-config`
- `python -m ssrn_autobot run`
- `python -m ssrn_autobot digest`

## How to extend data sources

1. Add a new class implementing `SourceCollector` in `ssrn_autobot/collector/`.
2. Return `list[CandidatePaper]` from `collect()`.
3. Register it in `_source_registry()` in `ssrn_autobot/__main__.py`.
4. Add the source name to `sources` in `config.yaml`.

## Where to add LLM summarization later

Replace/extend `processing/summarizer.py` with a strategy interface, e.g.:
- `HeuristicSummarizer` (current)
- `LLMSummarizer` (future)

Since scoring/tagging/storage consume populated `Paper` fields, no major pipeline rewrite is needed.

## Tests

```bash
pytest -q
```

Covers:
- scoring behavior for relevant vs irrelevant papers
- deduplication behavior for external IDs and normalized titles
