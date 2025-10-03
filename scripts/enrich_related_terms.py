# scripts/enrich_related_terms.py
from __future__ import annotations
import json
import math
import os
import re
from collections import Counter
from pathlib import Path
from typing import List, Tuple
from urllib.parse import urlparse

IN = Path("build/glossary.json")
OUT_JSON = Path("build/related.json")
# IMPORTANT: since mkdocs.yml lives under site/, docs_dir is "docs"
OUT_DIR = Path("site/docs/includes/related")  # MkDocs will include these via --8<--

S3_INPUT_ENV = "INPUT_S3_URI"
S3_OUTPUT_ENV = "OUTPUT_S3_PREFIX"
AWS_REGION_ENV = "AWS_REGION"

MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # fast CPU model
TOP_K = 8
CACHE_DIR = Path(os.environ.get("GLOSSARY_EMBEDDING_CACHE", "models/all-MiniLM-L6-v2")).expanduser()


def _parse_s3_uri(uri: str) -> Tuple[str, str]:
    parsed = urlparse(uri)
    if parsed.scheme != "s3" or not parsed.netloc:
        raise ValueError(f"Invalid S3 URI: {uri}")
    key = parsed.path.lstrip("/")
    if not key:
        raise ValueError(f"S3 URI must include an object key: {uri}")
    return parsed.netloc, key


def _s3_client():
    try:
        import boto3  # type: ignore
    except ImportError as exc:  # pragma: no cover - optional dependency
        raise RuntimeError(
            "boto3 is required for S3 inputs/outputs. Install with `pip install boto3`."
        ) from exc

    region = os.environ.get(AWS_REGION_ENV)
    if region:
        return boto3.client("s3", region_name=region)
    return boto3.client("s3")


def _maybe_download_input() -> None:
    uri = os.environ.get(S3_INPUT_ENV)
    if not uri:
        return

    bucket, key = _parse_s3_uri(uri)
    client = _s3_client()
    IN.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading glossary from {uri} -> {IN}")
    client.download_file(bucket, key, str(IN))


def _maybe_upload_outputs() -> None:
    prefix = os.environ.get(S3_OUTPUT_ENV)
    if not prefix:
        return

    bucket, root_key = _parse_s3_uri(prefix)
    base = root_key.rstrip("/")
    client = _s3_client()

    json_key = f"{base}/related.json" if base else "related.json"
    print(f"Uploading {OUT_JSON} -> s3://{bucket}/{json_key}")
    client.upload_file(str(OUT_JSON), bucket, json_key)

    md_prefix = f"{base}/includes" if base else "includes"
    for path in OUT_DIR.glob("*.md"):
        dest_key = f"{md_prefix}/{path.name}" if md_prefix else path.name
        print(f"Uploading {path} -> s3://{bucket}/{dest_key}")
        client.upload_file(str(path), bucket, dest_key)


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b\w+\b", text.lower())


def _tfidf_embeddings(texts: List[str]) -> List[dict[str, float]]:
    tokenised = [Counter(_tokenize(text)) for text in texts]
    doc_freq: Counter[str] = Counter()
    for bucket in tokenised:
        doc_freq.update(bucket.keys())
    total_docs = len(texts)

    vectors: List[dict[str, float]] = []
    for bucket in tokenised:
        total_terms = sum(bucket.values()) or 1
        normalised: dict[str, float] = {}
        norm = 0.0
        for term, count in bucket.items():
            tf = count / total_terms
            idf = math.log((total_docs + 1) / (doc_freq[term] + 1)) + 1
            weight = tf * idf
            normalised[term] = weight
            norm += weight * weight
        norm = math.sqrt(norm) or 1.0
        vectors.append({term: weight / norm for term, weight in normalised.items()})
    return vectors


def _sparse_cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(weight * b.get(term, 0.0) for term, weight in a.items())


def _load_sentence_transformer(cache_candidate: Path, model_path_override: Path | None) -> Tuple[object, str] | None:
    """Attempt to load SentenceTransformer from cache or override."""
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ImportError:
        return None

    candidates = [path for path in [model_path_override, cache_candidate] if path]

    try:
        cache_candidate.mkdir(parents=True, exist_ok=True)
        model = SentenceTransformer(MODEL, cache_folder=str(cache_candidate))
        return model, "dense"
    except Exception as error:  # pragma: no cover
        last_error = error

    for candidate in candidates:
        if candidate and candidate.exists():
            try:
                model = SentenceTransformer(str(candidate))
                print(f"Loaded SentenceTransformer model from {candidate}")
                return model, "dense"
            except Exception as local_error:  # pragma: no cover
                last_error = local_error

    raise last_error  # type: ignore[misc]


def embed_texts(texts: List[str]) -> Tuple[List, str]:
    try:
        import huggingface_hub  # type: ignore
        if not hasattr(huggingface_hub, "cached_download"):
            try:
                from huggingface_hub import hf_hub_download  # type: ignore
            except ImportError:
                hf_hub_download = None  # type: ignore
            if hf_hub_download is not None:
                huggingface_hub.cached_download = hf_hub_download  # type: ignore[attr-defined]
    except ImportError:
        print("sentence-transformers not available; falling back to TF-IDF.", flush=True)
        return _tfidf_embeddings(texts), "sparse"

    try:
        env_override = os.environ.get("GLOSSARY_EMBEDDING_MODEL_PATH")
        override_path = Path(env_override).expanduser() if env_override else None
        loaded = _load_sentence_transformer(CACHE_DIR, override_path)
        if loaded is None:
            raise ImportError
        model, flavour = loaded
    except Exception as error:  # pragma: no cover
        print(f"Failed to load {MODEL} ({error}); falling back to TF-IDF.", flush=True)
        return _tfidf_embeddings(texts), "sparse"

    embeddings = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    return embeddings, flavour


def load_terms():
    data = json.loads(IN.read_text(encoding="utf-8"))
    items = []
    for t in data["terms"]:
        slug = (t.get("slug") or t["term"].strip().lower().replace(" ", "-"))
        body = " ".join(
            [
                t.get("term", ""),
                t.get("short_def", ""),
                t.get("long_def", ""),
                " ".join(t.get("aliases", [])),
                " ".join(t.get("categories", [])),
            ]
        )
        items.append({"slug": slug, "title": t["term"], "text": body})
    return items


def main():
    _maybe_download_input()
    terms = load_terms()
    texts = [x["text"] for x in terms]
    embeddings, flavour = embed_texts(texts)

    related = {}
    for i, a in enumerate(embeddings):
        scores = []
        for j, b in enumerate(embeddings):
            if i == j:
                continue
            if flavour == "dense":
                score = float(sum(x * y for x, y in zip(a, b)))
            else:
                score = _sparse_cosine(a, b)
            scores.append((score, j))
        scores.sort(reverse=True)
        top = scores[:TOP_K]
        related[terms[i]["slug"]] = [
            {"slug": terms[j]["slug"], "title": terms[j]["title"], "score": round(s, 3)}
            for s, j in top
        ]

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(related, ensure_ascii=False, indent=2), encoding="utf-8")

    # write small markdown includes per term
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for slug, lst in related.items():
        lines = ["\n**Related terms**\n", ""]
        for r in lst:
            lines.append(f"- [{r['title']}](../../terms/{r['slug']}.md)")
        (OUT_DIR / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Wrote related data: {OUT_JSON} and {OUT_DIR}/*.md")
    _maybe_upload_outputs()


if __name__ == "__main__":
    main()
