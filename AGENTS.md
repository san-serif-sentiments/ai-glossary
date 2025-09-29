# Agent Guidelines

## Repository-wide conventions
- Run `make validate` before opening a PR to ensure the glossary schema, link checker, and MkDocs build remain healthy.
- Prefer updating source YAML in `data/terms/` and regenerate derived content via the existing tooling instead of editing generated files directly.

## Documentation links
- When you author Markdown links inside Markdown content, use the `.md` source paths so MkDocs can rewrite them.
- When embedding raw HTML inside Markdown (for example, hero banners or custom grids), point internal links at the built artifact using `path/index.html` so the static site and the link validator both resolve the destination.
- Keep external citations limited to sources that respond with HTTP 200 without authentication to avoid breaking the validation pipeline.

## Commit hygiene
- Group related documentation and YAML updates into focused commits with descriptive messages.
- Avoid committing regenerated artifacts unless your change modifies the underlying source or affects the output.
