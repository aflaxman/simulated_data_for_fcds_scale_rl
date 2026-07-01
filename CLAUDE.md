# CLAUDE.md

Data Note for IJPDS: a Florida-scale simulated dataset (generated with pseudopeople)
for testing record-linkage software for cancer data systems (e.g. FCDS).
Quarto project, analysis in Python.

## Environment
- Python **3.10–3.11 only** (pseudopeople constraint). Managed with uv:
  `uv sync` to set up, `uv run <cmd>` to execute anything.
- Core deps: pseudopeople, duckdb, splink>=4, pandas, pyarrow.
- Quarto must be on PATH (cluster module or local install).

## Commands
- `uv run quarto preview paper.qmd` — live HTML preview while writing.
- `uv run quarto render paper.qmd --to docx` — build the IJPDS submission file.
- `uv run pytest` — tests (see tests/).

## Architecture — two tiers, keep them separate
1. **Paper tier (cheap, runs on every render):** `paper.qmd` executes only the
   small bundled pseudopeople *sample* population (~10k simulants) and reads
   precomputed summaries from `results/`. Keep this fast.
2. **Pipeline tier (heavy, manual, for srun/slogin):** `pipeline/` checks the US
   population, filters to Florida (~22M), adds noise, writes Parquet to scratch,
   and writes *small* summaries (counts, overlaps, error rates, QA) into
   `results/`. Never inline this in the paper; never run it on a login/dev node.

Layout: `src/simulated_data_for_fcds_scale_rl/` = importable, tested logic shared by paper + pipeline ·
`pipeline/` = heavy scripts · `results/` = small committed summaries the paper reads ·
`reference/` = small committed reference data · `paper.qmd` = the Data Note.

## Conventions
- **Never hard-code a computed number in prose.** Every computed value is an inline
  `{python} expr` backed by a variable loaded in an earlier chunk (load chunks must
  come before the inline uses). Facts from citations are plain prose + citation.
- **Freeze:** a single-doc render *always* executes; `freeze: auto` only affects
  full-project renders. Freeze hashes `paper.qmd` only — it does NOT watch `src/`,
  `config.yaml`, or data. After editing `src/`, run `quarto render paper.qmd` once
  to refresh `_freeze/`. Commit `_freeze/` and `results/` together (they let a
  machine without the Python env or the data still render the project).
- To change a headline result: edit the pipeline or `config.yaml`, re-run the sbatch
  job (which rewrites `results/`), then re-render. Do not edit the number in the paper.
- Paths and the RNG seed live in `config.yaml` (single source of truth); always set
  and record the seed so error rates are reproducible.

## Guardrails
- **File safety:** big data and derivatives live under the user's own scratch space
  (writable). Do NOT delete, move, overwrite, or rename anything on shared, read-only
  locations (e.g. paths under /ihme or /mnt/share other than the user's own home). If
  a destructive op there seems needed, copy to a working dir first and ask.

## Writing target (IJPDS)
IMRAD; structured abstract ≤300 words (intro/objectives/methods/results/conclusions);
3–5 highlight bullets; figures/tables inline; Vancouver references with DOIs (via
`ijpds.csl`). The submission is the rendered `.docx` (styled by `reference-doc.docx`);
the dataset goes to a separate DOI deposit, not as a supplement.