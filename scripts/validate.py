"""Validate glossary term files against custom rules."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from glossary_utils import safe_load_path

SCHEMA_PATH = Path("schema/term.schema.json")
ALLOWED_PARTS_OF_SPEECH = {"noun", "noun_phrase", "verb", "adjective", "process", "concept"}
ALLOWED_STATUSES = {"draft", "reviewed", "approved", "deprecated"}
ALLOWED_LICENSES = {"CC BY-SA 4.0"}
ALLOWED_ROLES = {
    "product",
    "engineering",
    "data_science",
    "policy",
    "legal",
    "security",
    "communications",
}
MAX_SHORT_DEF_WORDS = 40
MIN_LONG_DEF_WORDS = 80
MAX_LONG_DEF_WORDS = 220


def load_required_fields() -> List[str]:
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    return schema.get("required", [])


def normalize_term(term: str) -> str:
    slug = term.strip().lower().replace(" ", "-").replace("_", "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug


def count_words(text: str) -> int:
    return len([word for word in text.split() if word.strip()])


def ensure_list_of_strings(value, *, allow_empty: bool = False) -> bool:
    if not isinstance(value, list):
        return False
    if not allow_empty and len(value) == 0:
        return False
    return all(isinstance(item, str) and item.strip() for item in value)


def validate_file(path: Path, required_fields: List[str]) -> List[str]:
    errors: List[str] = []
    data = safe_load_path(path)

    if not isinstance(data, dict):
        return [f"{path}: top-level YAML must define a mapping"]

    for field in required_fields:
        if field not in data:
            errors.append(f"{path}: missing required field '{field}'")

    term = data.get("term")
    if isinstance(term, str):
        if normalize_term(term) != path.stem.lower():
            errors.append(
                f"{path}: term '{term}' should match filename slug '{path.stem.lower()}'"
            )
    else:
        errors.append(f"{path}: 'term' must be a string")

    aliases = data.get("aliases")
    if not ensure_list_of_strings(aliases):
        errors.append(f"{path}: 'aliases' must be a non-empty list of strings")

    categories = data.get("categories")
    if not ensure_list_of_strings(categories):
        errors.append(f"{path}: 'categories' must be a non-empty list of strings")

    roles = data.get("roles")
    if not ensure_list_of_strings(roles):
        errors.append(f"{path}: 'roles' must be a non-empty list of strings")
    else:
        invalid_roles = sorted({role for role in roles if role not in ALLOWED_ROLES})
        if invalid_roles:
            errors.append(
                f"{path}: roles {invalid_roles} are invalid (expected subset of {sorted(ALLOWED_ROLES)})"
            )

    part = data.get("part_of_speech")
    if part not in ALLOWED_PARTS_OF_SPEECH:
        errors.append(f"{path}: part_of_speech '{part}' is invalid")

    short_def = data.get("short_def")
    if isinstance(short_def, str):
        word_count = count_words(short_def)
        if word_count > MAX_SHORT_DEF_WORDS:
            errors.append(
                f"{path}: short_def has {word_count} words (max {MAX_SHORT_DEF_WORDS})"
            )
    else:
        errors.append(f"{path}: 'short_def' must be a string")

    long_def = data.get("long_def")
    if isinstance(long_def, str):
        word_count = count_words(long_def)
        if word_count < MIN_LONG_DEF_WORDS or word_count > MAX_LONG_DEF_WORDS:
            errors.append(
                f"{path}: long_def has {word_count} words (expected {MIN_LONG_DEF_WORDS}-{MAX_LONG_DEF_WORDS})"
            )
    else:
        errors.append(f"{path}: 'long_def' must be a string")

    audiences = data.get("audiences")
    if isinstance(audiences, dict):
        for audience in ("exec", "engineer"):
            value = audiences.get(audience)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{path}: audiences.{audience} must be a non-empty string")
    else:
        errors.append(f"{path}: 'audiences' must be a mapping with exec/engineer keys")

    examples = data.get("examples")
    if isinstance(examples, dict):
        for key in ("do", "dont"):
            entries = examples.get(key)
            if not ensure_list_of_strings(entries):
                errors.append(f"{path}: examples.{key} must include at least one example")
    else:
        errors.append(f"{path}: 'examples' must define 'do' and 'dont' lists")

    governance = data.get("governance")
    if isinstance(governance, dict):
        tags = governance.get("nist_rmf_tags")
        if tags is not None and not ensure_list_of_strings(tags, allow_empty=False):
            errors.append(f"{path}: governance.nist_rmf_tags must be a list of strings")
        notes = governance.get("risk_notes")
        if notes is not None and not isinstance(notes, str):
            errors.append(f"{path}: governance.risk_notes must be a string when provided")
    else:
        errors.append(f"{path}: 'governance' must be a mapping")

    relationships = data.get("relationships")
    if isinstance(relationships, dict):
        for rel_key in ("broader", "narrower", "related"):
            rel_value = relationships.get(rel_key)
            if rel_value is not None and not ensure_list_of_strings(rel_value, allow_empty=True):
                errors.append(f"{path}: relationships.{rel_key} must be a list of strings")
    else:
        errors.append(f"{path}: 'relationships' must be a mapping")

    citations = data.get("citations")
    if isinstance(citations, list) and citations:
        for idx, citation in enumerate(citations):
            if not isinstance(citation, dict):
                errors.append(f"{path}: citation #{idx + 1} must be a mapping")
                continue
            if not isinstance(citation.get("source"), str) or not citation["source"].strip():
                errors.append(f"{path}: citation #{idx + 1} missing 'source'")
            url = citation.get("url")
            if not isinstance(url, str) or not url.startswith("http"):
                errors.append(f"{path}: citation #{idx + 1} has invalid 'url'")
    else:
        errors.append(f"{path}: 'citations' must contain at least one entry")

    license_value = data.get("license")
    if license_value not in ALLOWED_LICENSES:
        errors.append(f"{path}: license '{license_value}' must be one of {sorted(ALLOWED_LICENSES)}")

    status = data.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"{path}: status '{status}' is not valid")

    last_reviewed = data.get("last_reviewed")
    if isinstance(last_reviewed, str):
        try:
            datetime.fromisoformat(last_reviewed)
        except ValueError:
            errors.append(f"{path}: last_reviewed '{last_reviewed}' is not ISO date (YYYY-MM-DD)")
    else:
        errors.append(f"{path}: 'last_reviewed' must be an ISO date string")

    return errors


def iter_term_files(data_dir: Path) -> Iterable[Path]:
    return sorted(data_dir.glob("*.yml"))


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Validate glossary term files")
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/terms"),
        help="Directory containing YAML term files",
    )
    args = parser.parse_args(argv)

    if not SCHEMA_PATH.exists():
        print(f"Schema not found at {SCHEMA_PATH}", file=sys.stderr)
        return 1

    required_fields = load_required_fields()
    term_files = list(iter_term_files(args.data_dir))
    if not term_files:
        print(f"No term files found in {args.data_dir}", file=sys.stderr)
        return 1

    all_errors: List[str] = []
    for file_path in term_files:
        all_errors.extend(validate_file(file_path, required_fields))

    if all_errors:
        print("Validation failed:", file=sys.stderr)
        for message in all_errors:
            print(f" - {message}", file=sys.stderr)
        return 1

    print(f"Validated {len(term_files)} term(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
