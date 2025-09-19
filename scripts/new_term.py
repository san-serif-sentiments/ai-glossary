"""Scaffold a new glossary term YAML file with quality guardrails."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from textwrap import dedent

import sys

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
DATA_DIR = REPO_ROOT / "data" / "terms"


def slugify(value: str) -> str:
    slug = value.strip().lower().replace(" ", "-").replace("_", "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug


def build_template(term: str) -> str:
    today = date.today().isoformat()
    short_placeholder = "TODO: Add a 1-2 sentence short definition (<=320 characters)."
    long_placeholder = (
        "TODO: Draft a longer definition (80-220 words) covering purpose, actors, and governance."
    )
    exec_placeholder = "Explain why this matters for strategy, risk, or customer outcomes."
    eng_placeholder = "Outline implementation, data, or operational expectations."

    return dedent(
        f"""term: "{term.lower()}"
aliases:
  - "{term.title()}"
categories:
  - "TODO category"
roles:
  - "product"
  - "engineering"
part_of_speech: "concept"
short_def: "{short_placeholder}"
long_def: >-
  {long_placeholder}
audiences:
  exec: "{exec_placeholder}"
  engineer: "{eng_placeholder}"
examples:
  do:
    - "TODO: Add a best-practice example."
  dont:
    - "TODO: Add an anti-pattern example."
governance:
  nist_rmf_tags:
    - "TODO"
  risk_notes: "TODO: Capture risks or controls."
relationships:
  broader:
    - "TODO"
  related:
    - "TODO"
citations:
  - source: "TODO: Primary reference"
    url: "https://example.com"
license: "CC BY-SA 4.0"
status: "draft"
last_reviewed: "{today}"
"""
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create a new glossary term scaffold")
    parser.add_argument("--term", required=True, help="Canonical term name (e.g., 'Assurance case')")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Allow overwriting an existing file if it already exists.",
    )
    args = parser.parse_args(argv)

    term = args.term.strip()
    if not term:
        parser.error("--term cannot be blank")

    slug = slugify(term)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    destination = DATA_DIR / f"{slug}.yml"

    if destination.exists() and not args.overwrite:
        parser.error(f"{destination} already exists. Use --overwrite to replace it.")

    destination.write_text(build_template(term), encoding="utf-8")
    print(f"Created scaffold at {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
