# Simulated Data for FCDS-Scale Record Linkage

A Data Resource Profile for [IJPDS](https://ijpds.org/) describing a Florida-scale simulated
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

> **Note:** If your shell has another project's environment activated (its name
> appears in your prompt, e.g. `(some_other_project)`), `uv sync` may warn that
> `VIRTUAL_ENV` does not match the project environment. This is safe to ignore —
> uv uses this project's `.venv` anyway. To silence it, run `deactivate` (for a
> venv) or `conda deactivate` (for a conda environment) first. Either way,
> prefer `uv run ...` or the `make` targets over bare `python`/`quarto`, which
> would resolve to whatever environment is activated.

## Editing, compiling, and viewing the paper

1. **Edit** the prose and analysis code in `paper.qmd`. Computed numbers in the
   text are inline `` `{python} expr` `` expressions backed by variables from
   earlier code chunks — never hard-code a computed value in prose.
2. **Preview while writing** (live-reloading HTML in your browser):

   ```sh
   uv run quarto preview paper.qmd
   ```

   Open the **"Browse at http://localhost:PORT/paper.html"** link that quarto
   prints — the "Listening on http://127.0.0.1:PORT/" line is just the server's
   bind address (its root URL serves nothing for a single-document preview).
   When working over VS Code Remote-SSH, VS Code forwards the port
   automatically, so the "Browse at" link opens straight from the terminal.

3. **Compile** the submission file:

   ```sh
   make paper                # renders docx (and html) from frozen results
   ```

### Working in VS Code (Remote-SSH)

`Ctrl+Shift+K` (Quarto: Preview) works once all of the following hold:

- You're **connected to a cluster worker node**, not the submit node.
- You've **opened this folder as the workspace root** (not a parent directory) —
  otherwise the settings in `.vscode/settings.json` don't apply.
- The **Quarto extension is installed on the SSH remote**, not just locally: in
  the Extensions view, find Quarto and click *"Install in SSH: \<host\>"*. (If
  it's only installed locally it runs on your laptop, can't see the cluster's
  quarto, and offers to install Quarto on Windows — decline that.)
- `.vscode/settings.json` points the extension at the venv's quarto binary via
  `quarto.path`, and the Python interpreter is the project venv
  (`.venv/bin/python`, via *Python: Select Interpreter*). Both are already set
  in this repo's `.vscode/settings.json`.

## Other commands

```sh
make test    # uv run pytest
make lint    # uv run ruff check .
```

## Project layout

- `paper.qmd` — the Data Resource Profile (fast to render: it executes only the small
  bundled pseudopeople sample population and reads precomputed summaries)
- `src/simulated_data_for_fcds_scale_rl/` — importable, tested Python logic
- `_quarto.yml` — render configuration; `_freeze/` caches executed results so
  the project renders even without the Python environment or data
- `references.bib`, `ijpds.csl` — bibliography and IJPDS (Vancouver) citation style
- `reference-doc.docx` — Word styling for the submission

Heavy data generation (the full ~22M-person Florida population) belongs in a
separate pipeline tier run manually on the cluster — see `CLAUDE.md` for the
architecture and conventions.
