CONFIG = config.json
PYTHON = uv run python3

# The assigned A-Maze-ing package is installed as-is from its wheel
# (unzipped from mazegenerator-*.zip when no .whl is present).
install:
	uv sync
	@ls mazegenerator-*.whl >/dev/null 2>&1 || unzip -oq mazegenerator-*.zip
	uv pip install mazegenerator-*.whl

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
	uv run flake8 .
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict

test:
	uv run pytest

check: lint test

build:
	./packaging/build.sh

.PHONY: install run debug clean lint lint-strict test check build