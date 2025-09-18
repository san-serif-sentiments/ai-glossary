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

1. Create and activate a Python 3.10+ virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Validate all glossary entries:
   ```bash
   make validate
   ```
4. Regenerate JSON outputs after editing entries:
   ```bash
   python scripts/build_index.py
   ```

The MkDocs site (in `site/`) and FastAPI service (in `api/`) consume the YAML files generated under `data/terms/`.

## Data model

Each term file under `data/terms/` must satisfy `schema/term.schema.json`. Highlights:

- `term`: canonical name that should match the filename.
- `aliases`: alternative spellings or related expressions.
- `short_def`: ≤40-word description for broad audiences.
- `audiences.exec` and `audiences.engineer`: tailored explanations.
- `examples.do` / `examples.dont`: positive and negative illustrations.
- `governance`: risk-related notes and NIST RMF tags when applicable.
- `citations`: at least one reputable source with URL.
- `status`: lifecycle state (`draft`, `reviewed`, `approved`, `deprecated`).

## Governance

- Contributions must follow the [Contributor Covenant](CODE_OF_CONDUCT.md).
- Every PR should modify a single term (or add a new one) and include citations.
- Automated checks enforce schema compliance, lint rules, and documentation builds.

## Roadmap

- **v0.1** – 50 core LLM and governance terms with MkDocs site & JSON index.
- **v0.2** – 120+ terms, NIST RMF crosswalks, improved search metadata.
- **v0.3** – Hosted API, embeddable widget, automated synonym suggestions.

## License

- Code is provided under the [MIT License](LICENSE).
- Content (YAML term files) is provided under [CC BY-SA 4.0](CONTENT_LICENSE).
