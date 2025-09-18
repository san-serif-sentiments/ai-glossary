"""Build aggregated JSON files from glossary YAML entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

import sys

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glossary_utils import safe_load_path

SITE_ASSETS_DIR = REPO_ROOT / "site" / "docs" / "assets"


def normalize_term(term: str) -> str:
    slug = term.strip().lower().replace(" ", "-").replace("_", "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug


def load_terms(data_dir: Path) -> List[Dict[str, Any]]:
    terms: List[Dict[str, Any]] = []
    for path in sorted(data_dir.glob("*.yml")):
        data = safe_load_path(path) or {}
        if not isinstance(data, dict):
            raise ValueError(f"Expected mapping in {path}")
        canonical = str(data.get("term", path.stem))
        data["slug"] = normalize_term(canonical)
        data["_source_file"] = str(path)
        terms.append(data)
    return terms


def build_search_index(terms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    index: List[Dict[str, Any]] = []
    for entry in terms:
        index.append(
            {
                "term": entry.get("term"),
                "aliases": entry.get("aliases", []),
                "categories": entry.get("categories", []),
                "roles": entry.get("roles", []),
                "short_def": entry.get("short_def"),
                "nist_rmf_tags": entry.get("governance", {}).get("nist_rmf_tags", []),
                "status": entry.get("status"),
                "slug": entry.get("slug"),
            }
        )
    return index


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build JSON outputs from glossary data")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/terms"),
        help="Directory containing YAML term files",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("build"),
        help="Directory for generated JSON files",
    )
    args = parser.parse_args()

    terms = load_terms(args.data_dir)
    if not terms:
        raise SystemExit(f"No term files found in {args.data_dir}")

    glossary_payload = {"terms": terms}
    search_payload = build_search_index(terms)

    write_json(args.output_dir / "glossary.json", glossary_payload)
    write_json(args.output_dir / "search-index.json", search_payload)

    # Ensure the MkDocs site has access to the search payload for client-side lookup.
    write_json(SITE_ASSETS_DIR / "glossary-search.json", search_payload)

    print(
        f"Wrote {len(terms)} term(s) to {args.output_dir / 'glossary.json'} and search index."
    )


if __name__ == "__main__":
    main()
