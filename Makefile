PYTHON ?= python3
VENV ?= .venv
VENV_BIN := $(VENV)/bin
VENV_PYTHON := $(VENV_BIN)/python

ifneq (,$(wildcard $(VENV_PYTHON)))
PYTHON := $(VENV_PYTHON)
endif

DATA_DIR := data/terms

.PHONY: venv validate build serve-api serve-docs render-docs

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
