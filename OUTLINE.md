# Outline: Data Note: A Florida-scale simulated dataset for developing and benchmarking record-linkage software for cancer data systems

> **Status, 2026-07-28.** This is a planning document, not a draft. It was assembled from the working notebooks in
> `/ihme/homes/abie/notebook/2026/` (chiefly `2026_02_11b_duckdb_psp_reproducible_randomness.ipynb`), from literature
> research, and from measurements taken directly against the shipped v0.2 files. Claims marked **verified** were
> measured or checked on this date; everything else is marked *TO WRITE*, *to confirm*, or *unverified* and should be
> treated as a claim the paper cannot yet make. The deterministic-linkage baselines are real and reproducible today via
> `uv run python pipeline/linkage_baseline.py`; nothing else in `results/` exists yet.

**Editor's note.** The single claim this paper makes is: *a simulated, openly downloadable, ground-truthed linkage benchmark at the scale and cancer demography of a real US state registry is now possible, and here is the one that exists, together with what broke while building it.* It is for two audiences at once — cancer-registry staff and vendors who need somewhere to test matching software that is not their own confidential file, and the linkage-methods community that has metrics but no large shared corpus. The paper is an IJPDS **Data Note**, so the genre reward is not the dataset description but the *problems encountered in the pipeline*: reproducible randomness under a parallel SQL engine, the oversample-then-downsample pattern and the overlap overshoot it caused, and the simulator affordance gaps that had to be filled by hand. Before this can be submitted, five things must happen, in this order: (1) **commit `config.yaml`, `pipeline/`, `results/` and `reference/` — all four are currently untracked in git**, so every headline number in the paper rests on files that could vanish and that a reviewer of the repo cannot see; (2) port the build from the working notebook into `pipeline/` scripts and confirm they reproduce the four published md5 checksums — until that re-run happens the paper's central reproducibility claim is untested, not merely unwritten; (3) write the six small `results/` summaries the text needs (only `linkage_baseline.json` exists today); (4) resolve the two provenance holes that currently have no citable source — the FCDS incidence table used for QA, and the "FCDS 2024 monograph" credited in `config.yaml` with the choice of noise rates; (5) mint the Zenodo DOI, because IJPDS requires a dataset DOI plus a private reviewer URL at submission and the Data Availability Statement cannot be finished without them. On length: IJPDS Data Notes are 2,000–3,000 words *including title page and references*, which four of the five section drafts blow through several times over. Note that overage is cheap (£50 covers up to 5,000 words over), so the binding constraint is editorial patience and genre fit rather than cost — which makes "Data Note vs Data Resource Profile (3,000–8,000 words)" a real choice rather than a forced one. This outline is built to the Data Note limit; where it hurts, it says so.

---

## Title, authors, keywords

**Recommended:** *Data Note: A Florida-scale simulated dataset for developing and benchmarking record-linkage software for cancer data systems*

IJPDS author guidelines require the title to begin `Data Note: `. This version keeps the working title's content while fixing a modifier-attachment bug in it: "research and development of Florida-scale record linkage software" reads as though the *software* is Florida-scale. It is the data that is. "Developing and benchmarking" also names both uses, which matters because the benchmark half is what the deterministic baseline and the ground-truth key are for.

Runners-up:

| Option | Why it might win | Why it does not |
|---|---|---|
| *Data Note: Building a state-scale simulated linkage benchmark with pseudopeople and DuckDB* | Foregrounds the pipeline lessons, which is precisely the register IJPDS Data Notes reward | Buries cancer and the registry audience; reads as a methods paper, and the cancer-demography weighting is the paper's most distinctive design choice |
| *Data Note: Simulated finder files and a simulated cancer registry at Florida scale, with ground truth, for open linkage benchmarking* | Most concrete about what actually ships; "finder file" is the term FCDS submitters use | Longest of the four; "ground truth" is jargon to registry staff, and "cancer data systems" (the generalisable phrase) disappears |
| *Data Note: Simulated data for research and development of Florida-scale record linkage software for cancer data systems* | The author's working title, minimally adapted — safest for continuity with repo and deposit naming | Carries the modifier bug above |

**Author.** Abraham D. Flaxman, Institute for Health Metrics and Evaluation, University of Washington, Seattle, WA, USA. ORCID must be filled in — `paper.qmd` currently reads `Your Name` / `0000-0000-0000-0000`.

**Keywords (7):** record linkage; entity resolution; simulated data; cancer registry; benchmark dataset; reproducibility; pseudopeople.

---

## Key Features

IJPDS calls this section **Key Features**, not "Highlights" (`paper.qmd` currently says "Highlights"), and allows a maximum of six bullets.

- We release a simulated cancer-registry linkage benchmark at the scale of a real state registry: a registry stand-in of `{python} registry_rows` records and two researcher finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records, drawn from `{python} fl_simulants` simulated Florida residents. To our knowledge it is the largest openly downloadable *fully simulated* multi-file person corpus with cross-file ground-truth identity; larger open person benchmarks exist but are built from real voter records with few attributes [@saeedi2018famer].
- The registry's age and sex structure follows Global Burden of Disease neoplasm prevalence for Florida, so linkage methods meet the demography that cancer linkage actually presents — mass at the oldest ages — rather than general-population demography.
- Every record carries `simulant_id`, a ground-truth identity key, so missed-match and false-match rates of any method can be computed exactly rather than estimated [@harron2017guide; @lam2024synthetic].
- Weighted sampling replaces the SQL engine's thread-dependent random number generator with keyed cryptographic hashes, making each released file a pure function of one recorded seed; published checksums let any user verify the file they hold is the file the paper describes.
- We report deterministic exact-match baselines as a floor for probabilistic tools to beat [@linacre2022splink], and we report honestly where the build missed its own targets — realised overlaps overshot by roughly a third.

---

## Structured abstract (draft, 287 words)

IJPDS Data Note abstracts use **four** headings — Introduction / Methods / Results / Conclusion — not the five-heading Introduction/Objectives/Methods/Results/Conclusions form used for Research Articles and currently stubbed in `paper.qmd`. The Data Note "Results" heading is defined by the journal as *the specific data issues, problems and challenges encountered*, which this draft leans into deliberately. Each `{python}` placeholder is counted as one word.

> **Introduction**
> Software that links records to cancer registries must be built and tested on names, dates of birth, addresses and Social Security numbers (SSNs) — the fields that confidentiality rules prevent registries such as the Florida Cancer Data System (FCDS) from releasing. Openly available linkage test corpora are orders of magnitude smaller than a state registry and do not carry the age and sex structure of cancer.
>
> **Methods**
> From the pseudopeople simulated United States population we extracted the `{python} fl_simulants` simulated Florida residents in the 2020 decennial census. We sampled a registry stand-in of `{python} registry_rows` records, weighted by Global Burden of Disease neoplasm prevalence for Florida by age and sex, plus two finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records. Sampling used keyed hashes rather than the engine's random number generator, so each released file is reproducible from one recorded seed.
>
> **Results**
> Overlaps overshot their targets by about a third (`{python} overlap_500k_simulants` simulants against `{python} overlap_500k_target`) because downsampling retained all surviving overlap pairs. Registry SSN missingness reached `{python} registry_ssn_missing`, above target, because some simulants never held an SSN. Against the published ground-truth key, name plus date of birth linked `{python} r500_name_dob_recall` of true pairs at `{python} r500_name_dob_precision` precision; exact agreement on FCDS's current minimum field set linked `{python} r500_fcds_current_recall` with no false matches; name-and-birthdate-or-SSN linked `{python} r500_best_recall`.
>
> **Conclusion**
> A seed fixes a random stream but not its pairing to rows: row order had to be pinned before noise generation. Simulator affordance gaps are best filled by owning the pipeline around the simulator.

---

## 1. Introduction

*Combined target ≈ 430 words. IJPDS Data Notes require a separate **Background** heading between Introduction and Methods. §1.1 and §1.4 stay under "Introduction"; §1.2 and §1.3 become "Background" at draft time. They are numbered here so the collisions between the five drafts can be resolved in one place.*

### 1.1 Linkage is the registry's core competency, and its software cannot be developed in the open — ¶2 (~170 words)

- Open on the concrete ratio rather than an abstraction: Florida's reporting facilities send FCDS more than 310,000 case reports a year, which must resolve to roughly 145,000 newly diagnosed cases; the registry also links incidence to the state Bureau of Vital Statistics mortality file for passive follow-up [@fcds_welcome]. Cite with access date — the page carries no as-of date. Recognising that two differently spelled records describe one person *is* the product, so any improvement in linkage software is an improvement in the state's cancer statistics.
- The bind: the identifiers linkage software runs on are exactly what registry policy prevents from leaving the registry, and NAACCR states plainly that restrictive and varying state policies limit onward sharing of registry-derived data [@naaccr2023secondarysharing]. Separating linkage from analysis makes linkage a black box whose reliability researchers struggle to judge [@harron2017challenges]. Access is also slow and costly: one 224,000-member occupational cohort spent about 700 hours and $22,440 over five years obtaining approvals and matches from state registries [@buchanich2009methodological].
- The sharper problem, and the one this dataset answers: even a researcher who clears every hurdle gets no answer key. Real registry data carries no ground truth for which candidate pairs are the same person, so accuracy can only be estimated [@harron2017guide].

### 1.2 → Background: the transaction the dataset imitates — ¶2 (~140 words)

