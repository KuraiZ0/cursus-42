CONFIG = config.json
PYTHON = uv run python3

install:
	uv sync

run:
	$(PYTHON) pac-man.py $(CONFIG)

debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf build
	rm -rf dist

lint:
	uv run flake8 src tests pac-man.py
	uv run mypy src tests pac-man.py \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 src tests pac-man.py
	uv run mypy src tests pac-man.py --strict

test:
	uv run pytest

check: lint test

build:
	./packaging/build.sh

.PHONY: install run debug clean lint lint-strict test check build