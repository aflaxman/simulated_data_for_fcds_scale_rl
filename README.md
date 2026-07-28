# Simulated Data for FCDS-Scale Record Linkage

A Data Note for [IJPDS](https://ijpds.org/) describing a Florida-scale simulated
dataset, generated with [pseudopeople](https://pseudopeople.readthedocs.io/), for
testing record-linkage software for cancer data systems such as the Florida Cancer
Data System (FCDS).

The paper itself is `paper.qmd`, a [Quarto](https://quarto.org/) document with the
analysis written in Python. Rendering produces two artifacts:

- `paper.docx` — the IJPDS submission file (styled by `reference-doc.docx`)
- `paper.html` — a self-contained copy for sharing

## Setup

Requires Python 3.10–3.11 (a pseudopeople constraint) and
[uv](https://docs.astral.sh/uv/). Quarto is installed as a dev dependency, so
one command sets up everything:

```sh
uv sync
```

## Editing, compiling, and viewing the paper

1. **Edit** the prose and analysis code in `paper.qmd`. Computed numbers in the
   text are inline `` `{python} expr` `` expressions backed by variables from
   earlier code chunks — never hard-code a computed value in prose.
2. **Preview while writing** (live-reloading HTML in your browser):

   ```sh
   uv run quarto preview paper.qmd
   ```

3. **Compile** the submission file:

   ```sh
   make paper                # renders docx (and html) from frozen results
   ```

## Other commands

```sh
make test    # uv run pytest
make lint    # uv run ruff check .
```

## Project layout

- `paper.qmd` — the Data Note (fast to render: it executes only the small
  bundled pseudopeople sample population and reads precomputed summaries)
- `src/simulated_data_for_fcds_scale_rl/` — importable, tested Python logic
- `_quarto.yml` — render configuration; `_freeze/` caches executed results so
  the project renders even without the Python environment or data
- `references.bib`, `ijpds.csl` — bibliography and IJPDS (Vancouver) citation style
- `reference-doc.docx` — Word styling for the submission

Heavy data generation (the full ~22M-person Florida population) belongs in a
separate pipeline tier run manually on the cluster — see `CLAUDE.md` for the
architecture and conventions.