- Define "finder file" once, here, and never again: a researcher submits a cohort's identifiers, FCDS links them against the statewide incidence file, and returns matched records. **This is the only place the FCDS minimum-fields rule is stated** — Methods refers back to it. State both vintages, because they differ and no document establishes which supersedes: the 2007/2016 Procedure Guide requires first + last name AND SSN AND sex, *or* first + last name AND month and year of birth AND sex [@fdoh_fcds_procedure_guide_2007]; the current Data Linkage Record Layout requires name + sex + DOB + SSN, *or* name + sex + DOB + ZIP + street address, in a fixed-width ASCII record [@fcds_linkage_layout]. The released files satisfy either.
- One sentence of friction, not a table (see the display-item budget): identifiable FCDS data requires serial DOH IRB and Cancer Registry Review Committee approval with notarized confidentiality pledges and destruction on completion [@fdoh_fcds_procedure_guide_2007]; linkage runs onsite only and carries a sliding fee schedule [@fcds_data_release_procedures; @fcds_fees_2020]. **Attribute turnaround figures to their vintage** ("per FCDS's 2017 release procedures") — the digest marks current times as unverified.
- Close with the motivating fact, which is the strongest thing the paper has: FCDS's own 2023 Splink feasibility study ran on a 1,000,000 × 1,000,000 synthetic test file supplied privately by the present author, stated that "the datasets are not yet publicly available", and formally recommended making the test data public [@alexandersson2023splinkfcds]. The published follow-up comparison of fastLink, Match\*Pro and Splink for the Florida registry then ran at Rhode Island scale, roughly one twentieth of the population FCDS serves [@alexandersson2024comparing]. Say this Note *responds directly to* that recommendation — **not** "is literally the fulfillment of", which the reviewer correctly flagged as overstated since this is a different, larger corpus.

### 1.3 → Background: why existing corpora do not fit — ¶1 (~90 words)

*Compressed from a full page in the Introduction draft plus a duplicate subsection and table in the Discussion draft. The comparator landscape is stated **once, here**, in prose. `tbl-prior-benchmarks` and `tbl-benchmark-comparison` are both cut.*

- Linkage-specific generators model the right errors at the wrong scale: in the only controlled head-to-head benchmark, only three of five tools exceeded one million records, GeCo needed about 13 hours to corrupt one million and produced nothing at ten million [@hildebrandt2020dapo]; the shipped FEBRL corpora and the field's other standard tools are counted in thousands [@christen2008febrl; @tran2013geco; @talburt2009sog], and the public benchmark inventory confirms the pattern [@binette2022almost].
- Be scrupulous about the counter-examples, because a reviewer will be: the largest openly downloadable person benchmarks are real North Carolina voters — 10M records with as few as four attributes, excluding children, so age-structured opposite to a cancer registry [@saeedi2018famer]. The one prior ~20M-person microsimulation built to study linkage quality does not appear to have been released [@schnell2023microsim]. The only cancer-registry benchmark ships precomputed comparison vectors with no names or dates, so it cannot exercise blocking or string comparison [@schmidtmann2011krebsregister]. Synthea publishes a million rich synthetic patients but no identifier-error model and no cross-file ground truth [@walonoski2018synthea].
- **Do not mention "GeCo3"** — it is an unrelated DNA compressor. Do not name commercial vendors; the digest marks that as an unverified negative.

### 1.4 Contribution — ¶1 (~90 words)

- Numbered, and deliberately *not* re-quoting the counts that Results owns (the exact overlaps and file sizes move out of the Introduction entirely): (1) a prevalence-weighted registry stand-in and two finder files with exactly known overlap via a ground-truth key; (2) targeted error injection on top of pseudopeople's default noise at rates **plausible for this transaction** — not "chosen to reflect registry practice", which nothing verified supports; (3) a seeded, checksummed pipeline; (4) deterministic linkage baselines as a published floor.
- **Add the clause the Introduction draft was missing:** promise the pipeline lessons — reproducible randomness, the affordance gaps, the overlap overshoot — because that is the Data Note payload and otherwise the Discussion arrives unannounced.
- The generalisation sentence (illicit-drug epidemiology, social work, economics) moves to §6; it duplicated the planned Conclusion.

---

## 2. Methods

*Target ≈ 430 words. Cut from ten subsections to four, per the Methods reviewer. Load order: `paper.qmd` must open with a setup chunk reading `config.yaml` into `cfg` and the `results/` summaries into `lb`, `pop`, `err`, `rel` before any inline expression resolves.*

### 2.1 Source population and the Florida extract — ¶2 (~130 words)

- Source: the pseudopeople simulated US population, artifact `pseudopeople_simulated_population_usa_2_0_0`, generated by the Vivarium microsimulation `vivarium_census_prl_synth_pop`, with `simulant_id` as ground-truth identity across all observers [@haddock2024simulated; @pseudopeople_software]. Record the artifact name (not the internal `release_02_yellow` tag, which is undocumented publicly), the pseudopeople package version, and DuckDB `{python} duckdb_version`.
- Extraction: DuckDB reads the census-observer Parquet directly, filters `state = 'FL'` and `year = 2020` from `config.yaml`, deduplicates with `QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1`, yielding `{python} fl_simulants` simulants. SSNs come from the Social Security observer joined on `simulant_id`.
- **State the honest affordance gap, narrowly.** Verified in this project's venv (pseudopeople 1.2.8): `generate_decennial_census` *does* take `state=` and `year=` and *does* have a Dask engine. The Discussion draft's claim that pseudopeople "exposes no state filter, no predicate pushdown, and no lazy evaluation" is **false and must be deleted** — the author is a pseudopeople co-author and a reviewer will catch it. What is true and verified: `generate_social_security` has **no** `state` parameter, so the SSN join must be done by hand; and there is no API for prevalence-weighted or overlap-controlled sampling, which is the whole cohort design. Either report what `state='FL'` plus `engine='dask'` actually cost when tried, or say plainly it was not tried.
- Two-tier note: this is pipeline-tier code run manually; nothing in the rendered paper executes it. Soften any pandas claim to a memory-footprint argument — "cannot load even one state" is unmeasured.

### 2.2 Cohort design and reproducible sampling — ¶3 (~180 words)

