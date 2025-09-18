"""FastAPI service that serves glossary terms from YAML files."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List

import sys

CURRENT_DIR = Path(__file__).resolve().parent
REPO_ROOT = CURRENT_DIR.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi import FastAPI, HTTPException

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
    }


@app.get("/terms", tags=["terms"])
def list_terms() -> List[dict]:
    return _terms_list()


@app.get("/terms/{slug}", tags=["terms"])
def get_term(slug: str) -> dict:
    term = _load_terms().get(slug)
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    return term


@app.post("/refresh", tags=["metadata"], response_model=dict)
def refresh_terms() -> dict:
    _load_terms.cache_clear()  # type: ignore[attr-defined]
    refreshed = len(_load_terms())
    return {"refreshed": refreshed}
