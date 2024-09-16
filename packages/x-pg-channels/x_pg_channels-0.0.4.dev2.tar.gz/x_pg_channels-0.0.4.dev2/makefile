PACKAGE := x_pg_channels
VENV := venv
VPYTHON := . $(VENV)/bin/activate && python

.PHONY: all install clean build

all:
	install

.PHONY: install
install: $(VENV)
	$(VPYTHON) -m pip install -e .[dev]; pre-commit install

clean: .pytest_cache $(PACKAGE).egg-info
	rm -rf .pytest_cache dist/* $(PACKAGE).egg-info

build:
	$(VPYTHON) -m build; twine

twine: dist
	twine upload dist/*