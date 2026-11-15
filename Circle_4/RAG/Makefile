PYTHON      = uv run python
MODULE      = src
SCOPE      ?= UnansweredQuestions
DATASET    ?= dataset_docs_public.json

.PHONY: install run debug clean lint lint-strict test index search answer evaluate

install:
	uv sync

## run: full pipeline on one dataset (index -> search -> answers)
run: index
	$(PYTHON) -m $(MODULE) search_dataset \
		--dataset_path data/datasets/$(SCOPE)/$(DATASET) --k 10 \
		--save_directory data/output/search_results/$(SCOPE)
	$(PYTHON) -m $(MODULE) answer_dataset \
		--student_search_results_path data/output/search_results/$(SCOPE)/$(DATASET) \
		--save_directory data/output/search_results_and_answer/$(SCOPE)

index:
	$(PYTHON) -m $(MODULE) index --max_chunk_size 2000

debug:
	$(PYTHON) -m pdb -m $(MODULE) search "How do I load a LoRA adapter?" --k 5

evaluate:
	$(PYTHON) -m $(MODULE) evaluate \
		--student_search_results_path data/output/search_results/$(SCOPE)/$(DATASET) \
		--dataset_path data/datasets/AnsweredQuestions/$(DATASET)

test:
	uv run pytest -q tests

clean:
	find . -type d \( -name __pycache__ -o -name .mypy_cache -o -name .pytest_cache \) \
		-not -path "./.venv/*" -prune -exec rm -rf {} +

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict
