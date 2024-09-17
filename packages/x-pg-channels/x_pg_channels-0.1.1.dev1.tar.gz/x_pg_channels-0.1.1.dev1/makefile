PACKAGE := x_pg_channels
VENV := venv
VPYTHON := . $(VENV)/bin/activate && python

.PHONY: all install test clean build

all:
	make install test clean build

install: $(VENV)
	$(VPYTHON) -m pip install -e .[dev]; pre-commit install

test:
	$(VPYTHON) -m pytest

build:
	$(VPYTHON) -m build; make twine

clean: .pytest_cache dist $(PACKAGE).egg-info
	rm -rf .pytest_cache dist/* $(PACKAGE).egg-info $(PACKAGE)/__pycache__ dist/__pycache__

twine: dist
	$(VPYTHON) -m twine upload dist/*