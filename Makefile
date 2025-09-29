PYTHON ?= python3
VENV ?= .venv
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python

ifneq (,$(wildcard $(VENV_PYTHON)))
PYTHON := $(VENV_PYTHON)
endif

DATA_DIR := data/terms

.PHONY: venv validate build serve-api serve-docs render-docs preview test check new-term gh-pages github-push

venv:
	python3 -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -r requirements.txt
	@echo "Activate the virtual environment with 'source $(VENV_BIN)/activate'"

validate:
	$(PYTHON) scripts/validate.py --data-dir $(DATA_DIR)

build:
	$(PYTHON) scripts/build_index.py --data-dir $(DATA_DIR)
	$(PYTHON) scripts/render_docs.py --data-dir $(DATA_DIR) --docs-dir site/docs/terms

render-docs:
	$(PYTHON) scripts/render_docs.py --data-dir $(DATA_DIR) --docs-dir site/docs/terms

serve-api:
	uvicorn api.main:app --reload

serve-docs:
	cd site && mkdocs serve

preview:
	mkdocs serve -f site/mkdocs.yml

test:
	$(PYTHON) -m unittest discover

check:
	$(PYTHON) scripts/validate.py --data-dir $(DATA_DIR)
	$(PYTHON) -m unittest discover
	mkdocs build --strict -f site/mkdocs.yml

new-term:
	@if [ -z "$(NAME)" ]; then \
		echo "Usage: make new-term NAME=\"your term\""; \
		exit 1; \
	fi
	$(PYTHON) scripts/new_term.py --term "$(NAME)"

gh-pages:
	mkdocs build --strict -f site/mkdocs.yml
	mkdocs gh-deploy -f site/mkdocs.yml --force

github-push:
	@if [ -z "$(MESSAGE)" ]; then \
		echo "Usage: make github-push MESSAGE=\"describe your changes\""; \
		exit 1; \
	fi
	@if [ -z "$(filter main,$(shell git branch --show-current))" ]; then \
		echo "⚠️  Please switch to the main branch before pushing."; \
		exit 1; \
	fi
	@echo "▶︎ Running validation before push..."
	$(MAKE) check
	git status
	@if git status --short | grep -q '^?? models/'; then \
		echo "⚠️  The 'models/' directory is untracked. It is ignored by .gitignore and will not be pushed."; \
	fi
	git add README.md Makefile scripts/enrich_related_terms.py site/docs site/mkdocs.yml data/terms .gitignore
	git commit -m "$(MESSAGE)"
	git push origin main
