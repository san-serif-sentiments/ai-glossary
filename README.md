# AI Glossary

An open, living glossary that bridges product, engineering, and governance language for artificial intelligence systems. Each term is stored as structured data so it can power documentation, APIs, and downstream tools.

## Project goals

- Harmonize terminology used by product, engineering, and policy teams.
- Capture sourcing, examples, and governance context for every term.
- Provide audience-aware definitions (executive and engineering perspectives).
- Publish content as both a static site and machine-readable datasets.

## Repository layout

```
ai-glossary/
  README.md
  LICENSE
  CONTENT_LICENSE
  CONTRIBUTING.md
  CODE_OF_CONDUCT.md
  schema/term.schema.json
  data/terms/
    ... individual YAML entries ...
  scripts/
    validate.py
    build_index.py
  site/
    mkdocs.yml
    docs/
      index.md
  api/
    main.py
  .github/
    workflows/
      validate.yml
      build_release.yml
    ISSUE_TEMPLATE.md
    PULL_REQUEST_TEMPLATE.md
  Makefile
  requirements.txt
```

## Getting started

1. Create and activate a Python 3.10+ virtual environment (one-liner provided):
   ```bash
   make venv
   source .venv/bin/activate
   ```
   The target installs dependencies inside `.venv/`. If you prefer manual setup, run `python3 -m venv .venv` followed by `pip install -r requirements.txt` instead.
3. Validate all glossary entries:
   ```bash
   make validate
   ```
4. Rebuild derived assets (JSON index + Markdown term pages):
   ```bash
   make build
   ```
   This writes fresh JSON files to `build/`, regenerates Markdown documentation under
   `site/docs/terms/`, and refreshes the MkDocs navigation/search assets.
5. Compile the MkDocs site (strict mode treats warnings as errors):
   ```bash
   cd site
   mkdocs build --strict
   ```
   Use plain `mkdocs build` only for fast previews; rely on the `--strict` flag before pushing so missing links or nav entries fail loudly.
6. Run automated tests:
   ```bash
   python -m unittest discover -s tests
   ```
   The suite exercises the FastAPI filters (e.g., role and alias lookups) to confirm responses stay consistent.

Need to refresh just the term documentation? Run `make render-docs`.

The MkDocs site (in `site/`) and FastAPI service (in `api/`) consume the YAML files generated under `data/terms/`.

## Data model

Each term file under `data/terms/` must satisfy `schema/term.schema.json`. Highlights:

- `term`: canonical name that should match the filename.
- `aliases`: alternative spellings or related expressions.
- `categories`: content buckets (e.g., LLM Core, Retrieval & RAG) used for navigation and search.
- `roles`: audience tags (`product`, `engineering`, `data_science`, `policy`, `legal`,
  `security`, `communications`) used for role-based discovery.
- `short_def`: ≤40-word description for broad audiences.
- `audiences.exec` and `audiences.engineer`: tailored explanations.
- `examples.do` / `examples.dont`: positive and negative illustrations.
- `governance`: risk-related notes and NIST RMF tags when applicable.
- `citations`: at least one reputable source with URL.
- `status`: lifecycle state (`draft`, `reviewed`, `approved`, `deprecated`).

## Search & API quick reference

- Browse the static site locally at `site/site/index.html` after running the build steps. The
  **Glossary Search** page filters terms by name, alias, category, or status using the generated
  `assets/glossary-search.json` payload.
- Serve the FastAPI project with `make serve-api` and query endpoints:
  - `GET /terms?q=retrieval&category=Retrieval%20%26%20RAG`
  - `GET /terms?alias=RAG`
  - `GET /terms?status=draft`
  - `GET /terms?role=policy`
  - `GET /categories`
  - `GET /roles`
  - `GET /terms/quantization`
  - `POST /refresh`
- Explore the documentation via
  - `site/site/search/index.html` (interactive filters)
  - `site/site/roles/index.html` (role starter packs)
  - `site/site/categories/index.html` (category explorer)

## Governance

- Contributions must follow the [Contributor Covenant](CODE_OF_CONDUCT.md).
- Every PR should modify a single term (or add a new one) and include citations.
- Automated checks enforce schema compliance, lint rules, and documentation builds.

## How teams use it

- **Enable shared language** – product, engineering, legal, and policy teams consult the same
  definitions, examples, and governance notes.
- **Bootstrap onboarding** – role starter packs highlight the must-know terms for new hires in
  PM, platform, data science, policy, legal, security, and communications roles.
- **Power multiple surfaces** – structured YAML drives the static site, a search JSON payload,
  and FastAPI endpoints, so downstream tools can embed the glossary directly.
- **Support governance workflows** – each term carries NIST RMF tags, risk notes, and citations,
  making it easy to reference during audits, model cards, and privacy reviews.

## License

- Code is provided under the [MIT License](LICENSE).
- Content (YAML term files) is provided under [CC BY-SA 4.0](CONTENT_LICENSE).
