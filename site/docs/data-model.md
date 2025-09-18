# Data Model

All glossary entries follow the schema defined in `schema/term.schema.json`. Each
YAML file under `data/terms/` captures a single concept and includes metadata for
cross-team alignment.

```yaml
term: "example"
aliases:
  - "synonym"
categories:
  - "Category name"
roles:
  - "product"
part_of_speech: "noun"
short_def: "≤40 word summary."
long_def: >-
  120–200 word explanation that provides history, context, and operational
  considerations.
audiences:
  exec: "Business-ready framing."
  engineer: "Technical framing."
examples:
  do:
    - "What good practice looks like."
  dont:
    - "What to avoid."
governance:
  nist_rmf_tags:
    - "tag"
  risk_notes: "Key compliance considerations."
relationships:
  broader:
    - "parent term"
  narrower:
    - "child term"
  related:
    - "peer term"
citations:
  - source: "Credible reference"
    url: "https://example.com"
license: "CC BY-SA 4.0"
status: "draft"
last_reviewed: "2024-01-01"
```

## Validation rules

- `short_def` must be **40 words or fewer**.
- `long_def` must fall between **80 and 220 words**.
- Executive and engineering variants are mandatory.
- Provide at least one example in each of the `do` and `dont` lists.
- Assign at least one category so entries can be grouped in navigation and search.
- Tag entries with at least one role (`product`, `engineering`, `data_science`, `policy`,
  `legal`, `security`, or `communications`) for role-based guidance.
- Cite sources with URLs to reputable glossaries, standards, or academic
  references.

Run `make validate` locally to confirm entries match both the JSON Schema and
custom rules.
