# Contributing to the AI Glossary

Thank you for helping build a high-quality, shared vocabulary for AI.

## Ground rules

- Be respectful and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Open an issue before large or controversial changes.
- Keep PRs focused: add or update **one term** (or a closely related set of
  metadata files) per pull request.
- Provide at least **one reputable citation** for every definition.
- Prefer paraphrasing over copying. All contributions are shared under
  [CC BY-SA 4.0](CONTENT_LICENSE).

## Workflow

1. Fork the repository and create a feature branch.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the validation suite before committing:
   ```bash
   make validate
   ```
4. Regenerate JSON outputs when adding or updating terms:
   ```bash
   python scripts/build_index.py
   ```
5. Commit changes with clear messages and open a pull request using the
   provided template.

## Authoring a term

All term files live in `data/terms/` and must:

- Be named after the canonical term (kebab-case), e.g., `retrieval-augmented-generation.yml`.
- Match the schema defined in `schema/term.schema.json`.
- Include:
  - `short_def` (≤40 words, plain language)
  - `long_def` (120–200 words, structured paragraphs welcome)
  - `audiences.exec` and `audiences.engineer`
  - At least one `examples.do` entry and one `examples.dont` entry
  - Governance notes (`nist_rmf_tags`, `risk_notes`) when applicable
  - `citations` with `source` and `url`
  - `status` lifecycle field (`draft`, `reviewed`, `approved`, `deprecated`)
- Use inclusive language and avoid marketing claims.

## Review checklist

Reviewers use the following checklist:

- [ ] Schema validation succeeds (`make validate`).
- [ ] `short_def` <= 40 words and is free of jargon.
- [ ] `long_def` provides necessary context (120–200 words).
- [ ] Executive and engineering explanations are present and audience-appropriate.
- [ ] Examples illustrate correct and incorrect usage.
- [ ] At least one credible citation is provided.
- [ ] NIST RMF tags or risk notes supplied when relevant.
- [ ] No obvious copy/paste without attribution.

## Questions?

Open a [discussion](https://github.com/your-org/ai-glossary/discussions) or reach
out via issues if you are unsure about anything.
