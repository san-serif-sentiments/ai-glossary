# Contributing

Thank you for helping expand the glossary. Follow these steps to get started:

1. Fork the repository and create a feature branch.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create or update a YAML file under `data/terms/`, covering categories, roles, citations, and examples.
4. Run `make validate` to ensure schema and lint checks pass.
5. Run `make build` followed by `cd site && mkdocs build --strict` to confirm the docs compile cleanly.
6. Open a pull request using the provided template.

See the root-level `CONTRIBUTING.md` for detailed guidance, including
formatting rules, review checklist, and citation requirements.
