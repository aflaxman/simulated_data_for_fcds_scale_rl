# CLAUDE.md

Data Resource Profile for IJPDS: a Florida-scale simulated dataset (generated with pseudopeople)
for testing record-linkage software for cancer data systems (e.g. FCDS).
Quarto project, analysis in Python.

## Environment
- Python **3.10–3.11 only** (pseudopeople constraint). Managed with uv:
  `uv sync` to set up, `uv run <cmd>` to execute anything.
- Core deps: pseudopeople, duckdb, splink>=4, pandas, pyarrow, pyyaml, matplotlib (figures).
- Quarto is **not** a system install or cluster module here: it is the `quarto-cli`
  package in the uv dev group, so `uv sync` puts it at `.venv/bin/quarto`. Always call
  it as `uv run quarto …` or via the `make` targets. Bare `quarto` is not on PATH, so
  `which quarto` outside `uv run` wrongly reports it missing.

## Commands
- `uv run quarto preview paper.qmd` — live HTML preview while writing. Open the
  "Browse at http://localhost:PORT/paper.html" link it prints, not the "Listening on"
  root URL; VS Code Remote-SSH forwards the port from a cluster worker node.
- `uv run quarto render paper.qmd` — single-document render (always executes; writes
  `paper.html` and refreshes `_freeze/`). Add `--to docx` for the submission file only.
- `make paper` — project render to docx (`uv run quarto render --to docx`), which is
  the one path where `freeze: auto` applies.
- `uv run pytest` — tests (see tests/). `make test` / `make lint` wrap pytest and ruff.
- Run renders and previews on a cluster worker node, not the submit node (see README,
  "Working in VS Code"); the paper tier is cheap enough for a dev node.
- Rebuild (cluster only, via `sbatch`, never a login node): `pipeline/build_cohorts.py` (the version comes from `--version`, whose default must match `config.yaml`; `--force` rebuilds in place)
  (~10 min, 8 CPUs, 120G), then `linkage_baseline.py`, `example_pair.py`, `pair_agreement.py`
  (seconds each), then `make checks`, `make figures` and a render; commit `results/`, `_freeze/`,
  the notebook and the renders together. README gives the exact commands.

## Architecture — two tiers, keep them separate
1. **Paper tier (cheap, runs on every render):** `paper.qmd` executes only the
   small bundled pseudopeople *sample* population (~10k simulants) and reads
   precomputed summaries from `results/`. Keep this fast.
2. **Pipeline tier (heavy, manual, for srun/slogin):** `pipeline/` checks the US
   population, filters to Florida across the simulated 2020, 2030 and 2040 censuses (~50M person-records; the
   registry is drawn from each simulant's last appearance, the finder files from 2040 residents), adds noise, writes Parquet to scratch,
   and writes *small* summaries (counts, overlaps, error rates, QA) into
   `results/`. Never inline this in the paper; never run it on a login/dev node.

Layout: `src/simulated_data_for_fcds_scale_rl/` = importable, tested logic shared by paper + pipeline ·
`pipeline/` = heavy scripts · `results/` = small committed summaries the paper reads ·
`notebooks/` = the receiver's acceptance checks (generated and executed by `notebooks/make_acceptance_checks.py`) ·
`figures/` = figure renders, gitignored ·
`reference/` = small committed reference data, including `data_dictionary.csv`, which the build ships inside the zip · `paper.qmd` = the Data Resource Profile.

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

## Writing target (IJPDS Data Resource Profile)
Body: Background → Methods → Results → Discussion → Data Access → Conclusions (no
Introduction section). Structured abstract ≤300 words with four headings
(Introduction/Methods/Results/Conclusion, dataset-first content); Key Features ≤6
bullets on the journal's roster; figures/tables inline; Vancouver references with
DOIs (via `ijpds.csl`). Lingo per the FCDS Procedure Guide: *finder file* = the
researcher-submitted cohort (the released 500k/100k files); the 5M file is the
*simulated registry*, never a finder file. The registry alone carries `diagnosis_date`. "Simulant" is
pseudopeople's word for a simulated person: introduce it once, in quotes, where `simulant_id` is first
explained, then write "people" or "simulated people" in prose, keeping "simulant" for the identifier
and for reminders that no real person is involved. Sex uses the data's own categories, male and female
("females", "male records"), never men/women/boys/girls, in prose, tables, figures and the notebook
(author's call, 2026-10-04). The submission is the rendered `.docx`
(styled by `reference-doc.docx`); the dataset goes to a separate DOI deposit, not
as a supplement.

## Voice (all prose: paper, abstract, README, drafts for the author)
The full calibrated style prompt is `STYLE.md`; read it before drafting or revising more
than a sentence. It is measured on the author's 2015 monograph, so it gives numbers to
hit, not adjectives. The essentials:
- **First person owns every choice.** Since 2026-09-24 the paper has two authors, so its
  prose says "we used," "we prefer," "which we call" for the authors' choices (the abstract
  already does); "I" is for single-author pieces such as README notes and drafts addressed
  to the author. Never "it was decided" or "the literature suggests."
- **Pragmatist, not purist.** State the principled objection fairly and in full, then say
  what was actually done and why the compromise is acceptable ("a method of
  convenience," "something is better than nothing," "just complicated enough").
- **Drawback beside the claim, in the same sentence.** "X has the best balance of A and
  B, but cannot cope with C." Say "crude" or "not very good" plainly. Never sell: no
  "novel," "robust," "powerful," "comprehensive," "state-of-the-art"; no "importantly,"
  "crucially," "genuinely," "clearly."
- **Hedge with frequency, not confidence:** "often," "usually," "in practice." Not
  "perhaps," "arguably," "it could be argued." Uncertainty is a fact about the data.
- **Sentences are long but unpadded** (median ~23 words), built from subordinate clauses
  that each add a qualification, tradeoff, or pointer. No choppy "impact" sentences.
  Commas and parentheses carry asides; semicolons rare; dashes almost never. About one
  sentence in ten opens with "This ..." pointing at the previous idea. Argument lives in
  paragraphs; bullets only enumerate models, steps, or properties.
- **Order of exposition:** plain-language framing before any notation; announce the plan,
  then follow it; a real motivating example with actual numbers and units before general
  theory; simplest model first, and show the failure (a figure, a number) before the
  fix; equation, every symbol defined in words at once, then "the intuition is simple:".
  Signpost with exact forward and backward section references.
- **Terminology:** coin names and say so ("which I call ..."); jargon in quotes on first
  use only; flag misleading names. Impersonal constructions for the machinery ("can be
  written as"), first person for the choices.
- **At most** one dry line per section and one anecdote per piece, and only if it does
  explanatory work.
- **Real numbers only,** via the inline `{python}` convention above. If a value is not
  known, say so rather than invent one.
- **DRP register dial.** The journal structure above wins over the monograph scaffolding:
  no "Summary and future work" header; Conclusions carries the two-sentence verdict with
  its tradeoff, then open directions each given an honest weight ("promising," "worthy of
  additional attention"). Limitations are collected in Discussion (§4.2) because the
  journal expects it, but each drawback is still named beside the claim where it first
  arises, not deferred to that section. The structured abstract and Key Features follow
  the journal's format, not the voice.
