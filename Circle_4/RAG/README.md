*This project has been created as part of the 42 curriculum by ialmani.*

# RAG against the machine

## Description

A Retrieval-Augmented Generation (RAG) system that answers questions about
the [vLLM](https://github.com/vllm-project/vllm) 0.10.1 codebase. It:

1. **indexes** the repository (Python code and Markdown/text docs) into
   chunks of at most 2000 characters and a BM25 index,
2. **retrieves** the top-k most relevant chunks for a question, as exact
   source locations (`file_path` + character range),
3. **augments** a prompt with those chunks within a token budget,
4. **generates** a grounded answer with the local model `Qwen/Qwen3-0.6B`.

Retrieval quality is measured with recall@k against reference datasets.

## Instructions

Requirements: Python >= 3.10 and [uv](https://docs.astral.sh/uv/).
PyTorch is installed from the CPU wheel index (no CUDA download).

```bash
make install            # uv sync
```

Expected data layout (not committed):

```
data/raw/vllm-0.10.1/                 # unzip vllm-0.10.1.zip in data/raw
data/datasets/UnansweredQuestions/    # from datasets_public.zip
data/datasets/AnsweredQuestions/
```

Commands (all paths are CLI arguments, nothing is hard-coded):

```bash
uv run python -m src index --max_chunk_size 2000
uv run python -m src search "How do I load a LoRA adapter?" --k 5
uv run python -m src search_dataset \
    --dataset_path data/datasets/UnansweredQuestions/dataset_docs_public.json \
    --k 10 --save_directory data/output/search_results/UnansweredQuestions
uv run python -m src answer "What does --max-num-seqs control?" --k 5
uv run python -m src answer_dataset \
    --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
    --save_directory data/output/search_results_and_answer/UnansweredQuestions
uv run python -m src evaluate \
    --student_search_results_path data/output/search_results/UnansweredQuestions/dataset_docs_public.json \
    --dataset_path data/datasets/AnsweredQuestions/dataset_docs_public.json
```

Global option: `--index_dir` (default `data/processed`), placed before the
command. Makefile rules: `install`, `run` (index + search + answers,
`SCOPE=` / `DATASET=` select the dataset), `debug` (pdb), `clean`, `lint`,
`lint-strict`, `test`, `index`, `evaluate`.

## System architecture

```
data/raw ──> indexer ──> chunking (python | text) ──> tokenizer ──> BM25
                                                                    │
                                     data/processed/ (chunks.json, bm25.npz)
                                                                    │
question ──> tokenizer ──> retriever (BM25 top-k) ──> MinimalSource list
                                                                    │
                       generator: context (<= 3000 tokens) + prompt ──> Qwen3-0.6B ──> answer
```

| Module | Role |
| --- | --- |
| `src/__main__.py` | Entry point, Fire, global error handling (no traceback) |
| `src/cli.py` | `RagCLI`: one method per command, argument validation |
| `src/models.py` | Pydantic models of the subject + `Chunk` |
| `src/chunking.py` | Python (AST) and Markdown/text chunkers |
| `src/tokenizer.py` | Shared tokenization for chunks and queries |
| `src/bm25.py` | Numpy BM25 with precomputed weights |
| `src/indexer.py` | Corpus walk, chunking, index persistence |
| `src/retriever.py` | Index loading and top-k search |
| `src/generator.py` | Prompt building and Qwen3 generation |
| `src/evaluate.py` | Our recall@k (IoU >= 0.05), for iteration |

## Chunking strategy

Both chunkers work on character offsets of the file read with
`newline=""` (no `\r\n` translation, so offsets match the reference).
They share a recursive splitter: a span longer than `max_chunk_size` is cut
at the best available "break level", each piece is split again with the
next levels if needed, and small neighbouring pieces are merged back while
they fit. No chunk can exceed `max_chunk_size`.

| Level | Python (`ast`) | Markdown / text |
| --- | --- | --- |
| 0 | top-level `def` / `class` (with decorators) | `#` / `##` headings |
| 1 | other top-level statements, methods, nested defs | `###`+ headings |
| 2 | blank lines | blank lines |
| 3 | newlines | newlines |

Files that do not parse fall back to a `def|class|@` regex. Headings inside
code fences are ignored. Indexed extensions: `.py`, `.md`, `.txt`, `.rst`.

Each chunk is indexed with extra words: its path (`docs/features/lora.md`
-> "docs features lora") and a title (Markdown heading breadcrumb or
`Class.method` names). The returned span is unchanged.

## Retrieval method

Okapi BM25 (`k1 = 1.2`, `b = 0.75`). All query-independent weights
`idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * dl / avgdl))` are computed at
indexing time and stored per term (CSC-like arrays `term_ptr`, `doc_ids`,
`weights`). A query sums the slices of its terms in a numpy score vector and
`argpartition` extracts the top-k.

Tokenization: words `[A-Za-z0-9_]+`; compound identifiers are kept whole
**and** split on `_` / camelCase (`max_num_seqs` -> `max_num_seqs`, `max`,
`num`, `seqs`), so a question can match a verbatim identifier or a
paraphrase; lowercase, stopwords removed, light suffix stemming.

## Performance analysis

Public datasets, `k = 10`, scored by the moulinette (our `evaluate`
command gives identical numbers):

| Dataset | Recall@1 | Recall@3 | Recall@5 | Recall@10 | Required R@5 |
| --- | --- | --- | --- | --- | --- |
| docs (100 q.) | 0.70 | 0.83 | **0.90** | 0.91 | 0.80 |
| code (99 q.) | 0.57 | 0.81 | **0.87** | 0.92 | 0.50 |

Effect of `--max_chunk_size` on recall@5:

| max_chunk_size | chunks | docs R@5 | code R@5 |
| --- | --- | --- | --- |
| 500 | 53,147 | 0.85 | 0.87 |
| 1000 | 27,023 | 0.88 | 0.82 |
| 1500 | 18,175 | 0.89 | 0.87 |
| 2000 | 13,859 | 0.90 | 0.87 |

Ablations (chunk size 2000, recall@5 docs / code): final 0.90 / 0.87;
without path + title words 0.86 / 0.74; without stemming 0.86 / 0.89;
without stopwords 0.83 / 0.84.

Timings (12-core CPU laptop): indexing 1968 files in ~13 s (limit 5 min);
searching 200 questions in < 0.1 s plus ~1 s of index loading (limit 90 s);
answer generation ~13 s per question with Qwen3-0.6B on CPU (~22 min for 100).

## Design decisions

- **BM25 rather than TF-IDF**: saturates term frequency and normalizes by
  chunk length; the standard of search engines.
- **Own numpy BM25**: no black box, fast, easy to persist (`.npz`).
- **AST for Python**: cuts exactly on function/class boundaries, so a chunk
  is a meaningful unit of code.
- **Chunks store offsets, not text**: the index stays small and the text is
  read back from the corpus when generating.
- **Lazy import of torch/transformers**: `index` and `search` start fast.
- **Greedy decoding, `enable_thinking=False`**: deterministic, short answers;
  Qwen3's reasoning block is too slow on CPU and not needed.
- **Strict prompt**: answer only from the context, quote exact names, say
  when the answer is missing, to limit hallucinations.

## Challenges faced

- *Questions and code use different words*: solved by indexing identifiers
  both whole and split, and by adding path and title words to each chunk
  (+13 points of code recall@5).
- *Exact offsets*: a few corpus files use `\r\n`; reading with `newline=""`
  keeps offsets identical to the raw file.
- *Never crash*: Fire may pass ints or tuples as queries; every command
  validates its inputs and errors are turned into one-line messages.
- *Markdown headings inside code blocks* (`# comment` in bash) were mistaken
  for headings; fences are now tracked.

## Example usage

```
$ uv run python -m src search "What HTTP endpoint is used to dynamically load a LoRA adapter?" --k 3
 1. [ 41.02] data/raw/vllm-0.10.1/docs/features/lora.md [4695:6098]
 ...
$ uv run python -m src answer "What HTTP endpoint is used to dynamically load a LoRA adapter in vLLM?" --k 5
Answer:
The HTTP endpoint used to dynamically load a LoRA adapter is `/v1/load_lora_adapter`.
$ uv run python -m src search "" --k 3
Error: the query is empty
```

## Resources

- S. Robertson, H. Zaragoza, *The Probabilistic Relevance Framework: BM25
  and Beyond* (2009).
- P. Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive
  NLP Tasks* (2020), https://arxiv.org/abs/2005.11401
- Manning, Raghavan, Schütze, *Introduction to Information Retrieval*,
  ch. 6 and 11, https://nlp.stanford.edu/IR-book/
- Python `ast` module: https://docs.python.org/3/library/ast.html
- Qwen3 model card: https://huggingface.co/Qwen/Qwen3-0.6B
- Hugging Face transformers generation docs:
  https://huggingface.co/docs/transformers/main_classes/text_generation
- Python Fire: https://github.com/google/python-fire

**AI usage**: an AI assistant (Claude) was used to scaffold the project
structure, draft the chunking/BM25/CLI code and this README, and to run the
recall experiments. Every module was then read, tested (unit tests, edge
cases, moulinette) and explained in a personal study guide so that each
design choice can be justified.
