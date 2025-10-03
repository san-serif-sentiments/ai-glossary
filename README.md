# AI Glossary for Everyone

A plain-language handbook that keeps product, policy, engineering, and safety teams speaking the same AI vocabulary. Terms live in simple YAML files so the same content can generate a website, a JSON API, search indexes, and printable summaries. You do not need to be a developer to keep the glossary healthy—this guide walks you through every button to press.

---

## 1. The Big Picture (Explain Like I’m 12)

- Think of the glossary as a giant spreadsheet of AI words, their meanings, and why they matter.
- Each row lives in a YAML file under `data/terms/`. YAML is just a text format with key → value pairs.
- Scripts turn that YAML into:
  - Markdown pages for the public site (`site/docs/terms/...`).
  - A JSON file (`build/glossary.json`) that powers search and the API.
  - “Related term” callouts so readers can keep exploring without getting lost.
- A Makefile wraps every task. Typing `make something` runs the right script for you.

When you add or edit a term, you only touch one YAML file. Everything else is generated for you.

---

## 2. What You Get Out of the Box

- **100+ curated AI definitions** covering models, agents, governance, and risk controls.
- **Structured metadata**: aliases, audiences, lifecycle status, roles, and citations for every entry.
- **Docs site** built with MkDocs Material (lives under `site/`).
- **FastAPI backend** that serves the glossary as JSON.
- **Search index** ready to drop into web or mobile apps.
- **Related-term engine** that suggests eight neighbors for each concept.
- **Automation hooks** (Make targets + GitHub Actions) so you can validate and publish with one command.

---

## 3. Beginner Setup (No Prior Experience Needed)

You only need three tools installed once: Git, Python 3.10+, and Make.

1. **Download the project**
   ```bash
   git clone https://github.com/san-serif-sentiments/ai-glossary.git
   cd ai-glossary
   ```
2. **Create a safe sandbox for Python packages**
   ```bash
   make venv
   source .venv/bin/activate
   ```
   This builds `.venv/` and installs everything in `requirements.txt`.
3. **Check that all YAML files look good**
   ```bash
   make validate
   ```
   If you see “0 errors”, you are ready to go. If something is wrong, the command prints a friendly message pointing to the file and line number.
4. **Generate the website and JSON files**
   ```bash
   make build
   ```
   The results land in the `build/` and `site/docs/` folders.
5. **Preview the documentation**
   ```bash
   mkdocs serve -f site/mkdocs.yml
   ```
   Open <http://127.0.0.1:8000> in your browser. MkDocs auto-refreshes whenever a file changes.

You now have the full glossary running on your laptop.

---

## 4. Common Day-to-Day Tasks

### Add a Brand-New Term
1. Scaffold a file:
   ```bash
   make new-term NAME="Fast Weight Programmer"
   ```
   This creates `data/terms/fast-weight-programmer.yml` with helpful placeholders.
2. Fill in `short_def`, `long_def`, roles, examples, citations, and `last_reviewed`.
3. Run `make validate` to catch mistakes (missing citation, too-short definition, etc.).
4. Run `make build` so the JSON and docs stay in sync.
5. (Optional) Refresh related-term panels: `python scripts/enrich_related_terms.py`.

### Update an Existing Definition
1. Edit the YAML file in `data/terms/`.
2. Bump `last_reviewed` and adjust `status` if the definition is now approved.
3. Run `make validate && make build`.
4. Commit your change.

### Publish Your Changes

| Goal | Command | What happens |
| --- | --- | --- |
| Commit and push | `make github-push MESSAGE="Add term for Fast Weight Programmer"` | Runs checks, commits staged files, and pushes to `origin/main`. |
| Deploy docs to GitHub Pages | `make gh-pages` | Builds MkDocs in strict mode and publishes to the `gh-pages` branch. |
| Serve API locally | `make serve-api` | Starts FastAPI on `http://127.0.0.1:8000`. |

---

## 5. How Related Terms Work

The script `scripts/enrich_related_terms.py` reads `build/glossary.json`, embeds every term, calculates cosine similarity, and writes the top 8 neighbors to `build/related.json` plus `site/docs/includes/related/<slug>.md`.

You have two modes:

- **Dense embeddings (better)** – requires internet the first time to download the Hugging Face model `sentence-transformers/all-MiniLM-L6-v2`.
  ```bash
  source .venv/bin/activate
  pip install sentence-transformers==2.7.0
  python scripts/enrich_related_terms.py
  ```
- **Offline fallback** – if the model import fails, the script falls back to TF–IDF vectors. No setup needed, results are decent for quick drafts.

Output files live in `build/related/`. After the script runs, copy them into the docs with:
```bash
cp build/related/related.json build/related.json
rsync -av build/related/includes/ site/docs/includes/related/
```

### Scaling with Cloud Burst (Optional)
Need to refresh related terms for hundreds of entries on a lightweight laptop? Use the ready-made AWS Batch assets in `infra/aws-batch/`:
1. Build and push the Docker image (`infra/aws-batch/Dockerfile`).
2. Upload `build/glossary.json` to S3.
3. Register the job definition (`infra/aws-batch/job-definition.json`).
4. Submit a Batch job. The container downloads the glossary, computes related terms, and uploads `related.json` and the Markdown snippets back to S3.
5. Sync the outputs locally and copy them into the repo as shown above.

The README in `infra/aws-batch/` contains the exact commands (ELI12 steps included).

---

## 6. Folder Map

```
README.md                  ← This guide
Makefile                   ← One-stop shortcut list
requirements.txt           ← Python dependencies
schema/                    ← JSON Schema for validation
scripts/                   ← Helper scripts (build, validate, enrich)
api/                       ← FastAPI application
site/mkdocs.yml            ← Docs configuration
site/docs/terms/           ← Generated Markdown pages (do not edit by hand)
data/terms/                ← Source of truth (edit these)
build/                     ← Generated JSON assets
infra/aws-batch/           ← Container + Batch job templates for cloud runs
```

---

## 7. Troubleshooting (Friendly Answers)

| Problem | Try this |
| --- | --- |
| `make venv` fails | Ensure Python 3.10+ is installed. On macOS run `brew install python@3.12`. Delete `.venv/` and rerun. |
| `make validate` reports schema errors | The error message lists the file and the missing field. Open the YAML and fix the value. |
| Related-term script says `Unable to locate credentials` | Set AWS credentials or run locally without S3. For Batch runs, grant the job role `s3:GetObject` and `s3:PutObject`. |
| MkDocs shows outdated content | Run `make build` again or delete the `site/site_build/` folder before serving. |
| API shows old data | Call `POST /refresh` on the FastAPI server or rerun `make build`. |

Still stuck? Open an issue or ping `@sans_serif_sentiments` on GitHub.

---

## 8. Contributing and Licensing

- Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting changes.
- Run `make validate && make build && make check` before every pull request.
- Source code is MIT licensed. Glossary content is CC BY-SA 4.0. See [LICENSE](LICENSE) and [CONTENT_LICENSE](CONTENT_LICENSE).

Thanks for helping build an AI glossary that real humans can understand.
