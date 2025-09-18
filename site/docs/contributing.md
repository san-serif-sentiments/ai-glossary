# Contributing

Thank you for helping expand the glossary. Follow these steps to get started:

1. Fork the repository and create a feature branch.
2. Install dependencies with `pip install -r requirements.txt`.
3. Create or update a YAML file under `data/terms/`.
4. Run `make validate` to ensure schema and lint checks pass.
5. Regenerate JSON outputs using `python scripts/build_index.py` (optional but recommended).
6. Open a pull request using the provided template.

See the root-level [CONTRIBUTING.md](../CONTRIBUTING.md) for detailed guidance,
including formatting rules, review checklist, and citation requirements.
