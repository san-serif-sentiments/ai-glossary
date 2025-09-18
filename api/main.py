"""FastAPI service that serves glossary terms from YAML files."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

import sys

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi import FastAPI, HTTPException, Query

from glossary_utils import safe_load_path

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "terms"

app = FastAPI(
    title="AI Glossary API",
    description="Lightweight API that exposes glossary entries maintained in YAML files.",
    version="0.1.0",
)


def normalize_term(term: str) -> str:
    slug = term.strip().lower().replace(" ", "-").replace("_", "-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug


@lru_cache(maxsize=1)
def _load_terms() -> Dict[str, dict]:
    terms: Dict[str, dict] = {}
    for path in sorted(DATA_DIR.glob("*.yml")):
        data = safe_load_path(path) or {}
        slug = normalize_term(data.get("term", path.stem))
        data["slug"] = slug
        data.setdefault("aliases", [])
        data.setdefault("categories", [])
        data.setdefault("roles", [])
        data["_source_file"] = str(path)
        terms[slug] = data
    return terms


def _terms_list() -> List[dict]:
    return list(_load_terms().values())


@app.get("/", tags=["metadata"])
def read_root() -> dict:
    return {
        "name": "AI Glossary",
        "description": "Structured, citation-backed AI glossary",
        "count": len(_load_terms()),
        "categories": sorted({cat for term in _terms_list() for cat in term.get("categories", [])}),
        "roles": sorted({role for term in _terms_list() for role in term.get("roles", [])}),
    }


def _matches_query(term: dict, query: str) -> bool:
    haystack = []
    haystack.append(term.get("term", ""))
    haystack.extend(term.get("aliases", []))
    haystack.append(term.get("short_def", ""))
    haystack.extend(term.get("categories", []))
    q = query.lower()
    return any(q in (value or "").lower() for value in haystack)


def _matches_category(term: dict, category: str) -> bool:
    term_categories = {value.lower() for value in term.get("categories", [])}
    targets = {value.strip().lower() for value in category.split(",") if value.strip()}
    return bool(term_categories & targets)


def _matches_role(term: dict, role: str) -> bool:
    term_roles = {value.lower() for value in term.get("roles", [])}
    targets = {value.strip().lower() for value in role.split(",") if value.strip()}
    return bool(term_roles & targets)


@app.get("/terms", tags=["terms"])
def list_terms(
    q: Optional[str] = Query(None, description="Free-text search across term names, aliases, and definitions."),
    category: Optional[str] = Query(
        None,
        description="Filter by category label. Multiple categories can be supplied as a comma-separated list.",
    ),
    status: Optional[str] = Query(None, description="Filter by status (draft, reviewed, approved, deprecated)."),
    alias: Optional[str] = Query(None, description="Return the entry matching a specific alias."),
    role: Optional[str] = Query(
        None,
        description="Filter by role slug (product, engineering, data_science, policy, legal, security, communications).",
    ),
) -> List[dict]:
    results = _terms_list()

    if q:
        results = [term for term in results if _matches_query(term, q)]

    if category:
        results = [term for term in results if _matches_category(term, category)]

    if status:
        expected = status.lower()
        results = [term for term in results if str(term.get("status", "")).lower() == expected]

    if role:
        results = [term for term in results if _matches_role(term, role)]

    if alias:
        alias_norm = alias.lower()
        results = [
            term
            for term in results
            if any(alias_norm == value.lower() for value in term.get("aliases", []))
        ]

    return results


@app.get("/terms/{slug}", tags=["terms"])
def get_term(slug: str) -> dict:
    term = _load_terms().get(slug)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@app.get("/categories", tags=["metadata"])
def list_categories() -> dict:
    categories = sorted({cat for term in _terms_list() for cat in term.get("categories", [])})
    return {"categories": categories}


@app.get("/roles", tags=["metadata"])
def list_roles() -> dict:
    roles = sorted({role for term in _terms_list() for role in term.get("roles", [])})
    return {"roles": roles}


@app.post("/refresh", tags=["metadata"], response_model=dict)
def refresh_terms() -> dict:
    _load_terms.cache_clear()  # type: ignore[attr-defined]
    refreshed = len(_load_terms())
    return {"refreshed": refreshed}