- Design in one paragraph, targets from `config.yaml`: a registry stand-in targeting `{python} cfg_registry_target` records sampled with probability proportional to age- and sex-specific cancer prevalence, and two finder files targeting `{python} cfg_finder_500k_target` and `{python} cfg_finder_100k_target` records with `{python} overlap_500k_target` and `{python} overlap_100k_target` overlapping simulants. Weights are GBD all-neoplasm prevalence for Florida, 2021, mean over 1,000 draws, 22 age bins by sex, committed as `reference/gbd_neoplasm_prevalence_florida.csv`; range `{python} gbd_prev_min`% (males under 1) to `{python} gbd_prev_max`% (males 95+). **The file stores percentages** — format with `:.1f` and a literal `%`, never `:.0%`.
- Why prevalence and not incidence, in two sentences only (condensed from four bullets): a registry accumulated over decades holds everyone living with or having had a diagnosis, so its composition follows prevalence; incidence is the right comparator for the *shape* check in §2.4. Drop the unverified conjectures about "name eras" and "address stability" — the sufficient rationale is matching the registry's age/sex structure to Florida cancer demography.
- **Add the load-bearing fact all five drafts omitted:** overlap members are drawn from the registry cohort and the remainder from outside it via separate hash streams, and the two files are then noised *independently* (`psp_registry` seed `{python} cfg_seed_registry`, `psp_finder` seed `{python} cfg_seed_finder`). That independence is what makes this a linkage problem rather than a join.
- Reproducible randomness, **stated once here and not restated in the Discussion**: DuckDB's `random()` is not reproducible across threads, so every draw is made a pure function of the record key — the Efraimidis–Spirakis exponential-race key with the uniform replaced by a keyed hash. Quote the expression exactly, including the constant `18446744073709551617.0` (= 2⁶⁴+1); the Discussion draft's "2^64" is a paraphrase, and a section whose claim is bit-identical checksums cannot paraphrase the formula that produces them. Five salts give independent streams from seed `{python} cfg_seed_sample`.
- **Add the most reusable pattern in the pipeline, which no draft stated:** row-level omission noise deletes rows, so exact targets are unreachable in one pass; cohorts are drawn at `{python} cfg_oversample`× target and downsampled afterwards with `numpy.default_rng({python} cfg_seed_postprocess)` over sorted ID lists. Downsampling *after* noising is the direct cause of the overlap overshoot in §3.2 — the causal story the Data Note exists to tell. Note the reason for oversampling is that the number dropped is *not known in advance*, not that noise is nondeterministic (it is seeded and deterministic; that determinism is the point of §2.2's row-order fixes).
- The two silent order-dependence bugs, one sentence each: the staged Parquet must be written `ORDER BY simulant_id` because pseudopeople walks rows in file order, and the SSA join must be sorted before numpy selection. The run-twice assertion moves to `tests/`, mentioned in half a sentence; `lst-weighted-sample` is cut.

### 2.3 Noise, schema and packaging — ¶2 (~80 words)

- Base layer: pseudopeople's full default suite (omission, non-response, duplication; typos, OCR, phonetic, nicknames, fake names, month/day swaps, wrong digits, blanks). Targeted overrides from `config.yaml`, values never typed: finder files `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` SSN transposition, `{python} cfg_finder_address_missing` on each address field; registry `{python} cfg_registry_ssn_missing` / `{python} cfg_registry_ssn_transposed` / `{python} cfg_registry_address_missing`. Rationale in one clause: a researcher's finder file is dirtier than a certified registry's consolidated file. **The provenance of these rates is unresolved** — `config.yaml` credits an unread "FCDS 2024 monograph"; until confirmed, describe them as author-chosen and plausible, anchored to published registry figures [@qiao2023lexisnexis].
- Adjacent-digit SSN transposition is not in pseudopeople's noise taxonomy, so it is a post-hoc numpy step — the concrete affordance gap §4.1 generalises.
- Published columns: `simulant_id` plus first name, middle initial, last name, date of birth, sex, street number, street name, unit number, city, state, ZIP, SSN. Say the release covers **all fields required by either minimum matching rule** — not "exactly the fields FCDS requires", since the current submission layout also carries race, maiden name, full middle name, alias and birthplace. `tbl-schema-layout` is cut as repo documentation.
- Deterministic archive: zip built with `-X` and fixed member timestamps so archive metadata is deterministic; checksums published for the three CSVs and the bundle. Dataset version `{python} dataset_version`; `config.yaml` is the single source of truth.

### 2.4 Quality assurance and the linkage baseline — ¶2 (~90 words)

- QA check 1, external scale: the extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents (a cited literal — **needs a Census Bureau citekey**).
- QA check 2, registry demography: the realised age/sex composition of the registry cohort against the GBD weights, and — *if and only if the provenance is confirmed* — against published FCDS incidence rates by age group. `reference/fcds_incidence_by_age_sex.csv` carries "PROVENANCE — NEEDS CONFIRMATION BEFORE PUBLICATION" in its own header; if it cannot be confirmed, that panel is dropped and the QA claim narrows to weights-vs-realised. Say which happened.
- Define passing so it is falsifiable, and **do not use monotonicity**: verified against the committed file, female prevalence peaks at 21.84% in the 85–90 bin and dips at 90–95, and male prevalence dips between ages 2 and 15, so "rises monotonically with age" is falsified by the paper's own inputs. The criterion is agreement in peak band and in the male/female crossover, not in level — the registry is prevalence-weighted while FCDS publishes incidence.
- Baseline: each rule is agreement on every key of a key-set, evaluated as DuckDB hash joins (disjunctions as UNIONs, avoiding a nested loop over ~5×10¹¹ pairs). Do not enumerate the ladder in prose — that is the Results table. Metrics: precision and recall, reported also as false-match and missed-match rates after Lam et al. [@lam2024synthetic]; F1 is computed but not used to rank, per the F-measure critique [@hand2018fmeasure]; specificity and accuracy are omitted because true non-matches grow quadratically [@christen2007quality]. Deterministic linkage is a legitimate floor, not a straw man — the distinction from probabilistic methods is largely one of implementation [@doidge2018demystifying], and SEER–Medicare runs a deterministic algorithm in production [@enewold2020seermedicare]. **Do not import SEER–Medicare's ~96% as a linkage-accuracy figure** — it is the share of SEER persons 65+ found in Medicare enrolment.
- **Cut from Methods entirely:** the headline-foreshadowing bullet (those numbers appear once, in Results) and the "optional, not yet run" linked-vs-unlinked extension.

---

## 3. Results

*Target ≈ 430 words. Per IJPDS, the Data Note "Results" is where data issues and challenges live, so the two target misses lead rather than hide.*

### 3.1 The release — ¶1 (~110 words)

- One paragraph plus **Table 1**. The extract of `{python} fl_simulants` simulants is `{python} fl_share_census` of the official 2020 Census count. The registry holds `{python} registry_rows` rows for `{python} registry_simulants` distinct simulants; the `{python} registry_dupe_rows` excess rows are the within-file duplication a real registry carries.
- **Mechanism now verified against the shipped file** (2026-07-28, `pipeline/linkage_baseline.py` machinery): exactly 19 simulants appear twice, none more than twice, and in every case *the two rows differ in content* — they were noised independently. That is pseudopeople row-duplication noise, and it is the realistic case of a registry holding two differently transcribed reports on one patient. Say this as a verified fact, not an inference from subtraction, and note that it is why a record-pair count can exceed a distinct-simulant count (§3.2).
- Checksums are presented as a result, not housekeeping: they are what lets a user prove the file they hold is the file scored here. State honestly how many independent regenerations were compared and on what hardware; if only one build exists, write "we record checksums so reproducibility can be checked", not "reproducibility is demonstrated".

### 3.2 The two target misses — ¶2 (~120 words)

- **Overshoot.** Realised overlaps are `{python} overlap_500k_simulants` simulants against a target of `{python} overlap_500k_target`, and `{python} overlap_100k_simulants` against `{python} overlap_100k_target` — roughly a third over, because the exact-target downsampling step retained all surviving overlap pairs rather than thinning to target. **Define overlap once and stick to it:** distinct simulants present in both files. Report the pair count separately (`{python} overlap_500k_pairs`) because it is the denominator of recall in §3.4.
- **Reconciliation now verified**: the 500k finder overlaps the registry in 129,356 distinct simulants but 129,357 record pairs, because exactly one of those simulants sits on two registry rows (§3.1); for the 100k finder both counts are 25,797. State it as measured.
- Do **not** write "the overshoot costs the benchmark nothing": **measured**, it moves match prevalence from a designed 20% of finder rows to `{python} match_prevalence_500k` (25.87%) and `{python} match_prevalence_100k` (25.80%), which changes class balance and any model's priors. Write instead that the realised overlap is exactly known and published, so users must take the shipped counts, not the config targets, as the benchmark definition.
- **A third, previously unreported target miss — report it.** The two finder files were designed against the registry independently and their mutual overlap was never specified, but they in fact share `{python} overlap_finder_finder` (2,508) simulants. A user linking all three files therefore meets an undesigned three-way structure, and the 100k file is *not* a clean held-out replicate of the 500k file. Either document the figure as a property of v0.2 or fix it in a later version; do not leave it for a user to discover.
- **Registry SSN missingness.** Realised `{python} registry_ssn_missing` against the `{python} cfg_registry_ssn_missing` target, because a share of Florida simulants never held an SSN in the source population and the pipeline warns rather than blanking further. **Use a second, distinct variable** `{python} pop_ssn_never` for the population-level rate — it is not the same quantity as the registry-measured rate (the registry is a prevalence-weighted, noised, downsampled draw), and no draft may render "5.77%" as a literal in prose. Arguably more realistic than the target: the New York State Cancer Registry reported 3.4% of 1.4M records lacking SSN [@qiao2023lexisnexis].
- **Resolved — the two files do not contradict each other, and the resolution is worth one sentence.** Measured on the shipped files, finder SSN missingness is *exactly* 100,000 of 500,000 and 20,000 of 100,000 rows. The pipeline sets missingness by target count, not by an independent Bernoulli draw: it counts what is already missing and blanks only the shortfall. The finder files' structural never-had-SSN rate sits below their 20% target, so the code tops them up to exactly 20%; the registry's structural rate already exceeds its 5% target, so the code blanks nothing further and warns. One mechanism, two outcomes. Say this — a reader who notices the asymmetry will otherwise assume a bug.
- Other realised rates in one clause from `results/error_rates.json`, folded into Table 1's columns rather than a second table.

### 3.3 What the data look like — ¶1 (~80 words)

- **Table 2**: the same simulant as it appears in the registry and in a finder file, `simulant_id` printed so the reader can verify, with discrepant cells marked and the noise mechanism named per row. This is where a registry reader *sees* why exact joins must fail. Two or three pairs, chosen to show a nickname or typo, a transposed SSN, and a blanked field.
- Name the fidelity giveaways here, in two sentences, rather than burying them: addresses are uniformly lowercased, `city` takes values such as "unincorporated", and a person born in 2019 appears in a 2020 census extract. These are linkage-relevant — an address standardiser benchmarked here never meets real casing and abbreviation variation — and users must be told. Cross-reference §5.

### 3.4 The deterministic floor — ¶2 (~120 words)

- **Table 3** and its narration. Framing: the point is that the benchmark discriminates between strategies and publishes a floor. Name+DOB reaches precision `{python} r500_name_dob_precision` but misses `{python} r500_name_dob_missed` of true pairs; SSN alone is near-perfect on precision (`{python} r500_ssn_only_precision`) yet misses `{python} r500_ssn_only_missed` because a fifth of finder SSNs are blank; the exact-agreement rule on FCDS's name+SSN+sex field set makes no false matches but finds only `{python} r500_fcds_min_ssn_recall`, while the month/year variant admits `{python} r500_fcds_min_monthyear_fp` false matches; taking either raises recall to `{python} r500_fcds_either_recall`; the best simple rule, name+DOB or SSN, reaches `{python} r500_best_recall` at `{python} r500_best_precision`; a deliberately under-specified last-name+DOB rule collapses to precision `{python} r500_lastname_dob_precision`, showing the benchmark punishes weak keys.
- **Relabel the FCDS rules honestly.** These are exact-agreement rules on FCDS's minimum *submission* field sets — rules about which identifiers a submitter must supply, not about which fields must agree for a match, and FCDS itself matches probabilistically with clerical review. Presenting a conjunctive join as "FCDS's rule" is a straw man. State the vintage of each field set.
- Comparator, one clause: name+DOB-style deterministic rules on real data link 88–93% with 97–99% correct [@li2006deterministic], so the simulated difficulty sits in a realistic band.
- Cost of evaluation: the full ladder runs in `{python} baseline_seconds_500k` seconds on the 500k finder. **Record the node spec** alongside the timing or drop "on a single node" — the number is meaningless without it. Note the 100k finder gives materially the same metrics in one sentence; its panel is cut.
- Say what is *not* here: no normalised/blocked variant, no probabilistic run. Named as the main remaining work, once.

---

## 4. Discussion

*Target ≈ 330 words, three subsections. The comparator survey and its table are cut and live in §1.3; the reproducibility mechanism is cut and lives in §2.2; the "principal findings" number restatement is cut. Only the 95.6%-vs-59.8% gap survives as a re-quoted figure, because it is the one thing this section reasons about. A Data Note Discussion of this length owns zero figures and zero tables.*

### 4.1 Engineering lessons worth stealing — ¶2 (~140 words)

- The composition pattern, stated so a reader can reuse it: do the heavy relational work (filter, dedupe, SSA join, weighted sampling) in out-of-core SQL, stage the result as a Parquet directory mimicking the source layout, and point the simulator's `source` at it. The two tools compose through the filesystem. Treat the simulator as one stage of a pipeline you own, not as the pipeline — which is also why the bespoke SSN-transposition step was cheap to add.
- The reproducibility lesson in two sentences, no mechanism restated: **a seed pins the random stream, not the pairing of stream to rows.** Any pipeline whose row order is not contractually fixed can pass every unit test and still be irreproducible; simulation tools should document their row-order sensitivity. This generalises to any parallel engine because it removes the RNG from the engine entirely.
- The Dask comparison, honestly scoped. Keep it **qualitative**: DuckDB is single-node and SQL-only; Dask and Spark buy horizontal scale-out and arbitrary Python at the cost of orchestration and worker tuning [@person_linkage_case_study]. **Delete** the assertion that the prior project suffers "non-deterministic partition/row ordering that fights reproducibility" — it is an unsupported negative characterisation of a named colleague's repository, and even the authorship attribution is an inference the author must confirm. **Delete** the 8.7-second figure from this paragraph: that is the downstream linkage timing, not the build, and says nothing about whether a 21M-simulant construction fits one node. Either report the construction wall time, peak RAM and node spec, or make no scale claim. Note that Splink runs on a DuckDB backend, so the same engine serves construction and the experiments the dataset is for [@linacre2022splink].

### 4.2 Fidelity where it counts — ¶1 (~90 words)

- The argument that licenses the simplification: for a *linkage* benchmark, difficulty is set by the joint distribution of the identifying fields — name frequency spectra, DOB collision rates within blocks, household co-residence, field-level error and missingness. Age enters only through those channels. The last-name+DOB rule's precision of `{python} r500_lastname_dob_precision` is the mechanism made visible, and it is inherited from the source population's demographically structured names and households, not from the cancer weighting.
- Where the argument breaks down, stated before a reviewer states it: if linkage error interacts with age- or ancestry-specific name structure, a mis-shaped mix changes measured *rankings*, not just error levels [@mcgrathlone2021ethnicbias]; the source draws first and last names independently and floors name frequency at public-list thresholds, so the rare-name tail is thinner than reality [@haddock2024simulated]; and missingness here is largely at random within targeted fields, whereas real registry missingness is differential.
- Anchor the tolerance: synthetic identifiers reproduced real linkage-quality estimates within fractions of a percentage point at small scale [@lam2024synthetic] — evidence that ranking and stressing methods tolerates fidelity gaps that inference would not [@ruggles2025shortcomings].

### 4.3 Why open release, and what it risks — ¶2 (~100 words)

- **Fix the provenance argument.** Do not call ACS PUMS "public aggregate statistics" and do not claim "no real person's record contributed". PUMS is individual-level public-use microdata of real households, sampled to initialise the simulation. The defensible argument runs through PUMS's own disclosure protections (already released, de-identified, swapped, top-coded) plus the fact that there is no confidential dataset fitted to and therefore no membership to leak — which is what distinguishes this from the generative-model threat model that membership-inference attacks target [@stadler2022groundhog]. Under the regulator's test the question becomes coincidental resemblance, not identifiability [@ico2023pets].
- Name the residual risk: coincidental generation [@suchow2023coincidental]. With tens of millions of simulated Floridians some name+DOB+city combinations will match real people by chance. Weigh against it that every name is a recombination of names each shared by many real Americans by construction of the public source lists [@haddock2024simulated].
- **Argue the benefit case against the right counterfactual.** The existing pseudopeople gate is a public, logged GitHub request under a relational-governance process [@keyes2026governance] — inverting the risk calculus against *real registry data* instead is a false dilemma. State who the gate actually excludes: CI systems and containerised reproductions cannot open an issue; classroom and workshop use at scale; and a fixed, checksummed artifact makes *this paper's own results* reproducible in a way a re-request cannot.
- Guardrails as a short list: provenance documentation, determinism plus published checksums, a DOI deposit with versioning and a tombstoned withdrawal path [@zenodo_policies], prominent "simulated data" labelling, and a stated objection route. **Present the objection route as an untested proposal, not a novel contribution.** Changing the sampling salt re-draws *which* simulants are selected; it does not regenerate the names attached to a given simulant, so a complainant's name can reappear — and it destroys comparability with every published result on v0.2. If a mechanism is promised, it must be targeted suppression plus a tombstoned version bump, and it must actually be implemented on the deposit. Say "we are not aware of a comparable project that states one", which is what the evidence supports.
- **Add one sentence of positionality.** This section assesses the ethics of the author's own simulator, using his own governance framing, motivated by a monograph recommendation that names him personally. Acknowledging that pre-empts a reviewer raising it less charitably; the COI statement carries the rest.
- **Add the exposure no draft mentioned:** the files ship syntactically valid SSNs alongside full name, DOB and address. A released SSN can collide with a real issued number, and the corpus is usable as synthetic-identity seed material. The labelling guardrail should name the risk it mitigates, and contamination of a real registry system by simulated records should be raised.

---

## 5. Limitations

*Target ≈ 200 words. IJPDS's template has no separate Limitations heading; these render as the closing subsections of the Discussion. Merged from eight bullets down to five, removing three sets of duplication the reviewer identified.*

### 5.1 Identity resolution only — ¶1 (~55 words)

- No tumour site, histology, stage, diagnosis date or treatment; no natural history of cancer. The benchmark exercises finder-file-to-registry *identity* matching, not tumour consolidation or death clearance.
- **Add the gap that matters more to a registry audience:** the registry is essentially one row per person, so within-file duplicate detection — the central registry task, and the one NAACCR certifies against at under 0.1% for Gold [@naaccr2026certification] — is not exercised at all.

### 5.2 Imperfect fidelity may mis-rank algorithms — ¶1 (~45 words)

- Merge the Discussion draft's "imperfect fidelity" and "inherited population fidelity" bullets, which said the same thing twice. If a load-bearing feature of the real problem is absent — differential missingness, name change at marriage, first/last name dependence, the thin rare-name tail, all documented gaps of the source population [@haddock2024simulated] — package comparisons here could rank tools differently than production data would. That is the one error this resource must warn its users against. Recommend treating results as necessary, not sufficient, and validating winners in situ [@alexandersson2024comparing].

### 5.3 Known construction imperfections — ¶1 (~35 words)

- The overlap overshoot, the undesigned finder-to-finder overlap, and the SSN-missingness floor, cross-referenced to §3.2 rather than re-narrated, plus the visible artifacts from §3.3 (lowercased addresses, "unincorporated", the 2019-born infant in a 2020 extract). The config parameter is a target, and the pipeline can only ever move realised missingness up to it — never down.
- One consumer-facing defect worth a clause because it will bite the first user: the CSVs quote the rare field containing a comma (a `street_number` of `"64,66"` appears in `finder_100k.csv`), but they do so seldom enough that DuckDB's CSV sniffer infers no quote character and then fails to read the file. Anyone loading the release must name the quote character explicitly. Shipping Parquet alongside CSV in a future version would remove the whole class of problem.

### 5.4 Prevalence is not reportable incidence — ¶1 (~30 words)

- GBD all-neoplasm prevalence is not registry-reportable incidence, and the registry's case mix is validated only at the level of the age/sex shape comparison. **Delete** the unsupported clauses "includes benign neoplasms and long-past cases" — neither the ground truth nor the digest establishes what the GBD neoplasms envelope contains, and GBD cancer prevalence is generally modelled in time-limited post-diagnosis phases.

### 5.5 Locale and vintage — ¶1 (~35 words)

- Names, addresses and households are USA-circa-2020. Name distributions drift and transfer poorly: GeCo required structural forking for Brazilian composite and multiple family names [@trentin2018brazil]. Conclusions about name-comparator choice do not port to Brazil, Australia or non-Latin-script registries, and any ethnic-bias finding reflects US-2020 name structure only [@mcgrathlone2021ethnicbias].

---

## 6. Conclusion

*Target ≈ 90 words, ¶1.*

- What was done, in one sentence, without re-quoting numbers: a prevalence-weighted, state-scale, three-file simulated linkage benchmark with a published ground-truth key, a reproducible seeded pipeline, and a deterministic floor.
- The transferable lessons in one sentence: pin row order before a simulator consumes rows; oversample and downsample, but understand what downsampling after noising does to your design targets; and fill affordance gaps by owning the pipeline around the tool.
- Generalisation, moved here from the Introduction as the reviewer directed: the transaction this dataset is shaped like — a government-held population-scale file, a researcher cohort, a minimum-identifiers rule, no shareable ground truth — recurs in vital statistics and drug-epidemiology cohort follow-up, and beyond health in social work and economics.
- Close with the invitation that is also the decisive external-validity test: FCDS re-running its own package comparison on this corpus and reporting rank agreement with its internal results.

---

## Figures, tables and code listings

Five essential items plus one optional. Everything else proposed across the five drafts is cut; the cut list is at the end of this section so the decisions are visible rather than silent.

| Label | Kind | Caption | What it shows | Produced by | Status |
|---|---|---|---|---|---|
| `tbl-release` (Table 1) | Table | The released files: contents, overlap with the registry, targeted versus realised error rates, size and checksum. | Rows: `registry.csv`, `finder_500k.csv`, `finder_100k.csv`, bundle `.zip`. Columns: rows; distinct simulants; overlap target; realised overlap (simulants, with pairs footnoted); SSN missing target/realised; street-name missing target/realised; size (MB); MD5. Merges three separately proposed tables (`tbl-file-summary`, `tbl-overlap`, `tbl-file-design`) and absorbs `tbl-error-rates` as four columns. | `paper.qmd` chunk over `results/release_manifest.json` + `results/error_rates.json` + `results/linkage_baseline.json` + `config.yaml` | **Essential** |
| `tbl-example-pair` (Table 2) | Table | The same simulant as it appears in the registry and in a finder file, with the noise mechanism named for each discrepancy. | 2–3 paired rows over the published columns plus `simulant_id`; discrepant cells marked; caption also names the fidelity giveaways (lowercased addresses, `city = "unincorporated"`, a 2019 birth in a 2020 extract). The author's explicit Results ask, and it does double duty as the evidence behind §5.3. | `pipeline/example_pair.py` → `results/example_pair.csv` with pinned `simulant_id`s so the table is stable across reruns | **Essential** |
| `tbl-linkage-baseline` (Table 3) | Table | Deterministic exact-match rules scored against the `simulant_id` ground truth, 500,000-record finder file. | Five rules only — name+DOB; SSN alone; either FCDS minimum field set; current FCDS field set; name+DOB-or-SSN — plus `lastname_dob` if space allows, × {predicted pairs, TP, FP, precision, recall, missed-match %, false-match %}. Cut from 9 rules × 2 files × 8 metrics, which is a research-article table. 100k finder noted in one sentence. | `pipeline/linkage_baseline.py` → `results/linkage_baseline.json` (**exists and verified**) | **Essential** |
| `fig-registry-age-sex` (Figure 1) | Figure | Realised age and sex composition of the simulated registry against the GBD neoplasm-prevalence weights and the simulated Florida population. | Two panels or overlaid series by sex across the 22 age bins. Optional second panel comparing GBD incidence to published FCDS rates per 100,000 — **include only if the FCDS incidence provenance is confirmed**. Caption states the pass criterion is agreement in peak band and sex crossover, not in level, because the registry is prevalence-weighted while FCDS publishes incidence. Consolidates three separately proposed figures. | `pipeline/qa_age_sex.py` → `results/registry_age_sex.csv` + `reference/*.csv` | **Essential** |
| `lst-noise-demo` (Listing 1) | Code listing | Generating noised records with pseudopeople and a targeted noise override, on the bundled ~10k-simulant sample population. | 8–12 echoed lines: build the hierarchical `noise_config` **pulling the rate from `cfg['noise']['finder']['address_missing']`, not a hard-coded 0.05** (the demo must honour the convention it showcases); call `generate_decennial_census`; show `.head()` and a one-line realised-rate check. The paper tier's only live computation. | `paper.qmd` chunk (replaces the current `sample-demo` stub) | **Essential** |
| `lst-fcds-fixed-width` | Code listing | Converting finder-file rows to the current FCDS 360-character fixed-width Data Linkage Record Layout. | ~15 lines: uppercase names, DOB → `YYYYMMDD` with 9-fill, missing SSN → `999999999`, padding to position; then 2–3 emitted records. Targets the current layout; the 2007 Attachment 9 layout is cited for existence only. | `paper.qmd` chunk over a function in `src/` that **does not yet exist** | **Optional — cut first** |

**Cut, deliberately:** `tbl-access-comparison` (every cell is a cited fact, so it is not a Results table; the contrast becomes three sentences split between §1.2 and §4.3 — this resolves the Methods-vs-Results tug-of-war by deciding the material is prose); `tbl-benchmark-comparison` and `tbl-prior-benchmarks` (the same comparator survey proposed twice, now prose in §1.3); `tbl-schema-layout` (repo documentation); `tbl-noise-config` (four numbers, better as a sentence); `tbl-noise-rates` (entirely uncomputed — a Results section cannot present a promised table, and it was pre-billed as "the single most useful table" sight unseen); `lst-weighted-sample` (a second executable listing the budget cannot afford; the SQL becomes a one-line display expression in §2.2 and the run-twice assertion moves to `tests/`); `fig-qa-incidence` (merged as a panel of Figure 1).

---

## Computed values referenced in the text

Canonical variable names, deduplicated across the five drafts. **Only `results/linkage_baseline.json` exists today** — every row marked *TO WRITE* is currently a number that lives in a working notebook and nowhere else.

| `{python}` variable | Known value | `results/` file | Sentence |
|---|---|---|---|
| `fl_simulants` | 21,123,234 | `population_summary.json` — **TO WRITE** | "…we extracted the `{python} fl_simulants` simulated Florida residents in the 2020 decennial census." |
| `fl_share_census` | 0.9807 | `population_summary.json` — **TO WRITE** (denominator 21,538,187 is a cited literal) | "The extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents." |
| `pop_ssn_never` | *unknown — not yet computed* | `population_summary.json` — **TO WRITE** | "…because `{python} pop_ssn_never` of Florida simulants never held an SSN in the source population." |
| `registry_rows` | 5,000,019 | `linkage_baseline.json` (exists) | "The registry stand-in holds `{python} registry_rows` rows…" |
| `registry_simulants` | 5,000,000 | `linkage_baseline.json` (exists) | "…for `{python} registry_simulants` distinct simulants." |
| `registry_dupe_rows` | 19 — **verified**: 19 simulants × 2 rows, each pair differing in content | `release_manifest.json` — **TO WRITE** | "The `{python} registry_dupe_rows` excess rows are the within-file duplication a real registry carries." |
| `registry_ssn_missing` | 0.057723 | `linkage_baseline.json` (exists) | "Registry SSN missingness reached `{python} registry_ssn_missing`, above its target." |
| `finder_500k_rows` | 500,000 | `linkage_baseline.json` (exists) | "…two finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records." |
| `finder_100k_rows` | 100,000 | `linkage_baseline.json` (exists) | as above |
| `finder_ssn_missing` | 0.200 | `linkage_baseline.json` (exists) | "SSN is blank in `{python} finder_ssn_missing` of finder records." |
| `overlap_500k_simulants` | 129,356 — **verified** | `release_manifest.json` — **TO WRITE** | "Realised overlap is `{python} overlap_500k_simulants` simulants against a target of `{python} overlap_500k_target`." |
| `overlap_100k_simulants` | 25,797 — **verified** | `release_manifest.json` — **TO WRITE** | as above, 100k file |
| `overlap_finder_finder` | 2,508 — **verified**, undesigned | `release_manifest.json` — **TO WRITE** | "The two finder files themselves share `{python} overlap_finder_finder` simulants, which the design did not specify." |
| `match_prevalence_500k`, `match_prevalence_100k` | 0.258712, 0.257970 — **verified** | `release_manifest.json` — **TO WRITE** | "The overshoot lifts match prevalence to `{python} match_prevalence_500k` of finder rows, against a designed 20%." |
| `overlap_500k_pairs` | 129,357 | `linkage_baseline.json` (exists) | "Recall is computed over `{python} overlap_500k_pairs` true record pairs." |
| `overlap_100k_pairs` | 25,797 | `linkage_baseline.json` (exists) | as above |
| `overlap_500k_target` / `overlap_100k_target` | 100,000 / 20,000 | `config.yaml` (exists) | "…against targets of `{python} overlap_500k_target` and `{python} overlap_100k_target`." |
| `cfg_registry_target`, `cfg_finder_500k_target`, `cfg_finder_100k_target` | 5,000,000 / 500,000 / 100,000 | `config.yaml` (exists) | "The registry cohort targets `{python} cfg_registry_target` records…" |
| `cfg_oversample` | 1.5 | `config.yaml` (exists) | "Cohorts are drawn at `{python} cfg_oversample`× target…" |
| `cfg_seed_sample`, `cfg_seed_registry`, `cfg_seed_finder`, `cfg_seed_postprocess` | 42, 42, 1, 999 | `config.yaml` (exists) | "All stochastic steps take their seeds from `config.yaml`…" |
| `cfg_finder_ssn_missing` / `_ssn_transposed` / `_address_missing` | 0.20 / 0.01 / 0.05 | `config.yaml` (exists) | "Finder files receive `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` transposition…" |
| `cfg_registry_ssn_missing` / `_ssn_transposed` / `_address_missing` | 0.05 / 0.00 / 0.01 | `config.yaml` (exists) | "…against the registry's `{python} cfg_registry_ssn_missing` target." |
| `err_street_500k`, `err_street_100k`, `err_street_reg` | 0.049904, 0.04898, 0.010017 | `error_rates.json` — **TO WRITE** | Table 1 cells; "street name is blank in `{python} err_street_500k` of the 500k finder file." |
| `err_ssn_transposed` | *unknown — measurement not yet run* | `error_rates.json` — **TO WRITE** | "Adjacent SSN digits were transposed in `{python} err_ssn_transposed` of finder records." |
| `size_registry_mb`, `size_finder500k_mb`, `size_finder100k_mb`, `size_zip_mb` | 478, 46, 9.3, 422 | `release_manifest.json` — **TO WRITE** | Table 1 cells; "…zipped to a `{python} size_zip_mb` MB bundle." |
| `md5_registry`, `md5_finder500k`, `md5_finder100k`, `md5_zip` | `3db6ba1c…`, `818c1097…`, `e27d3a89…`, `5743ecd6…` | `release_manifest.json` — **TO WRITE** | Table 1 cells; "the published MD5 of the bundle is `{python} md5_zip`." |
| `gbd_prev_min`, `gbd_prev_max` | 0.59, 32.36 (**percent units**) | `reference/gbd_neoplasm_prevalence_florida.csv` (exists) | "…from `{python} gbd_prev_min`% (males under 1) to `{python} gbd_prev_max`% (males 95+)." |
| `gbd_prev_female_max` | 21.84 at ages 85–90 (**verified against the file**) | `reference/gbd_neoplasm_prevalence_florida.csv` (exists) | Figure 1 caption; "female prevalence peaks at `{python} gbd_prev_female_max`%." |
| `r500_name_dob_precision` / `_recall` / `_missed` | 0.99811 / 0.79361 / 0.20639 | `linkage_baseline.json` (exists) | "Name plus date of birth linked `{python} r500_name_dob_recall` at `{python} r500_name_dob_precision` precision." |
| `r500_ssn_only_precision` / `_missed` | 0.99979 / 0.21465 | `linkage_baseline.json` (exists) | "SSN alone reaches precision `{python} r500_ssn_only_precision` yet misses `{python} r500_ssn_only_missed`." |
| `r500_fcds_min_ssn_recall` | 0.65412 (FP = 0) | `linkage_baseline.json` (exists) | "…makes no false matches but finds only `{python} r500_fcds_min_ssn_recall` of true pairs." |
| `r500_fcds_min_monthyear_fp` / `_precision` | 5,974 / 0.94320 | `linkage_baseline.json` (exists) | "The month/year variant admits `{python} r500_fcds_min_monthyear_fp` false matches." |
| `r500_fcds_either_recall` / `_precision` | 0.81901 / 0.94662 | `linkage_baseline.json` (exists) | "Taking either field set raises recall to `{python} r500_fcds_either_recall`." |
| `r500_fcds_current_recall` | 0.59845 (FP = 0) | `linkage_baseline.json` (exists) | "Exact agreement on the current minimum field set links `{python} r500_fcds_current_recall` with no false matches." |
| `r500_best_recall` / `r500_best_precision` | 0.95596 / 0.99826 | `linkage_baseline.json` (exists) | "Name-and-birthdate-or-SSN links `{python} r500_best_recall` at `{python} r500_best_precision`." |
| `r500_lastname_dob_precision` | 0.70006 | `linkage_baseline.json` (exists) | "…collapses to precision `{python} r500_lastname_dob_precision`, showing the benchmark punishes weak keys." |
| `baseline_seconds_500k` | 8.7 | `linkage_baseline.json` (exists) | "The full ladder runs in `{python} baseline_seconds_500k` seconds." |
| `duckdb_version` | 1.5.4 | `linkage_baseline.json` (exists) | "Extraction, sampling and scoring run in DuckDB `{python} duckdb_version`." |
| `psp_version` | 1.2.8 in the current venv — **the version used at generation time is unrecorded** | `environment.json` — **TO WRITE** | "…generated with pseudopeople `{python} psp_version`." |
| `dataset_version` | 0.2 | `config.yaml` / `linkage_baseline.json` (exists) | "This Note describes dataset version `{python} dataset_version`." |
| `build_wall_hours`, `build_node_spec` | *unknown — not recorded* | `environment.json` — **TO WRITE** | "The full build completes in `{python} build_wall_hours` hours on `{python} build_node_spec`." |

---

## References to add to `references.bib`

`references.bib` currently contains **only a comment block** — every entry below must be created. Duplicate keys across the research digests are collapsed to one key per work: `haddock2024simulated` (not `haddock2024pseudopeople`), `lam2024synthetic` (not `lam2024synthid`), `harron2017guide` (not `harron2017linkagequality`), `fdoh_fcds_procedure_guide_2007` (not `fcds2007procedureguide`), `fcds_welcome` (not `fcds2026welcome`).

### Core (26 entries — cite these)

```bibtex
@misc{fcds_welcome,
  author       = {{Florida Cancer Data System}},
  title        = {The Florida Cancer Data System Home Page},
  howpublished = {\url{https://fcds.med.miami.edu/inc/welcome.shtml}},
  organization = {University of Miami Miller School of Medicine},
  note         = {Accessed 2026-07-28},
  year         = {2026}
}

@techreport{fdoh_fcds_procedure_guide_2007,
  author      = {{Bureau of Epidemiology, Florida Department of Health}},
  title       = {Procedure Guide for Studies that Utilize Patient Identifiable Data from the {Florida Cancer Data System}},
  institution = {Florida Department of Health},
  address     = {Tallahassee, FL},
  year        = {2007},
  month       = oct,
  note        = {Revised October 2007. Accessed 2026-07-28},
  url         = {https://www.floridahealth.gov/wp-content/uploads/2025/07/request-guide.pdf}
}

@misc{fcds_linkage_layout,
  author       = {{Florida Cancer Data System}},
  title        = {Data Linkage Record Layout},
  howpublished = {\url{https://fcds.med.miami.edu/downloads/datarequest/Data\%20Linkage\%20Record\%20Layout.pdf}},
  organization = {University of Miami Miller School of Medicine},
  note         = {Fixed-length 360-character ASCII record specification for linkage submissions. Accessed 2026-07-28}
}

@misc{fcds_data_release_procedures,
  author       = {{Florida Cancer Data System}},
  title        = {Procedures for Data Release},
  howpublished = {\url{https://fcds.med.miami.edu/downloads/datarequest/procedure\%20for\%20data\%20release\%20auto\%20data\%20request\%205_2017\%20draft\%202.pdf}},
  organization = {University of Miami Miller School of Medicine},
  year         = {2017},
  note         = {Ad hoc approval 8 weeks to 18 months; linkage filled within 8 weeks of approval; onsite-only linkage. Accessed 2026-07-28}
}

@misc{fcds_fees_2020,
  author       = {{Florida Cancer Data System}},
  title        = {Data Request Fees: Fees and Billing Procedure},
  howpublished = {\url{https://fcds.med.miami.edu/downloads/datarequest/Data\%20Request\%20Fees\%202_2020\%20Rev.pdf}},
  organization = {University of Miami Miller School of Medicine},
  year         = {2020},
  month        = feb,
  note         = {Sliding-scale data-linkage fee schedule. Accessed 2026-07-28}
}

@techreport{naaccr2023secondarysharing,
  author      = {{North American Association of Central Cancer Registries}},
  title       = {Cancer Registries: Secondary Data Sharing Fact Sheet},
  institution = {North American Association of Central Cancer Registries},
  year        = {2023},
  month       = feb,
  url         = {https://www.naaccr.org/wp-content/uploads/2023/02/Cancer-Registry-Secondary-Data-Sharing-Fact-Sheet_Final_2.9.23.pdf}
}

@misc{naaccr2026certification,
  author       = {{North American Association of Central Cancer Registries}},
  title        = {Certification Criteria},
  howpublished = {\url{https://www.naaccr.org/certification-criteria/}},
  note         = {Accessed 28 July 2026}
}

@article{harron2017challenges,
  author  = {Harron, Katie and Dibben, Chris and Boyd, James and Hjern, Anders and Azimaee, Mahmoud and Barreto, Mauricio L. and Goldstein, Harvey},
  title   = {Challenges in administrative data linkage for research},
  journal = {Big Data \& Society},
  volume  = {4},
  number  = {2},
  pages   = {2053951717745678},
  year    = {2017},
  doi     = {10.1177/2053951717745678}
}

@article{buchanich2009methodological,
  author  = {Buchanich, Jeanine M. and Youk, Ada O. and Marsh, Gary M. and Bornemann, Zb and Lacey, Steven E. and Kennedy, Kathleen J. and Hancock, Roger P. and Esmen, Nurtan A. and Lieberman, Frank S.},
  title   = {Methodological issues in a retrospective cancer incidence study},
  journal = {American Journal of Epidemiology},
  volume  = {170},
  number  = {1},
  pages   = {112--119},
  year    = {2009},
  doi     = {10.1093/aje/kwp091}
}

@techreport{alexandersson2023splinkfcds,
  author      = {Alexandersson, Anders},
  title       = {A Feasibility Study of the {Python} Package splink for Probabilistic Record Linkage (2023 Monograph Supplement)},
  institution = {Florida Cancer Data System},
  year        = {2023},
  month       = jun,
  url         = {https://fcds.med.miami.edu/downloads/RecordLinkageMonograph/2023/splink_monograph_2023_supplement.pdf}
}

@article{alexandersson2024comparing,
  author  = {Alexandersson, Anders},
  title   = {Comparing the linkage performance of {fastLink}, {Match*Pro} and {Splink} at the {Florida Cancer Registry} using simulated pseudopeople data},
  journal = {International Journal of Population Data Science},
  volume  = {9},
  number  = {5},
  year    = {2024},
  doi     = {10.23889/ijpds.v9i5.2786},
  note    = {IPDLN 2024 Conference Proceedings issue}
}

@article{haddock2024simulated,
  author  = {Haddock, Beatrix and Pletcher, Alix and Blair-Stahn, Nathaniel and Keyes, Os and Kappel, Matt and Bachmeier, Steve and Lutze, Syl and Albright, James and Bowman, Alison and Kinuthia, Caroline and Burke-Conte, Zeb and Mudambi, Rajan and Flaxman, Abraham},
  title   = {Simulated data for census-scale entity resolution research without privacy restrictions: a large-scale dataset generated by individual-based modeling},
  journal = {Gates Open Research},
  volume  = {8},
  pages   = {36},
  year    = {2024},
  doi     = {10.12688/gatesopenres.15418.2},
  note    = {version 2; peer reviewed}
}

@misc{pseudopeople_software,
  author       = {{Simulation Science Team, Institute for Health Metrics and Evaluation}},
  title        = {pseudopeople: realistic simulated data about a fictional United States population},
  year         = {2026},
  howpublished = {\url{https://github.com/ihmeuw/pseudopeople}},
  note         = {BSD 3-Clause license; documentation at \url{https://pseudopeople.readthedocs.io/}. Pin the version used at generation time.}
}

@article{keyes2026governance,
  author  = {Keyes, Os and Flaxman, Abraham D.},
  title   = {New Ways of Thinking About Data Governance},
  journal = {Interactions},
  volume  = {33},
  number  = {1},
  pages   = {24--27},
  year    = {2026},
  doi     = {10.1145/3774948}
}

@article{lam2024synthetic,
  author  = {Lam, Joseph and Boyd, Andy and Linacre, Robin and Blackburn, Ruth and Harron, Katie},
  title   = {Generating synthetic identifiers to support development and evaluation of data linkage methods},
  journal = {International Journal of Population Data Science},
  volume  = {9},
  number  = {1},
  pages   = {2389},
  year    = {2024},
  doi     = {10.23889/ijpds.v9i1.2389}
}

@article{harron2017guide,
  author  = {Harron, Katie L. and Doidge, James C. and Knight, Hannah E. and Gilbert, Ruth E. and Goldstein, Harvey and Cromwell, David A. and van der Meulen, Jan H.},
  title   = {A guide to evaluating linkage quality for the analysis of linked data},
  journal = {International Journal of Epidemiology},
  volume  = {46},
  number  = {5},
  pages   = {1699--1710},
  year    = {2017},
  doi     = {10.1093/ije/dyx177}
}

@article{hand2018fmeasure,
  author  = {Hand, David and Christen, Peter},
  title   = {A note on using the {F}-measure for evaluating record linkage algorithms},
  journal = {Statistics and Computing},
  volume  = {28},
  number  = {3},
  pages   = {539--547},
  year    = {2018},
  doi     = {10.1007/s11222-017-9746-6}
}

@incollection{christen2007quality,
  author    = {Christen, Peter and Goiser, Karl},
  title     = {Quality and Complexity Measures for Data Linkage and Deduplication},
  booktitle = {Quality Measures in Data Mining},
  series    = {Studies in Computational Intelligence},
  volume    = {43},
  publisher = {Springer},
  address   = {Berlin, Heidelberg},
  pages     = {127--151},
  year      = {2007},
  doi       = {10.1007/978-3-540-44918-8_6}
}

@article{doidge2018demystifying,
  author  = {Doidge, James C. and Harron, Katie},
  title   = {Demystifying probabilistic linkage: Common myths and misconceptions},
  journal = {International Journal of Population Data Science},
  volume  = {3},
  number  = {1},
  pages   = {410},
  year    = {2018},
  doi     = {10.23889/ijpds.v3i1.410}
}

@article{enewold2020seermedicare,
  author  = {Enewold, Lindsey and Parsons, Helen and Zhao, Lirong and Bott, David and Rivera, Donna R. and Barrett, Michael J. and Virnig, Beth A. and Warren, Joan L.},
  title   = {Updated Overview of the {SEER}-Medicare Data: Enhanced Content and Applications},
  journal = {JNCI Monographs},
  volume  = {2020},
  number  = {55},
  pages   = {3--13},
  year    = {2020},
  doi     = {10.1093/jncimonographs/lgz029}
}

@article{linacre2022splink,
  author  = {Linacre, Robin and Lindsay, Sam and Manassis, Theodore and Slade, Zoe and Hepworth, Tom},
  title   = {Splink: Free software for probabilistic record linkage at scale},
  journal = {International Journal of Population Data Science},
  volume  = {7},
  number  = {3},
  pages   = {1794},
  year    = {2022},
  doi     = {10.23889/ijpds.v7i3.1794}
}

@article{hildebrandt2020dapo,
  author  = {Hildebrandt, Kai and Panse, Fabian and Wilcke, Niklas and Ritter, Norbert},
  title   = {Large-Scale Data Pollution with {Apache Spark}},
  journal = {IEEE Transactions on Big Data},
  volume  = {6},
  number  = {2},
  pages   = {396--411},
  year    = {2020},
  doi     = {10.1109/TBDATA.2016.2637378}
}

@article{binette2022almost,
  author  = {Binette, Olivier and Steorts, Rebecca C.},
  title   = {(Almost) all of entity resolution},
  journal = {Science Advances},
  volume  = {8},
  number  = {12},
  pages   = {eabi8021},
  year    = {2022},
  doi     = {10.1126/sciadv.abi8021}
}

@article{saeedi2018famer,
  author  = {Saeedi, Alieh and Nentwig, Markus and Peukert, Eric and Rahm, Erhard},
  title   = {Scalable Matching and Clustering of Entities with {FAMER}},
  journal = {Complex Systems Informatics and Modeling Quarterly},
  number  = {16},
  pages   = {61--83},
  year    = {2018},
  doi     = {10.7250/csimq.2018-16.04}
}

@article{schnell2023microsim,
  author  = {Schnell, Rainer and Weiand, Severin V.},
  title   = {Microsimulation of an educational attainment register to predict future record linkage quality},
  journal = {International Journal of Population Data Science},
  volume  = {8},
  number  = {1},
  year    = {2023},
  doi     = {10.23889/ijpds.v8i1.2122}
}

@misc{zenodo_policies,
  author       = {{CERN / Zenodo}},
  title        = {Zenodo General Policies},
  howpublished = {\url{https://about.zenodo.org/policies/}},
  note         = {Accessed 28 July 2026; withdrawal/tombstone and DOI-persistence policy}
}
```

### Trim tier (cut these first if over length — cited in the outline but each survivable)

```bibtex
@article{schmidtmann2011krebsregister,
  author    = {Schmidtmann, Irene and Hammer, Gael and Sariyar, Murat and Gerhold-Ay, Aslihan},
  title     = {Record Linkage Comparison Patterns},
  year      = {2011},
  publisher = {UCI Machine Learning Repository},
  doi       = {10.24432/C51K6B}
}

@article{walonoski2018synthea,
  author  = {Walonoski, Jason and Kramer, Mark and Nichols, Joseph and Quina, Andre and Moesel, Chris and Hall, Dylan and Duffett, Carlton and Dube, Kudakwashe and Gallagher, Thomas and McLachlan, Scott},
  title   = {Synthea: An approach, method, and software mechanism for generating synthetic patients and the synthetic electronic health care record},
  journal = {Journal of the American Medical Informatics Association},
  volume  = {25},
  number  = {3},
  pages   = {230--238},
  year    = {2018},
  doi     = {10.1093/jamia/ocx079}
}

@inproceedings{christen2008febrl,
  author    = {Christen, Peter},
  title     = {Febrl: a freely available record linkage system with a graphical user interface},
  booktitle = {Proceedings of the 14th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining},
  pages     = {1065--1068},
  year      = {2008},
  doi       = {10.1145/1401890.1402020}
}

@inproceedings{tran2013geco,
  author    = {Tran, Khoi-Nguyen and Vatsalan, Dinusha and Christen, Peter},
  title     = {{GeCo}: an online personal data generator and corruptor},
  booktitle = {Proceedings of the 22nd ACM International Conference on Information \& Knowledge Management (CIKM '13)},
  pages     = {2473--2476},
  year      = {2013},
  address   = {San Francisco, CA, USA},
  doi       = {10.1145/2505515.2508207}
}

@inproceedings{talburt2009sog,
  author    = {Talburt, John R. and Zhou, Yinle and Shivaiah, Savitha Y.},
  title     = {{SOG}: A Synthetic Occupancy Generator to Support Entity Resolution Instruction and Research},
  booktitle = {Proceedings of the 14th International Conference on Information Quality (ICIQ 2009)},
  pages     = {91--105},
  address   = {Potsdam, Germany},
  year      = {2009},
  note      = {No DOI. Page range and author list confirmed only from the proceedings listing --- verify against the paper before submission.}
}

@article{qiao2023lexisnexis,
  author  = {Qiao, Baozhen and Austin, April A. and Musco, Jennifer and Insaf, Tabassum and Schymura, Maria J.},
  title   = {Using {LexisNexis} to Improve Social Security Number Information in the {New York State Cancer Registry}},
  journal = {Journal of Registry Management},
  volume  = {50},
  number  = {4},
  pages   = {138--143},
  year    = {2023},
  note    = {PMCID: PMC10945922; no DOI assigned}
}

@article{li2006deterministic,
  author  = {Li, Bing and Quan, Hude and Fong, Andrew and Lu, Mingshan},
  title   = {Assessing record linkage between health care and {Vital Statistics} databases using deterministic methods},
  journal = {BMC Health Services Research},
  volume  = {6},
  pages   = {48},
  year    = {2006},
  doi     = {10.1186/1472-6963-6-48}
}

@misc{suchow2023coincidental,
  author        = {Suchow, Jordan W. and G{\"u}rkan, Necdet},
  title         = {Coincidental Generation},
  year          = {2023},
  eprint        = {2304.01108},
  archivePrefix = {arXiv},
  doi           = {10.48550/arXiv.2304.01108}
}

@inproceedings{stadler2022groundhog,
  author    = {Stadler, Theresa and Oprisanu, Bristena and Troncoso, Carmela},
  title     = {Synthetic Data -- Anonymisation Groundhog Day},
  booktitle = {31st USENIX Security Symposium (USENIX Security 22)},
  address   = {Boston, MA, USA},
  publisher = {USENIX Association},
  pages     = {1451--1468},
  year      = {2022},
  doi       = {10.48550/arXiv.2011.07018}
}

@misc{ico2023pets,
  author       = {{Information Commissioner's Office}},
  title        = {Privacy-enhancing technologies ({PETs}) guidance: Synthetic data},
  year         = {2023},
  howpublished = {\url{https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/privacy-enhancing-technologies/what-pets-are-there/synthetic-data/}},
  note         = {Accessed 28 July 2026}
}

@article{ruggles2025shortcomings,
  author  = {Ruggles, Steven},
  title   = {The shortcomings of synthetic census microdata},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {122},
  number  = {11},
  pages   = {e2424655122},
  year    = {2025},
  doi     = {10.1073/pnas.2424655122}
}

@article{mcgrathlone2021ethnicbias,
  author  = {{Mc Grath-Lone}, Louise and Libuy, Nicol{\'a}s and Etoori, David and Blackburn, Ruth and Gilbert, Ruth and Harron, Katie},
  title   = {Ethnic bias in data linkage},
  journal = {The Lancet Digital Health},
  volume  = {3},
  number  = {6},
  pages   = {e339},
  year    = {2021},
  doi     = {10.1016/S2589-7500(21)00081-9}
}

@article{trentin2018brazil,
  author  = {Trentin, Vitor and Bastos, Val{\'e}ria and Costa, Myrian and Camargo, Kenneth and Sobrino, Rejane and Guill{\'e}n, Lu{\'i}s Carlos and Coeli, Cl{\'a}udia},
  title   = {Synthetic data generator for testing record linkage routines in {Brazil}},
  journal = {International Journal of Population Data Science},
  volume  = {3},
  number  = {4},
  pages   = {722},
  year    = {2018},
  doi     = {10.23889/ijpds.v3i4.722}
}

@misc{person_linkage_case_study,
  author       = {Burke-Conte, Zeb and Blair-Stahn, Nathaniel},
  title        = {person\_linkage\_case\_study: emulating {US Census Bureau} person linkage with {Splink} and pseudopeople},
  year         = {2024},
  howpublished = {\url{https://github.com/ihmeuw/person_linkage_case_study}},
  note         = {BSD 3-Clause. AUTHOR ATTRIBUTION IS AN INFERENCE from repository contributors --- confirm with Zeb Burke-Conte before citing by name.}
}
```

### NEEDS VERIFICATION — wanted by the text, but not verified by the research

Do not paste these into `references.bib` until each is checked. Four of the six block specific sentences from being written at all.

1. **Efraimidis & Spirakis (2006), weighted random sampling with a reservoir.** The Methods section names the technique after its inventors; naming without citing is not acceptable, and the "present it without attribution" escape hatch should be rejected. Probable target — *verify volume, pages and DOI before use*:
   ```bibtex
   @article{efraimidis2006weighted,
     author  = {Efraimidis, Pavlos S. and Spirakis, Paul G.},
     title   = {Weighted random sampling with a reservoir},
     journal = {Information Processing Letters},
     volume  = {97},
     number  = {5},
     pages   = {181--185},
     year    = {2006},
     doi     = {10.1016/j.ipl.2005.11.003}
   }
   ```
2. **GBD source for the neoplasm prevalence weights.** `reference/gbd_neoplasm_prevalence_florida.csv` documents only an internal `vivarium_inputs` extraction and its own header demands the round/release be recorded. As written this is an uncitable provenance chain for a headline Methods input. Needs either a GBD results-tool citation or the capstone paper, plus the round recorded in the CSV.
3. **US Census Bureau, Florida 2020 resident population (21,538,187).** The fact is verified (census.gov "Florida Was Third-Largest State in 2020"); no BibTeX entry exists. Either add a `@misc` with access date or drop the literal from prose — as of now the QA sentence cannot be cited.
4. **The "FCDS 2024 monograph."** `config.yaml` credits it with the choice of noise rates and flags "Confirm the monograph citation before publication." The PDF's existence is confirmed; its authorship and contents were never read. Until confirmed, describe the rates as author-chosen and plausible.
5. **The FCDS published incidence rates in `reference/fcds_incidence_by_age_sex.csv`.** Hand-transcribed, headed "PROVENANCE — NEEDS CONFIRMATION BEFORE PUBLICATION", and its counts total 3.2M across 18 age groups, far more than one year of Florida incidence. Confirm the report title, the diagnosis-year span and the rate denominator, or drop that panel of Figure 1.
6. **Faker / commercial generators.** No citable reference beyond package metadata, and the digest marks the "no cross-file identity" claim about commercial products as an unverified negative. The outline avoids naming them; keep it that way.

---

## Work still to be done before rendering

Ordered by dependency. Items 1–3 must complete before any other number in the paper can be trusted.

1. **Commit what already exists.** `config.yaml`, `pipeline/`, `results/` and `reference/` are all untracked. Commit them now, before anything else — the paper's only computed artifact is currently invisible to git and to any reviewer of the repo.
2. **`pipeline/extract_florida.py` → `results/population_summary.json`.** Port the Florida filter from the working notebook. Computes: `fl_simulants` (21,123,234); `fl_share_census`; `pop_ssn_never` (the *population-level* never-had-an-SSN rate, a new quantity distinct from the registry-measured rate); the registry duplicate-row count with its verified mechanism.
3. **`pipeline/build_cohorts.py` → staged Parquet + cohort ID lists.** Port the weighted sampling, the five salted hash streams, the SSA join and the ordering fixes. **The acceptance test is that the pipeline reproduces the four published md5 checksums.** If it does not, the reproducibility claim fails and §2.2, §3.1 and the Conclusion all change. This is the single highest-risk item in the run list.
4. **`pipeline/apply_noise_and_package.py` → `results/release_manifest.json` and `results/error_rates.json`.** Manifest: per-file rows, distinct simulants, overlap by *both* definitions (distinct simulants and row pairs — this is what reconciles 129,356 vs 129,357), byte sizes, MD5 **and SHA-256** (upstream pseudopeople releases publish SHA-256; matching that practice costs nothing). Error rates: realised missingness per targeted column per file **plus the SSN-transposition rate, which has never been measured**, alongside the targets from `config.yaml`. Record the finder–finder overlap (2,508) and match prevalence per finder file here too — both are verified but live in no committed file yet. (Why finder SSN missingness lands at exactly 0.200 is now resolved: the noise step sets missingness by target *count* and tops up only the shortfall, so the finder files hit 20% exactly while the registry, whose structural floor already exceeds its 5% target, is left alone.)
5. **`pipeline/qa_age_sex.py` → `results/registry_age_sex.csv`.** Registry and Florida-population counts by age bin and sex, plus the GBD weights used. Backs Figure 1 and the §4.2 claim about where the registry's mass sits, which currently cannot be made because the realised distribution has never been computed.
6. **`pipeline/example_pair.py` → `results/example_pair.csv`.** Search the overlap for exemplars showing a nickname or typo, a transposed SSN, a blanked address field, and a swapped month/day; pin the chosen `simulant_id`s so Table 2 is stable across reruns. Verify such exemplars actually exist before promising all four.
7. **Extend `pipeline/linkage_baseline.py` and re-run.** Add the current layout's *other* minimum combination (name + sex + DOB + ZIP + street address) as a tenth rule — the shipped files carry every field it needs, and without it the paper covers only half of FCDS's current submission floor. Record the node spec (cores, RAM) alongside `seconds`, or the timing claim must be dropped.
8. **`results/environment.json`.** Pseudopeople version used at generation time (the venv has 1.2.8, but dataset v0.2 predates it), Python version, DuckDB version, node spec, and the construction run's wall time and peak RAM — the numbers §4.1 needs to make any scale claim at all.
9. **Deposit and mint DOIs.** Build the deterministic zip, deposit on Zenodo, mint a dataset DOI and a code-archive DOI, and obtain the private reviewer access URL IJPDS requires at submission. The Data Availability Statement, the abstract and Key Features cannot be finalised without these.
10. **Fix `paper.qmd` front matter.** Author is literally "Your Name"; ORCID is all zeros; the title lacks the mandatory `Data Note: ` prefix; the abstract stub uses the five-heading Research Article format instead of the four-heading Data Note format; the section is titled "Highlights" instead of "Key Features"; there is no Background section. Add the back-matter statements (Ethics, COI, Data Availability, Publication Consent, Funding, AI Disclosure, Abbreviations) — all mandatory, and the AI Disclosure especially, since this manuscript is AI-assisted.
11. **Render once and commit `_freeze/` with `results/`.** Per `CLAUDE.md`, freeze hashes `paper.qmd` only and does not watch `src/`, `config.yaml` or data, so a render is required after every `src/` change and the two directories must be committed together.

---

## Open decisions for the author

1. **Manuscript type:** submit as a Data Note (2,000–3,000 words including references) or as a Data Resource Profile (3,000–8,000 words)? Note that the Data Note overage fee is only £50 for up to 5,000 words over, so cost is not the constraint — genre fit and reviewer patience are. **Data Note, or Data Resource Profile?**
2. **Title:** adopt the recommended title above, or one of the three runners-up? **Which one?**
3. **Overlap definition:** report the overlap as distinct simulants in both files (recommended, with pairs footnoted), or as record pairs? **Simulants or pairs?**
4. **FCDS rule vintage:** foreground the 2007/2016 Procedure Guide rule, the current Data Linkage Record Layout rule, or both with the ambiguity stated (recommended)? **Which?**
5. **"Jo Lam's proposed quality metrics":** did you mean the missed-match / false-match framing of Lam et al. 2024, or the unpublished ITALO reporting work? If ITALO, there is no citable artifact yet. **Lam et al. 2024, or ITALO?**
6. **Noise-rate provenance:** can you confirm the FCDS 2024 monograph's authorship and that it characterises these rates — yes or no? If no, the paper describes the rates as author-chosen. **Yes or no?**
7. **FCDS incidence table:** can you confirm the source, year span and denominator of `reference/fcds_incidence_by_age_sex.csv` before publication? If no, the incidence panel of Figure 1 is dropped. **Yes or no?**
8. **Objection/redress mechanism:** do you commit to implementing a working one (targeted suppression plus a tombstoned version bump) on the deposit, or present it explicitly as an untested proposal? A salt change does not work — it re-draws which simulants are selected, not the names attached to them. **Commit, or present as proposal?**
9. **Licence:** CC0 (recommended — attribution stacking is impractical for benchmark data embedded in test suites) or CC-BY? **CC0 or CC-BY?**
10. **Conflict of interests:** disclose that you built pseudopeople, co-authored the source population, help govern access to it, and are named personally in the monograph recommendation that motivates this paper — or declare "None"? Recommended: disclose. **Disclose or not?**
11. **`person_linkage_case_study` attribution:** have you confirmed with Zeb Burke-Conte that he is the author and is content to be cited? **Yes or no?**
12. **Attachment 9 conversion demo:** keep `lst-fcds-fixed-width` (requires writing the converter in `src/`) or cut it as the first casualty of the word limit? **Keep or cut?**
13. **Funding:** what grant supports *this* work, as distinct from the underlying population's Gates INV-060835 and Census CB21RMD0160001 — or is it "no specific funding"? **Which?**
14. **Acknowledgment by name:** may Anders Alexandersson be thanked by name for the monograph recommendation, and have you asked? **Yes or no?**