PYTHON ?= python3
DATA_DIR := data/terms

.PHONY: validate build serve-api serve-docs

validate:
	$(PYTHON) scripts/validate.py --data-dir $(DATA_DIR)

build:
	$(PYTHON) scripts/build_index.py --data-dir $(DATA_DIR)

serve-api:
	uvicorn api.main:app --reload

serve-docs:
	cd site && mkdocs serve
