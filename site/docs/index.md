# AI Glossary

Welcome to the living glossary for artificial intelligence teams. The project
harmonizes terminology used across product, engineering, and governance
workstreams while keeping sourcing and risk context close to every definition.

## Why it exists

- **Shared language:** reduce confusion when policy, product, and engineering
  groups describe the same concept with different words.
- **Structured content:** every entry is stored as YAML so it can be reused in
  docs, APIs, or automated reviews.
- **Governance aware:** terms include NIST AI RMF tags, risk notes, and
  lifecycle status so compliance teams can trace the meaning.

## What you get today

- Seed entries for high-impact concepts like hallucination, retrieval-augmented
  generation, and quantization.
- A validation pipeline that enforces schema compliance, definition length, and
  presence of audience-specific explanations.
- JSON outputs (`build/glossary.json`, `build/search-index.json`) that downstream
  systems or chatbots can ingest.

## Next steps

- Expand to 50+ core LLM, ML Ops, and governance terms.
- Publish the static site via GitHub Pages.
- Stand up the lightweight API for programmatic access.

Ready to contribute? Check out the [Contribution guide](contributing.md).
