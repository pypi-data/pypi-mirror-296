SHELL := /bin/bash
PACKAGE=x_pg_channels
VENV := venv
PYTHON := . $(VENV)/bin/activate && python

.PHONY: install
install: pip install .

.PHONY: pip
pip: $(VENV)
	$(PYTHON) -m pip install -e .[dev]


.PHONY: pre-commit
pre-commit:
	pre-commit install

.PHONY: pytest
pytest:
	$(PYTHON) -m pytest --cov=./${PACKAGE} --cov-report=term-missing tests

.PHONY: pytest_loud
pytest_loud:
	$(PYTHON) -m pytest -s --cov=./${PACKAGE} --cov-report=term-missing tests

.PHONY: build
build: $(PACKAGE_CHECK)
	$(PYTHON) -m build

.PHONY: twine
twine: dist
	twine upload dist/*