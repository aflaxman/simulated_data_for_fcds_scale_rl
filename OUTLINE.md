# Outline: Data Resource Profile: A Florida-scale simulated dataset for developing and benchmarking record-linkage software for cancer data systems

> **Status, 2026-07-28.** This is a planning document, not a draft. It was assembled from the working notebooks in
> `/ihme/homes/abie/notebook/2026/` (chiefly `2026_02_11b_duckdb_psp_reproducible_randomness.ipynb`), from literature
> research, and from measurements taken directly against the shipped v0.2 files. Claims marked **verified** were
> measured or checked on this date; everything else is marked *TO WRITE*, *to confirm*, or *unverified* and should be
> treated as a claim the paper cannot yet make. The deterministic-linkage baselines are real and reproducible today via
> `uv run python pipeline/linkage_baseline.py`; nothing else in `results/` exists yet.
>
> **Update 4, 2026-08-09 (latest).** Merged with the author's own DRP outline. The author's calls: **no m/u table** — Fellegi–Sunter framing is a distraction from the paper's point (cut from the abstract, §2.5, §3.3, the display list, the computed values, and the run list; `fellegi1969theory` removed from the references); **the deterministic ladder stays**, now with a plain-English explainer and an exposition budget in §3.4; **race/ethnicity stratification stays provisionally** (decision #15); **lingo fixed per the FCDS Procedure Guide** — *finder file* = the researcher-submitted cohort, matched against the *statewide incidence file*, whose stand-in is our registry file. Absorbed from the author's outline: the harm-foreshadowing sentence (§1.4, delivered in §4.4); the fuller simulation description, the honest extract-friction narrative, and the AI-assistance disclosure (§2.1); the three-way load benchmark (§3.1); the data-quality forensics — common names, date parseability, sentinel checks, and the do-not-geocode address warning (§3.2–§3.3); the insider limitations — disease as a bolt-on, simplistic household dynamics, no phone/email fields (§4.2); the download-monitoring plan and release-as-experiment framing (§4.3, §6); and the Census Bureau acknowledgment, rephrased neutrally (§7). New decisions #16–#17; new needs-verification items #7–#10.
>
> **Update 3, 2026-08-08 (later still).** Reworked as an IJPDS **Data Resource Profile**, per the submission guidelines the author supplied verbatim — which supersede this outline's earlier, partly wrong claims about a "Data Note" article type (the journal's current Data Note call is a four-section process-notes genre with no Results section, and no formal Data Note manuscript type appears in the author guidelines at all). Consequences: the body runs Background → Methods → Results → Discussion → Data Access → Conclusions with **no Introduction section**; Key Features follows the journal's six-bullet roster; the abstract's Results describes contents and quality, not problems; Results pivots from inventory-plus-confessions to a **difficulty portrait** — per-field m/u probabilities, quasi-identifier uniqueness, and error statistics stratified by race/ethnicity (`race_ethnicity` joins the released schema in the v0.3 rebuild); the old Limitations section merges into the Discussion; a Data Access section and the full roster of required back-matter statements are added. Open decision #1 (genre) is resolved.
>
> **Update 2, 2026-08-08 (later).** The overlap overshoot is resolved by decision: fix the sampler and rebuild as **v0.3**. The corrected stratified trim is implemented and unit-tested (`src/simulated_data_for_fcds_scale_rl/downsample.py`; `tests/test_stratified_trim.py`, 6 passing) — but the heavy rebuild has **not** run, so the shipped files are still v0.2 and every measured number in this outline is a v0.2 measurement that will change (see the banner over the computed-values table). The overshoot's narrative footprint shrinks to a two-sentence QA story in §3.2; the finder–finder overlap becomes 0 by design; the SSN-missingness floor remains the honest structural deviation.
>
> **Update, 2026-08-08.** The Introduction is reframed to the author's outline: record linkage as an ingredient of the "big data" hypothesis; lack of access to confidential data as the barrier to linkage testing and adoption; the simulated-data lineage (faker, FEBRL/GeCo, SOG, and most recently pseudopeople) failing on either realism or access friction; and an extremely low-barrier dataset at the scale of the Florida cancer registry's typical linkage challenge as the response — with the paper reporting the resource, the process of its development, and demonstration usage. The reframe propagates to the Editor's note, Key Features, the abstract, §§1.1–1.4, §3.4, §4.3, §6, and the references (faker entry added; the uptake-barrier claim's evidence base consolidated in §1.3).

**Editor's note.** The single claim this paper makes is: *what blocks record-linkage research and development is access to realistic test data, not methods — and here is a simulated, ground-truthed benchmark at the scale and cancer demography of a real US state registry that anyone can download without asking permission, together with a difficulty portrait that tells a user how hard the linkage is and for whom.* It is for two audiences at once — cancer-registry staff and vendors who need somewhere to test matching software that is not their own confidential file, and the linkage-methods community that has metrics but no large shared corpus. The release itself is framed as an experiment (2026-08-09): download volume will be compared with pseudopeople's PyPI installs and with the request counts for its gated state/national files, making the uptake-barrier claim falsifiable (§4.3, §6). The paper is an IJPDS **Data Resource Profile**, so the genre reward *is* the dataset description: contents, characteristics, quality, and demonstrated and suggested uses. The pipeline war stories a Data Note would have foregrounded — reproducible randomness under a parallel SQL engine, the overshoot the v0.2 unstratified trim caused (caught against the ground-truth key, fixed in `src/`, rebuilt as v0.3), the simulator affordance gaps — compress into Methods and one Discussion paragraph. Before this can be submitted, five things must happen, in this order: (1) commit `config.yaml`, `pipeline/`, `results/` and `reference/` — **done as of `ddd88c5`** (all four are tracked; the stratified-trim module and its tests joined them 2026-08-08); (2) port the build from the working notebook into `pipeline/` scripts — with `stratified_trim` from `src/` in place of the notebook's buggy downsampling cell, and `race_ethnicity` carried into the released schema — and rebuild as v0.3; the v0.2 checksums are obsolete *by design*, so the acceptance test becomes hitting every design target exactly plus run-twice checksum identity on the new files; (3) write the small `results/` summaries from the v0.3 build, including the forensics file and the stratified baselines (the existing `linkage_baseline.json` describes v0.2 and must be re-run); (4) resolve the two provenance holes that currently have no citable source — the FCDS incidence table used for QA, and the "FCDS 2024 monograph" credited in `config.yaml` with the choice of noise rates; (5) mint the Zenodo DOI, because IJPDS requires a dataset DOI plus a private reviewer URL at submission and the Data Availability Statement cannot be finished without them. On length: the guidelines the author supplied do not state the Data Resource Profile word limit — they defer to the journal's Fee Structure table, which must be checked before submission (overage is £50 for up to 5,000 words over in any case). The section targets below sum to ≈4,500 words plus display items, comfortable for the genre; the compression pressure the Data Note assumption imposed is gone.

---

## Title, authors, keywords

**Recommended:** *Data Resource Profile: A Florida-scale simulated dataset for developing and benchmarking record-linkage software for cancer data systems*

The journal requires the title to begin `Data Resource Profile: ` (the runner-up titles below take the same prefix swap). This version keeps the working title's content while fixing a modifier-attachment bug in it: "research and development of Florida-scale record linkage software" reads as though the *software* is Florida-scale. It is the data that is. "Developing and benchmarking" also names both uses, which matters because the benchmark half is what the deterministic baseline and the ground-truth key are for. The Background's objective sentence ("research and development … at the scale of the Florida cancer registry's typical linkage challenge") echoes the working title, but the recommendation stands — "developing and benchmarking" says the same thing without the modifier bug.

Runners-up:

| Option | Why it might win | Why it does not |
|---|---|---|
| *Data Note: Building a state-scale simulated linkage benchmark with pseudopeople and DuckDB* | Foregrounds the pipeline lessons, which is precisely the register IJPDS Data Notes reward | Buries cancer and the registry audience; reads as a methods paper, and the cancer-demography weighting is the paper's most distinctive design choice |
| *Data Note: Simulated finder files and a simulated cancer registry at Florida scale, with ground truth, for open linkage benchmarking* | Most concrete about what actually ships; "finder file" is the term FCDS submitters use | Longest of the four; "ground truth" is jargon to registry staff, and "cancer data systems" (the generalisable phrase) disappears |
| *Data Note: Simulated data for research and development of Florida-scale record linkage software for cancer data systems* | The author's working title, minimally adapted — safest for continuity with repo and deposit naming | Carries the modifier bug above |

**Author.** Abraham D. Flaxman, Institute for Health Metrics and Evaluation, University of Washington, Seattle, WA, USA. ORCID must be filled in — `paper.qmd` currently reads `Your Name` / `0000-0000-0000-0000`. Data Resource Profiles require **full addresses of all authors** — use the complete IHME street address, not just the affiliation line.

**Keywords (7):** record linkage; entity resolution; simulated data; cancer registry; benchmark dataset; reproducibility; pseudopeople.

---

## Key Features

The journal caps Key Features at **six bullets of one or two sentences each** and models them on a fixed roster — what is unique, why created, details (location/size/composition), data linkage, main categories of data, and how to access/collaborate. Follow the roster; reviewers will look for it. The reproducibility bullet and the deterministic-baselines bullet of earlier drafts demote to Methods and Results, where this genre puts them.

- **What is unique:** to our knowledge the largest openly downloadable *fully simulated* multi-file person corpus with cross-file ground-truth identity — every record carries `simulant_id`, so missed-match and false-match rates of any method are computed exactly rather than estimated [@harron2017guide; @lam2024synthetic]. Larger open person benchmarks exist but are built from real voter records with few attributes [@saeedi2018famer].
- **Why created:** linkage software for cancer registries must be developed and tested on names, dates of birth, addresses and SSNs — exactly the identifiers confidentiality rules prevent registries from releasing — and every comparably realistic substitute sits behind at least a lightweight access request, which we believe has been a barrier to uptake [@keyes2026governance]; the Florida registry's own feasibility study formally recommended a public test corpus [@alexandersson2023splinkfcds].
- **Details:** a simulated 2020 Florida resource drawn from `{python} fl_simulants` simulants: a registry stand-in of `{python} registry_rows` records whose age and sex structure follows Global Burden of Disease neoplasm prevalence for Florida, plus researcher finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records.
- **Data linkage:** the ground-truth key makes the designed overlaps exact — `{python} overlap_500k_target` and `{python} overlap_100k_target` simulants shared with the registry, none between the finder files — so every linkage run against the registry is exactly scoreable.
- **Main categories of data:** person-level identifiers as they appear in linkage practice — names, date of birth, sex, street-address fields, SSN, race/ethnicity — carrying pseudopeople's realistic noise (typos, nicknames, month/day swaps, blanks, duplications) plus targeted overrides.
- **Access:** direct download under a permissive licence with a DOI — no application, no approval, no data-use agreement; contact the corresponding author to collaborate.

---

## Structured abstract (draft, 272 words — recount before submission; ≤300 permitted)

The Data Resource Profile abstract keeps four headings but assigns each dataset-first content: **Introduction** = a brief summary of the dataset; **Methods** = how it was created, original sources, linkage; **Results** = where it is held, contents, quality; **Conclusion** = how to access, suggested uses, ongoing improvements. The pipeline-lessons conclusion of the Data Note draft is retired. Each `{python}` placeholder is counted as one word.

> **Introduction**
> We present a simulated resource for developing and benchmarking cancer-registry record linkage: a registry stand-in and two researcher finder files at the scale of the Florida Cancer Data System's (FCDS's) linkage workload, with a published ground-truth identity key. Linkage software must be developed and tested on names, dates of birth, addresses and Social Security numbers (SSNs), which confidentiality requirements prevent registries from releasing, and existing substitutes are orders of magnitude too small, unrealistically clean, or gated behind access approval that deters uptake.
>
> **Methods**
> From the pseudopeople simulated United States population we extracted the `{python} fl_simulants` simulated Florida residents in the 2020 decennial census. We sampled a registry stand-in of `{python} registry_rows` records, weighted by Global Burden of Disease neoplasm prevalence for Florida by age and sex, plus finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records with exactly `{python} overlap_500k_target` and `{python} overlap_100k_target` simulants overlapping the registry. Keyed-hash sampling and a stratified trim make each file a pure function of one recorded seed; pseudopeople noise plus targeted overrides supply realistic errors.
>
> **Results**
> The files are an open deposit on Zenodo, checksummed for verification. Against the ground-truth key, name plus date of birth links `{python} r500_name_dob_recall` of true pairs at `{python} r500_name_dob_precision` precision; exact agreement on FCDS's current minimum field set links `{python} r500_fcds_current_recall` with no false matches. We publish quasi-identifier uniqueness, per-field error rates, and linkage statistics stratified by race/ethnicity; registry SSN missingness sits above target because some simulants never held an SSN.
>
> **Conclusion**
> The dataset is a direct download with a DOI: no application, no approval. We suggest it for benchmarking and tuning linkage software, studying differential linkage error, and teaching; planned improvements include Parquet distribution and probabilistic baselines.

---

## 1. Background

*Combined target ≈ 700 words. A Data Resource Profile has **no Introduction section in the body**: the four-heading abstract carries the summary, and the body opens with Background — "a detailed overview of the rationale for creating the dataset and the various sources of data from which the resource was created." The author's four introduction beats survive intact as the Background's arc (big-data hypothesis → confidential-data barrier → simulated-data lineage → low-barrier objective), followed by the sources overview the genre asks for. Spell out "record linkage" throughout — to most readers "RL" means reinforcement learning, and the abbreviation should not appear in the paper.*

### 1.1 Rationale: record linkage under the "big data" hypothesis, and the data it cannot get — ¶2 (~180 words)

- Open on the hypothesis, one sentence: much of what population data science promises rests on the claim that existing data sources — administrative, clinical, registry — can yield insights without new, expensive and time-consuming data collection [@harron2017challenges]. Record linkage algorithms are a load-bearing ingredient of that claim, because reuse means combining sources never designed to be combined, and when linkage is wrong everything downstream inherits the error [@doidge2018demystifying].
- Then the concrete instance, kept from the previous draft because it is still the best ratio in the paper: Florida's reporting facilities send FCDS more than 310,000 case reports a year, which must resolve to roughly 145,000 newly diagnosed cases; the registry also links incidence to the state mortality file for passive follow-up [@fcds_welcome]. Cite with access date — the page carries no as-of date. Recognising that two differently spelled records describe one person *is* the product.
- The barrier, the outline's second beat: the identifiers linkage software runs on are exactly what confidentiality rules prevent from leaving the registry, and NAACCR states plainly that restrictive and varying state policies limit onward sharing of registry-derived data [@naaccr2023secondarysharing] — so testing stalls, and adoption follows. Three consequences, one clause each: separating linkage from analysis makes linkage a black box whose reliability researchers struggle to judge [@harron2017challenges]; access, where granted, is slow and costly — one 224,000-member occupational cohort spent about 700 hours and $22,440 over five years obtaining approvals and matches from state registries [@buchanich2009methodological]; and even a researcher who clears every hurdle gets no answer key, because real registry data carries no ground truth for which candidate pairs are the same person, so accuracy can only be estimated [@harron2017guide].
### 1.2 The transaction the dataset imitates — ¶1 (~120 words)

- Define "finder file" once, here, and never again: a researcher submits a cohort's identifiers, FCDS links them against the statewide incidence file, and returns matched records. **Lingo fixed per the Procedure Guide (author, 2026-08-09):** *finder file* = the researcher-submitted cohort; the two released 500k/100k files are the finder files; the 5M file is the *registry stand-in* (statewide incidence file). Never call the registry a finder file — the author's working outline used "master database"/"match files", which must not survive into the draft. **This is the only place the FCDS minimum-fields rule is stated** — Methods refers back to it. State both vintages, because they differ and no document establishes which supersedes: the 2007/2016 Procedure Guide requires first + last name AND SSN AND sex, *or* first + last name AND month and year of birth AND sex [@fdoh_fcds_procedure_guide_2007]; the current Data Linkage Record Layout requires name + sex + DOB + SSN, *or* name + sex + DOB + ZIP + street address, in a fixed-width ASCII record [@fcds_linkage_layout]. The released files satisfy either.
- One sentence of friction, not a table (see the display-item budget): identifiable FCDS data requires serial DOH IRB and Cancer Registry Review Committee approval with notarized confidentiality pledges and destruction on completion [@fdoh_fcds_procedure_guide_2007]; linkage runs onsite only and carries a sliding fee schedule [@fcds_data_release_procedures; @fcds_fees_2020]. **Attribute turnaround figures to their vintage** ("per FCDS's 2017 release procedures") — the digest marks current times as unverified. This bullet now does double duty: it is §1.1's "expensive and time-consuming" claim made concrete for FCDS, so the vintage attribution has to be exact.

### 1.3 Simulated data is the proposed fix, and why the shelf is bare — ¶2 (~150 words)

*Compressed from a full page in the Introduction draft plus a duplicate subsection and table in the Discussion draft, now organised along the author's two failure axes: **not realistic enough**, or **gated behind approval**. The comparator landscape is stated **once, here**, in prose. `tbl-prior-benchmarks` and `tbl-benchmark-comparison` stay cut.*

- Axis one, realism and scale. Generic fake-data tools such as faker produce clean, plausible, unlinked records — no error model, no cross-file identity, so no linkage testbed [@faker_software]. Linkage-specific generators model the right errors at the wrong scale: in the only controlled head-to-head benchmark, only three of five tools exceeded one million records, GeCo needed about 13 hours to corrupt one million and produced nothing at ten million [@hildebrandt2020dapo]; the shipped FEBRL and SOG corpora are counted in thousands [@christen2008febrl; @tran2013geco; @talburt2009sog], and the public benchmark inventory confirms the pattern [@binette2022almost].
- Be scrupulous about the counter-examples, because a reviewer will be: the largest openly downloadable person benchmarks are real North Carolina voters — 10M records with as few as four attributes, excluding children, so age-structured opposite to a cancer registry [@saeedi2018famer]. The one prior ~20M-person microsimulation built to study linkage quality does not appear to have been released [@schnell2023microsim]. The only cancer-registry benchmark ships precomputed comparison vectors with no names or dates, so it cannot exercise blocking or string comparison [@schmidtmann2011krebsregister]. Synthea publishes a million rich synthetic patients but no identifier-error model and no cross-file ground truth [@walonoski2018synthea].
- Axis two, access friction — the new beat, and pseudopeople's slot in the lineage: pseudopeople clears the realism and scale bar (a simulated US population with a ground-truth identity key [@haddock2024simulated]), but its large-scale populations require an access request [@keyes2026governance]. State the uptake claim with the author's hedge — approval, "even if lightweight, appears to be a barrier to uptake" — and give the evidence that makes the hedge honest in the same breath: FCDS's own 2023 Splink feasibility study ran on a 1,000,000 × 1,000,000 synthetic test file supplied privately by the present author, stated that "the datasets are not yet publicly available", and formally recommended making the test data public [@alexandersson2023splinkfcds]; the published follow-up comparison of fastLink, Match\*Pro and Splink then ran at Rhode Island scale, roughly one twentieth of the population FCDS serves [@alexandersson2024comparing]. (Moved here from §1.2: under the new framing this is evidence for the uptake-barrier claim, not registry colour.) Say this profile *responds directly to* that recommendation — **not** "is literally the fulfillment of", which the reviewer correctly flagged as overstated since this is a different, larger corpus. If the installs-vs-requests ratio verifies (needs-verification #9), quote it here — pseudopeople's PyPI installs run roughly two orders of magnitude above the access requests for its gated state/national files — as the sharpest single piece of evidence for the hedge.
- **Do not mention "GeCo3"** — it is an unrelated DNA compressor. Do not name commercial vendors; the digest marks that as an unverified negative. And note the positionality edge: the uptake-barrier judgment is the author assessing his own project's access process — §4.4's positionality sentence must cover it.

### 1.4 Objective, and the sources this resource is built from — ¶2 (~180 words)

- The objective sentence, close to the author's outline wording because it is the paper's thesis: we set out to make an extremely low-barrier dataset for record-linkage research and development at the scale of the Florida cancer registry's typical linkage challenge — a direct download with a DOI, no application, no approval, and a published ground-truth key.
- The author's tension sentence (2026-08-09), one clause, planted here and delivered in §4.4: even though the data are fake, they look real enough to risk doing harm — valid-looking SSNs, synthetic-identity seed material, addresses that must not be geocoded.
- Close the Background with the sources overview the genre requires, one sentence each: the **pseudopeople simulated US population** — an individual-based microsimulation initialised from American Community Survey public-use microdata, carrying `simulant_id` as ground-truth identity across all its observers [@haddock2024simulated; @pseudopeople_software]; **GBD neoplasm-prevalence estimates** for Florida by age and sex, the sampling weights (§2.2); and **FCDS's published submission layouts**, the design template for the schema and the deterministic rules [@fdoh_fcds_procedure_guide_2007; @fcds_linkage_layout].
- What the paper reports, in the author's tripartite order: (1) the data resource — a prevalence-weighted registry stand-in and two finder files with exactly known overlap; (2) the process of its development — the seeded, checksummed pipeline, targeted error injection at rates **plausible for this transaction** (not "chosen to reflect registry practice", which nothing verified supports), and the trim bug that scoring against the ground-truth key caught before release; (3) a difficulty portrait and demonstration usage — quasi-identifier uniqueness, data forensics, and deterministic baselines overall and stratified by race/ethnicity (§3.3–§3.4).
- Still deliberately *not* re-quoting the counts that Results owns — the exact overlaps and file sizes stay out of the Background entirely. The generalisation sentence (illicit-drug epidemiology, social work, economics) stays in §6; it duplicated the planned Conclusions.

---

## 2. Methods

*Target ≈ 850 words across five subsections — the Data Resource Profile asks Methods to detail the original sources, the linkage methods, and the study population. The author's outline prompts map as follows: "approach to getting age structure right" → §2.2; "approach to ensuring specific overlaps" → §2.2 (the stratified trim); "approach to setting noise levels" → §2.3; his proposed Methods table of the three files is folded into Table 1 (Results), which shows targets and realised values side by side. Load order: `paper.qmd` must open with a setup chunk reading `config.yaml` into `cfg` and the `results/` summaries into `lb`, `pop`, `err`, `rel`, `forensics`, `strat` before any inline expression resolves.*

### 2.1 Source population and the Florida extract — ¶3 (~220 words)

- The simulation is described in detail elsewhere [@haddock2024simulated; @pseudopeople_software]; give the author's own brief (2026-08-09), reconciled with the published description (needs-verification #7): a population initialised with the size and demographics (age, sex, household structure) of the 2020 United States from publicly available American Community Survey and 2020 Decennial Census data; mortality, fertility, and mobility modelled over twenty years from those sources and the Global Burden of Disease Study; and fully simulated versions of the confidential fields linkage runs on — names, dates of birth, addresses, SSNs — recorded for use with the pseudopeople Python package. The underlying large-scale populations are available through a lightweight approval process [@keyes2026governance]. Record the artifact name `pseudopeople_simulated_population_usa_2_0_0` (not the internal `release_02_yellow` tag), the Vivarium microsimulation `vivarium_census_prl_synth_pop` with `simulant_id` as ground-truth identity across all observers, the pseudopeople package version, and DuckDB `{python} duckdb_version`.
- The friction narrative, in the author's voice and with numbers behind it: using the full-USA data was possible but slow, and even pseudopeople's existing affordances for loading a single state with distributed computing were a barrier — so we built a Florida-only extract with DuckDB, using AI-assisted coding by Claude (disclosed here and in the back-matter AI Disclosure). The three-way load benchmark in §3.1 is the evidence; without those numbers this paragraph makes no claim. What stays true and verified about the affordances (pseudopeople 1.2.8): `generate_decennial_census` *does* take `state=`/`year=` and has a Dask engine — never claim otherwise, the author is a pseudopeople co-author and a reviewer will catch it; `generate_social_security` has **no** `state` parameter, so the SSN join is by hand; and there is no API for prevalence-weighted or overlap-controlled sampling, which is the whole cohort design.
- Extraction mechanics: DuckDB reads the census-observer Parquet directly, filters `state = 'FL'` and `year = 2020` from `config.yaml`, deduplicates with `QUALIFY row_number() OVER (PARTITION BY simulant_id) = 1`, yielding `{python} fl_simulants` simulants. SSNs come from the Social Security observer joined on `simulant_id`; `race_ethnicity` is carried through from the census observer into the released schema (new in v0.3) — FCDS's own submission layout carries race, so the column is transaction-faithful, and it is what §3.3–§3.4's stratified statistics stratify on.
- Two-tier note: this is pipeline-tier code run manually; nothing in the rendered paper executes it. The benchmark numbers replace conjecture — no unmeasured "cannot load even one state" claims.

### 2.2 Cohort design and reproducible sampling — ¶3 (~180 words)

- Design in one paragraph, targets from `config.yaml`: a registry stand-in targeting `{python} cfg_registry_target` records sampled with probability proportional to age- and sex-specific cancer prevalence, and two finder files targeting `{python} cfg_finder_500k_target` and `{python} cfg_finder_100k_target` records with `{python} overlap_500k_target` and `{python} overlap_100k_target` overlapping simulants. Weights are GBD all-neoplasm prevalence for Florida, 2021, mean over 1,000 draws, 22 age bins by sex, committed as `reference/gbd_neoplasm_prevalence_florida.csv`; range `{python} gbd_prev_min`% (males under 1) to `{python} gbd_prev_max`% (males 95+). **The file stores percentages** — format with `:.1f` and a literal `%`, never `:.0%`.
- Why prevalence and not incidence, in two sentences only (condensed from four bullets): a registry accumulated over decades holds everyone living with or having had a diagnosis, so its composition follows prevalence; incidence is the right comparator for the *shape* check in §2.4. Drop the unverified conjectures about "name eras" and "address stability" — the sufficient rationale is matching the registry's age/sex structure to Florida cancer demography.
- **Add the load-bearing fact all five drafts omitted:** overlap members are drawn from the registry cohort and the remainder from outside it via separate hash streams, and the two files are then noised *independently* (`psp_registry` seed `{python} cfg_seed_registry`, `psp_finder` seed `{python} cfg_seed_finder`). That independence is what makes this a linkage problem rather than a join.
- Reproducible randomness, **stated once here and not restated in the Discussion**: DuckDB's `random()` is not reproducible across threads, so every draw is made a pure function of the record key — the Efraimidis–Spirakis exponential-race key with the uniform replaced by a keyed hash. Quote the expression exactly, including the constant `18446744073709551617.0` (= 2⁶⁴+1); the Discussion draft's "2^64" is a paraphrase, and a section whose claim is bit-identical checksums cannot paraphrase the formula that produces them. Five salts give independent streams from seed `{python} cfg_seed_sample`.
- **Add the most reusable pattern in the pipeline, which no draft stated:** row-level omission noise deletes rows, so exact targets are unreachable in one pass; cohorts are drawn at `{python} cfg_oversample`× target and trimmed back afterwards with `numpy.default_rng({python} cfg_seed_postprocess)` over sorted ID lists. The trim must be *stratified* — exactly the target number of overlap members, filler drawn from survivors outside the entire overlap pool, the registry keeping only the chosen members (`stratified_trim` in `src/simulated_data_for_fcds_scale_rl/downsample.py`, unit-tested in `tests/test_stratified_trim.py`). The v0.2 build trimmed unstratified and overshot its overlap targets by a third; §3.1 tells that story in two sentences as evidence the ground-truth QA loop works. Note the reason for oversampling is that the number dropped is *not known in advance*, not that noise is nondeterministic (it is seeded and deterministic; that determinism is the point of §2.2's row-order fixes).
- The two silent order-dependence bugs, one sentence each: the staged Parquet must be written `ORDER BY simulant_id` because pseudopeople walks rows in file order, and the SSA join must be sorted before numpy selection. The run-twice assertion moves to `tests/`, mentioned in half a sentence; `lst-weighted-sample` is cut.

### 2.3 Noise, schema and packaging — ¶2 (~80 words)

- Base layer: pseudopeople's full default suite (omission, non-response, duplication; typos, OCR, phonetic, nicknames, fake names, month/day swaps, wrong digits, blanks). Targeted overrides from `config.yaml`, values never typed: finder files `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` SSN transposition, `{python} cfg_finder_address_missing` on each address field; registry `{python} cfg_registry_ssn_missing` / `{python} cfg_registry_ssn_transposed` / `{python} cfg_registry_address_missing`. Rationale in one clause: a researcher's finder file is dirtier than a certified registry's consolidated file. **The provenance of these rates is unresolved** — `config.yaml` credits an unread "FCDS 2024 monograph"; until confirmed, describe them as author-chosen and plausible, anchored to published registry figures [@qiao2023lexisnexis].
- Adjacent-digit SSN transposition is not in pseudopeople's noise taxonomy, so it is a post-hoc numpy step — the concrete affordance gap §4.1 generalises.
- Published columns: `simulant_id` plus first name, middle initial, last name, date of birth, sex, street number, street name, unit number, city, state, ZIP, SSN, and (from v0.3) race/ethnicity. Say the release covers **all fields required by either minimum matching rule, plus race** — not "exactly the fields FCDS requires", since the current submission layout also carries maiden name, full middle name, alias and birthplace. `tbl-schema-layout` is cut as repo documentation.
- Deterministic archive: zip built with `-X` and fixed member timestamps so archive metadata is deterministic; checksums published for the three CSVs and the bundle. Dataset version `{python} dataset_version`; `config.yaml` is the single source of truth.

### 2.4 Quality assurance and the linkage baseline — ¶2 (~90 words)

- QA check 1, external scale: the extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents (a cited literal — **needs a Census Bureau citekey**).
- QA check 2, registry demography: the realised age/sex composition of the registry cohort against the GBD weights, and — *if and only if the provenance is confirmed* — against published FCDS incidence rates by age group. `reference/fcds_incidence_by_age_sex.csv` carries "PROVENANCE — NEEDS CONFIRMATION BEFORE PUBLICATION" in its own header; if it cannot be confirmed, that panel is dropped and the QA claim narrows to weights-vs-realised. Say which happened.
- Define passing so it is falsifiable, and **do not use monotonicity**: verified against the committed file, female prevalence peaks at 21.84% in the 85–90 bin and dips at 90–95, and male prevalence dips between ages 2 and 15, so "rises monotonically with age" is falsified by the paper's own inputs. The criterion is agreement in peak band and in the male/female crossover, not in level — the registry is prevalence-weighted while FCDS publishes incidence.
- Baseline: each rule is agreement on every key of a key-set, evaluated as DuckDB hash joins (disjunctions as UNIONs, avoiding a nested loop over ~5×10¹¹ pairs). Do not enumerate the ladder in prose — that is the Results table. Metrics: precision and recall, reported also as false-match and missed-match rates after Lam et al. [@lam2024synthetic]; F1 is computed but not used to rank, per the F-measure critique [@hand2018fmeasure]; specificity and accuracy are omitted because true non-matches grow quadratically [@christen2007quality]. Deterministic linkage is a legitimate floor, not a straw man — the distinction from probabilistic methods is largely one of implementation [@doidge2018demystifying], and SEER–Medicare runs a deterministic algorithm in production [@enewold2020seermedicare]. **Do not import SEER–Medicare's ~96% as a linkage-accuracy figure** — it is the share of SEER persons 65+ found in Medicare enrolment.
- **Cut from Methods entirely:** the headline-foreshadowing bullet (those numbers appear once, in Results) and the "optional, not yet run" linked-vs-unlinked extension.

### 2.5 Characterising the data: forensics and difficulty — ¶1 (~90 words)

- Define the measures once, here; Results reports the numbers. **Cut 2026-08-09: the m/u-probability table** — the author rules the Fellegi–Sunter framing a distraction from the paper's point; nothing may reintroduce it. (1) **Quasi-identifier uniqueness**: the share of registry simulants unique on first+last name+DOB, on last name+DOB, and on ZIP+DOB+sex, plus the count of distinct simulants sharing a full name. (2) **Data forensics**, per the author's outline: most common first and last names (stratifier per decision #17); per cent of dates blank, and of non-blank dates that fail to parse; sentinel checks — "John Doe"-pattern names, repeated-digit SSNs such as 111-11-1111, SSNs violating SSA issuance rules. (3) **Stratified baselines**: the §2.4 ladder recomputed within `race_ethnicity` strata. Noise injection is race-uniform by design, so any differential is inherited from population structure — chiefly the race/ethnicity-conditioned surname sampling of the source population [@haddock2024simulated]; the fidelity caveats live in §4.2. (4) **Blocking feasibility**: candidate-pair counts and ground-truth pairs-completeness under blocking on full DOB and on last-name initial plus birth year.

---

## 3. Results

*Target ≈ 1,100 words. Genre spec: "a detailed description of the dataset created including its structure, characteristics (e.g. demographic, clinical, social) and data quality." The pivot (2026-08-08): Results is a **difficulty portrait**, not an inventory plus confessions — every number here should predict something about a user's experience. Four subsections: structure, population characteristics, error structure, linkage difficulty.*

### 3.1 Structure, contents, and where the data are held — ¶2 (~200 words)

- One paragraph plus **Table 1**: three CSVs deposited on Zenodo under a DOI; rows and distinct simulants per file; designed overlaps hit exactly (v0.3) with the finder files disjoint; sizes; MD5 and SHA-256. The extract of `{python} fl_simulants` simulants is `{python} fl_share_census` of the official 2020 Census count.
- The registry holds `{python} registry_rows` rows for `{python} registry_simulants` distinct simulants; the `{python} registry_dupe_rows` excess rows are within-file duplication. **Mechanism verified on v0.2** (re-measure on v0.3): duplicated simulants appear on two rows that *differ in content* — noised independently — which is pseudopeople row-duplication noise and the realistic case of a registry holding two differently transcribed reports on one patient. Say this as a measured fact, and note it is why a true-pair count can exceed a distinct-simulant count; **define overlap once** — distinct simulants in both files — and report the pair count (`{python} overlap_500k_pairs`) separately as the recall denominator (§3.4).
- Two sentences of quality provenance the genre rewards: the v0.2 build's unstratified trim overshot its overlap targets by roughly a third and left the finder files sharing 2,508 simulants before scoring against the ground-truth key caught it; the released build trims stratified (§2.2) and hits every design target exactly. Checksums let a user prove the file they hold is the file profiled here — state honestly how many independent regenerations were compared; if only one build exists, write "we record checksums so reproducibility can be checked", not "reproducibility is demonstrated".
- The three-way load benchmark, the author's addition (2026-08-09): wall time and peak memory to load the full USA via pseudopeople, Florida via pseudopeople's `state=` filter, and Florida from the staged extract — measured once each with the node spec recorded, from `results/environment.json`. These numbers justify the extract's existence (§2.1) and quantify the friction the Background claims; without them neither section may make the claim.

### 3.2 Population characteristics — ¶3 (~300 words)

- Open with the plain descriptives the author listed (2026-08-09): mean age, sex ratio, and race/ethnicity fractions per file — one sentence each, from `results/registry_age_sex.csv`.
- Age and sex: realised composition of **all three released files** against the GBD weights and the simulated Florida population, split by sex (**Figure 1**, per the author's spec). The pass criterion is agreement in peak band and in the male/female crossover, not in level — the registry is prevalence-weighted while FCDS publishes incidence; the optional incidence panel appears *only if* the `reference/fcds_incidence_by_age_sex.csv` provenance is confirmed (§2.4). Say which happened. (That file is "the age pattern Anders provided" from the author's outline — his own uncertainty about what it is *is* the provenance problem, decision #7: if it cannot be explained, it cannot be used.)
- Clinical characterisation, carefully scoped: the resource carries no tumour variables, so the "clinical" description the genre asks for is the cancer-prevalence weighting itself — GBD-based, age/sex only — and the registry-vs-weights comparison. Name the author's open question as decision #16: the stand-in samples *living* 2020 residents, while a real registry accumulates deceased cases; state the living-prevalent scope as a deliberate choice here and a limitation in §4.2.
- Race/ethnicity (new in v0.3): composition of the registry and finder files by `race_ethnicity` against the simulated Florida population (**Figure 1 panel or a one-row table**). State plainly, here and again in §4.2: the sampling weights are age/sex only, so the registry's race/ethnicity mix is inherited through age–race correlation in the population, not modelled — race/ethnicity-specific cancer prevalence is *not* represented.
- Households in one sentence: family members share surnames and addresses by construction of the source population, so address- and surname-based blocking meets realistic co-residence collisions [@haddock2024simulated].
- What the data look like: **Table 2** — the same simulant as it appears in the registry and in a finder file, `simulant_id` printed so the reader can verify, discrepant cells marked, noise mechanism named per row; two or three pairs showing a nickname or typo, a transposed SSN, and a blanked field. Name the fidelity giveaways in the same breath (lowercased addresses, `city = "unincorporated"`, a 2019-born person in a 2020 extract) — linkage-relevant, and users must be told; cross-reference §4.2. Add the author's address warning here as fact and in §4.2 as caveat: pseudopeople addresses are deliberately **not real addresses**, so running them through geocoding tools yields failures or fictitious hits — a surprise users must be spared [@pseudopeople_software].

### 3.3 Error structure — ¶2 (~300 words)

- Realised noise rates per targeted field per file against their `config.yaml` targets, folded into Table 1's columns. The one deviation narrated in prose is the SSN floor: realised registry missingness `{python} registry_ssn_missing` against the `{python} cfg_registry_ssn_missing` target, because `{python} pop_ssn_never` of Florida simulants never held an SSN in the source population and the pipeline warns rather than blanking further (**two distinct variables** — population rate vs registry-measured rate; never render "5.77%" as a literal). Arguably more realistic than the target: the New York State Cancer Registry reported 3.4% of 1.4M records lacking SSN [@qiao2023lexisnexis].
- The mechanism sentence that pre-empts a "bug" report: missingness is set by target *count*, not an independent Bernoulli draw — the finder files' structural rate sits below their 20% target so the pipeline tops them up to *exactly* 20%, while the registry's structural rate already exceeds its 5% target so nothing further is blanked. One mechanism, two outcomes.
- **Table 3 — most common names** (first and last; stratifier per decision #17): top-10 lists with counts. Reader-friendly fidelity evidence, and the visible mechanism behind both the uniqueness statistics and any stratified differential in §3.4 — common surnames are where exact-match precision goes to die. (Replaces the cut m/u table, 2026-08-09.)
- **Forensics, one sentence each, from `results/forensics.json`** (the author's checks, 2026-08-09): per cent of dates of birth blank, and per cent of non-blank dates that fail to parse; count of "John Doe"-pattern names; count of repeated-digit SSNs (e.g. 111-11-1111) and of SSNs violating SSA issuance rules. Frame as *published sentinel checks*: a real file would flunk some of these; say plainly which this file flunks and which it passes.
- Stratified error rates: per-field missingness and true-pair disagreement by `race_ethnicity` — the descriptive layer under §3.4's stratified performance. Note in one clause that noise injection is race-uniform by design, so differentials here are population-inherited, not configured.

### 3.4 Linkage difficulty — ¶3 (~350 words)

*For the author — what the ladder is, and what it costs to explain (2026-08-09). Each rule is one or two **field-sets** (e.g. {first name, last name, DOB}, or {first name, last name, SSN, sex}); a registry-row × finder-row pair is a **predicted match** if it agrees exactly on every field of at least one of the rule's field-sets. Each field-set is one DuckDB hash join (a two-field-set rule becomes a UNION of two joins), so the whole ladder runs in seconds rather than touching the ~5×10¹¹ possible pairs. Because every row carries `simulant_id`, each predicted pair is definitively true or false, giving exact precision and recall (equivalently false-match and missed-match rates) per rule. Exposition cost in the paper: Table 4 plus ~180 words of narration (the walk down the ladder in the second bullet) plus ~60 words of honest relabelling — about 250 words all-in. The code exists (`pipeline/linkage_baseline.py`), the v0.2 numbers are already in hand, and a full run takes ~9 seconds.*

- Quasi-identifier uniqueness first, because it sets expectations for everything below: the share of registry simulants unique on first+last name+DOB, last name+DOB, and ZIP+DOB+sex, and the number of distinct simulants sharing a full name. One sentence ties it to the ladder: exact name+DOB collisions between *different* people are what cap that rule's precision below 1.
- **Table 4** — the deterministic ladder, and its narration. Framing: demonstration usage (§1.4) — the resource discriminates between strategies and publishes a floor. Name+DOB reaches precision `{python} r500_name_dob_precision` but misses `{python} r500_name_dob_missed` of true pairs; SSN alone is near-perfect on precision (`{python} r500_ssn_only_precision`) yet misses `{python} r500_ssn_only_missed` because a fifth of finder SSNs are blank; the exact-agreement rule on FCDS's name+SSN+sex field set makes no false matches but finds only `{python} r500_fcds_min_ssn_recall`, while the month/year variant admits `{python} r500_fcds_min_monthyear_fp` false matches; taking either raises recall to `{python} r500_fcds_either_recall`; the best simple rule, name+DOB or SSN, reaches `{python} r500_best_recall` at `{python} r500_best_precision`; a deliberately under-specified last-name+DOB rule collapses to precision `{python} r500_lastname_dob_precision`, showing the benchmark punishes weak keys.
- **Relabel the FCDS rules honestly.** These are exact-agreement rules on FCDS's minimum *submission* field sets — rules about which identifiers a submitter must supply, not about which fields must agree for a match, and FCDS itself matches probabilistically with clerical review. Presenting a conjunctive join as "FCDS's rule" is a straw man. State the vintage of each field set.
- **Figure 2 (or a Table 4 panel) — the equity result:** recall and precision of two or three headline rules stratified by `race_ethnicity`. Motivate with the differential-linkage-error literature [@mcgrathlone2021ethnicbias; @lam2024synthetic]. **Do not assert the direction before computing it.** The mechanism to test: surname concentration differs by group in the race-conditioned source lists, so collision-driven precision loss should differ; if the computed differential is null, report the null — it is informative either way (decision #15).
- Comparator, one clause: name+DOB-style deterministic rules on real data link 88–93% with 97–99% correct [@li2006deterministic], so the simulated difficulty sits in a realistic band.
- Blocking feasibility in two sentences: the naive comparison space is ~5×10¹¹ pairs; blocking on full DOB yields `{python} pairs_block_dob` candidate pairs retaining `{python} completeness_block_dob` of true pairs (and one more key, per §2.5) — the first numbers any probabilistic user needs for compute planning.
- Cost of evaluation: the full ladder runs in `{python} baseline_seconds_500k` seconds on the 500k finder. **Record the node spec** alongside the timing or drop "on a single node". Note the 100k finder gives materially the same metrics in one sentence; its panel is cut. Say what is *not* here: no normalised/blocked variant of the ladder, no probabilistic run — named once as remaining work (§6's ongoing improvements).

---

## 4. Discussion

*Target ≈ 750 words, four subsections. Genre spec: strengths and limitations, projects currently using the dataset, and suggestions for how other researchers could use it. The comparator survey lives in §1.3; the reproducibility mechanism lives in §2.2; the old standalone Limitations section merges into §4.2; access mechanics move to §5 Data Access. Only the 95.6%-vs-59.8% gap survives as a re-quoted figure. A Discussion of this length owns zero figures and zero tables.*

### 4.1 Strengths, and the engineering lessons in one paragraph — ¶2 (~160 words)

- Strengths in two sentences, without re-quoting numbers: state scale with the age/sex demography of cancer; exact ground truth; zero-barrier access; determinism verified by published checksums. Each is claimed once here and argued elsewhere — a summary, not a reprise.
- The composition pattern, stated so a reader can reuse it: do the heavy relational work (filter, dedupe, SSA join, weighted sampling) in out-of-core SQL, stage the result as a Parquet directory mimicking the source layout, and point the simulator's `source` at it. The two tools compose through the filesystem. Treat the simulator as one stage of a pipeline you own, not as the pipeline — which is also why the bespoke SSN-transposition step was cheap to add.
- The reproducibility lesson in two sentences, no mechanism restated: **a seed pins the random stream, not the pairing of stream to rows.** Any pipeline whose row order is not contractually fixed can pass every unit test and still be irreproducible; simulation tools should document their row-order sensitivity. This generalises to any parallel engine because it removes the RNG from the engine entirely.
- The Dask comparison, honestly scoped. Keep it **qualitative**: DuckDB is single-node and SQL-only; Dask and Spark buy horizontal scale-out and arbitrary Python at the cost of orchestration and worker tuning [@person_linkage_case_study]. **Delete** the assertion that the prior project suffers "non-deterministic partition/row ordering that fights reproducibility" — it is an unsupported negative characterisation of a named colleague's repository, and even the authorship attribution is an inference the author must confirm. **Delete** the 8.7-second figure from this paragraph: that is the downstream linkage timing, not the build, and says nothing about whether a 21M-simulant construction fits one node. Either report the construction wall time, peak RAM and node spec, or make no scale claim. Note that Splink runs on a DuckDB backend, so the same engine serves construction and the experiments the dataset is for [@linacre2022splink].

### 4.2 Fidelity and limitations — ¶3 (~350 words; merges the old standalone Limitations section)

- The argument that licenses the simplification: for a *linkage* benchmark, difficulty is set by the joint distribution of the identifying fields — name frequency spectra, DOB collision rates within blocks, household co-residence, field-level error and missingness. Age enters only through those channels. The last-name+DOB rule's precision of `{python} r500_lastname_dob_precision` is the mechanism made visible, and it is inherited from the source population's demographically structured names and households, not from the cancer weighting.
- Where the argument breaks down, stated before a reviewer states it: if linkage error interacts with age- or ancestry-specific name structure, a mis-shaped mix changes measured *rankings*, not just error levels [@mcgrathlone2021ethnicbias]; the source draws first and last names independently and floors name frequency at public-list thresholds, so the rare-name tail is thinner than reality [@haddock2024simulated]; and missingness here is largely at random within targeted fields, whereas real registry missingness is differential.
- Anchor the tolerance: synthetic identifiers reproduced real linkage-quality estimates within fractions of a percentage point at small scale [@lam2024synthetic] — evidence that ranking and stressing methods tolerates fidelity gaps that inference would not [@ruggles2025shortcomings].
- **Identity resolution only.** No tumour site, histology, stage, diagnosis date or treatment; no natural history of cancer — the resource exercises finder-file-to-registry *identity* matching, not tumour consolidation or death clearance. And the gap that matters more to a registry audience: the registry is essentially one row per person, so within-file duplicate detection — the central registry task, the one NAACCR certifies at under 0.1% for Gold [@naaccr2026certification] — is not exercised at all.
- **Imperfect fidelity may mis-rank algorithms.** If a load-bearing feature of the real problem is absent — differential missingness, name change at marriage, first/last name dependence, the thin rare-name tail, all documented gaps of the source population [@haddock2024simulated] — package comparisons here could rank tools differently than production data would. That is the one error this resource must warn its users against: treat results as necessary, not sufficient, and validate winners in situ [@alexandersson2024comparing].
- **Race/ethnicity caveats, stated next to the equity results they qualify (§3.4):** first names are not race-conditioned in the source population, noise injection is race-uniform, and no race-differential data quality is modelled — so the stratified differentials measure name-structure effects only, and real-world differential error is plausibly larger.
- **Disease is a bolt-on, not integrated into the simulation** (the author's own characterisation, 2026-08-09): cancer status alters neither mobility nor mortality — a cancer patient and a healthy simulant of the same age, sex and race/ethnicity behave identically — so survivorship structure is absent. The related scope choice (decision #16): the registry stand-in holds living 2020 residents only, where a real registry accumulates deceased cases; cross-reference the identity-resolution-only bullet's death-clearance gap.
- **Household dynamics are simplistic:** when only part of a household moves, it is always a single person who moves to a new household or joins an existing one as an "other nonrelative" — **verify against the simulation code before print** (needs-verification #8). And the schema carries **no phone numbers or email addresses**, fields real linkage workflows increasingly rely on.
- **Addresses must not be geocoded:** they are deliberately not real addresses (§3.2); a user who geocodes them gets failures or fictitious locations.
- **Known construction imperfections that remain:** the SSN-missingness floor (§3.3 — the config parameter is a target the pipeline can only move realised missingness *up* to, never down) and the visible artifacts (§3.2: lowercased addresses, "unincorporated", the 2019-born infant). One consumer-facing defect worth a clause because it will bite the first user: the CSVs quote the rare comma-containing field (a `street_number` of `"64,66"` appears in `finder_100k.csv`) seldom enough that DuckDB's CSV sniffer infers no quote character and then fails to read the file — anyone loading the release must name the quote character explicitly; shipping Parquet alongside CSV in a future version removes the whole class of problem.
- **Prevalence is not reportable incidence.** GBD all-neoplasm prevalence is not registry-reportable incidence, and the case mix is validated only at the age/sex shape level, with race/ethnicity-specific prevalence explicitly not modelled (§3.2). **Delete** the unsupported clauses "includes benign neoplasms and long-past cases" — nothing verified establishes what the GBD neoplasms envelope contains.
- **Locale and vintage.** Names, addresses and households are USA-circa-2020, and name distributions transfer poorly: GeCo required structural forking for Brazilian composite and multiple family names [@trentin2018brazil]. Conclusions about name-comparator choice do not port to Brazil, Australia or non-Latin-script registries, and any ethnic-bias finding reflects US-2020 name structure only [@mcgrathlone2021ethnicbias].

### 4.3 Uses: demonstrated, current, and suggested — ¶1 (~140 words)

- Demonstrated in this paper: the deterministic ladder doubles as a worked example — a user can reproduce Table 4 from the deposit and the archived code before trusting their own harness.
- Current and adjacent use, stated precisely because no external project uses *this* deposit yet: FCDS's monograph programme ran on privately supplied pseudopeople data and formally recommended a public corpus [@alexandersson2023splinkfcds; @alexandersson2024comparing]; this resource responds. The invitation doubles as the decisive external-validity test (moved here from the old Conclusion): FCDS re-running its package comparison on this corpus and reporting rank agreement with its internal results.
- Suggested uses, in the author's terms first: cancer-registry analysts comparing alternative linkage solutions, and algorithm developers benchmarking methods and evaluating new directions without the overhead of access to confidential data on real patients. Then one clause each: regression-testing in continuous integration, which gate-free access makes possible at this scale for the first time; differential-linkage-error and blocking research [@mcgrathlone2021ethnicbias]; and evaluating synthetic-identifier generators against a common target [@lam2024synthetic].
- **The monitoring plan — the author's addition (2026-08-09), and the paper's empirical bite:** we will monitor download volume of these files and compare it with (a) PyPI installs of pseudopeople itself (smaller but more flexible linkable files, zero overhead) and (b) access-request counts for the gated Rhode Island and full-USA populations. The working figure — requests roughly two orders of magnitude below installs — is needs-verification #9. This turns the Background's "appears to be a barrier" hedge into something the release itself will test (§6).

### 4.4 Why open release, and what it risks — ¶2 (~120 words)

- **Fix the provenance argument.** Do not call ACS PUMS "public aggregate statistics" and do not claim "no real person's record contributed". PUMS is individual-level public-use microdata of real households, sampled to initialise the simulation. The defensible argument runs through PUMS's own disclosure protections (already released, de-identified, swapped, top-coded) plus the fact that there is no confidential dataset fitted to and therefore no membership to leak — which is what distinguishes this from the generative-model threat model that membership-inference attacks target [@stadler2022groundhog]. Under the regulator's test the question becomes coincidental resemblance, not identifiability [@ico2023pets].
- Name the residual risk: coincidental generation [@suchow2023coincidental]. With tens of millions of simulated Floridians some name+DOB+city combinations will match real people by chance. Weigh against it that every name is a recombination of names each shared by many real Americans by construction of the public source lists [@haddock2024simulated].
- **Argue the benefit case against the right counterfactual, in step with §1.3.** The Background asserts that even a lightweight approval step appears to deter uptake; this subsection owes the mechanism, not a re-assertion. The existing pseudopeople gate is a public, logged GitHub request under a relational-governance process [@keyes2026governance] — inverting the risk calculus against *real registry data* instead is a false dilemma. State who the gate actually excludes: CI systems and containerised reproductions cannot open an issue; classroom and workshop use at scale; and a fixed, checksummed artifact makes *this paper's own results* reproducible in a way a re-request cannot. These are the concrete referents behind §1.3's uptake clause — cross-reference them, do not repeat them.
- Guardrails as a short list: provenance documentation, determinism plus published checksums, a DOI deposit with versioning and a tombstoned withdrawal path [@zenodo_policies], prominent "simulated data" labelling, and a stated objection route — put with the author's honesty (2026-08-09): if someone objects to a simulated likeness of their name, *we have less recourse* than a controller of real data would. **Present the objection route as an untested proposal, not a novel contribution.** Changing the sampling salt re-draws *which* simulants are selected; it does not regenerate the names attached to a given simulant, so a complainant's name can reappear — and it destroys comparability with every published result on v0.2. If a mechanism is promised, it must be targeted suppression plus a tombstoned version bump, and it must actually be implemented on the deposit. Say "we are not aware of a comparable project that states one", which is what the evidence supports.
- **Add one sentence of positionality.** This section assesses the ethics of the author's own simulator, using his own governance framing, motivated by a monograph recommendation that names him personally. The reframed Background raises the stakes: §1.3's claim that the pseudopeople gate deters uptake is the author assessing his own project's governance, so the positionality sentence must cover the Background as well as this section. Acknowledging that pre-empts a reviewer raising it less charitably; the COI statement carries the rest.
- **Add the exposure no draft mentioned:** the files ship syntactically valid SSNs alongside full name, DOB and address. A released SSN can collide with a real issued number, and the corpus is usable as synthetic-identity seed material. The labelling guardrail should name the risk it mitigates, and contamination of a real registry system by simulated records should be raised.

---

## 5. Data Access

*Target ≈ 150 words. A required section for this genre — the paper's thesis made operational — and it feeds the Data Availability Statement.*

- Where: the Zenodo deposit — dataset DOI and version (run-list item 10) — with the pipeline archived under a code DOI and the repository linked.
- How: direct download; no application, no approval, no registration, no data-use agreement. Licence per decision #9 (CC0 recommended). Published MD5/SHA-256 checksums verify the download; `config.yaml` in the archive records every seed and target.
- Versioning and redress: versioned deposits with a tombstoned withdrawal path [@zenodo_policies]; the objection route presented as an untested proposal (§4.4); prominent "simulated data" labelling on the deposit landing page, naming the synthetic-identity-seed risk it mitigates (§4.4).
- Contact: the corresponding author, repeating the collaboration invitation from Key Features once.
- At submission: IJPDS requires the dataset DOI plus a private reviewer URL; the Data Availability Statement (§7) uses the journal's "openly available in a public repository" wording, with repository name, DOI, and no access restrictions to declare.

## 6. Conclusions

*Target ≈ 120 words, ¶1.*

- What exists now, in one sentence, close to the author's wording: a set of simulated data files for testing record linkage in the size and shape of the challenges faced by the Florida state cancer registry — direct download, DOI, no application or approval, published ground-truth key, deterministic baselines.
- The experiment framing, from the author's outline, as the second sentence: we made this openly available *to see whether* the lightweight request process for state- and national-scale pseudopeople data has been a barrier to uptake — we expect more use by people who need more volume than pseudopeople ships openly but lack the time to request the gated files; §4.3's monitoring plan is how we will know.
- Implications of use, one sentence: results on this corpus are necessary-but-not-sufficient evidence about production performance — validate winners in situ (§4.2) [@alexandersson2024comparing].
- Generalisation, kept: the transaction this dataset is shaped like — a government-held population-scale file, a researcher cohort, a minimum-identifiers rule, no shareable ground truth — recurs in vital statistics and drug-epidemiology cohort follow-up, and beyond health in social work and economics. One clause closes the loop with §1.1: wherever that transaction recurs, the binding constraint on linkage research and development is access to realistic test data, and the pattern here — simulate at scale, publish without a gate — transfers even where this dataset does not.
- Ongoing improvements, one sentence, because the abstract's Conclusion promises them: Parquet distribution alongside CSV, probabilistic (Splink) baselines, and community-contributed rule submissions. Close with the author's invitation, verbatim: *let us know what you find!*

## 7. Required back-matter statements

All mandatory per the guidelines the author supplied (2026-08-08); one drafting note each.

- **Acknowledgments:** thank Anders Alexandersson by name only with permission (decision #14). Acknowledge the US Census Bureau for making the underlying population possible — but **rephrase the author's draft** ("regret that they got too busy to continue cooperating in our cooperative agreement" will read as a dig at a federal agency in print): e.g. acknowledge support under cooperative agreement CB21RMD0160001 and note the agreement concluded before this work; exact wording is the author's call (needs-verification #10 for the agreement number's applicability).
- **Ethics Statement:** state that ethical approval was not required and why — fully simulated data, no human subjects or participants; the source population derives from public-use microdata carrying its own disclosure protections (§4.4).
- **Conflict of Interests Statement:** ICJME form; disclose that the author built pseudopeople, co-authored the source population, helps govern access to it, and is named personally in the monograph recommendation (decision #10 — recommended: disclose).
- **Publication Consent:** written acknowledgement of consent to publish and openly share the data — author-generated simulated data, so the author grants it; one sentence.
- **Funding Statement:** grant or "no specific funding" (decision #13); distinguish this work from the source population's Gates INV-060835 and Census CB21RMD0160001 funding; note salary sources if the funder requires.
- **Data Availability Statement:** placed just before References; the journal's open-repository wording with repository name, DOI/URL and reference number; no access restrictions to state.
- **Abbreviations:** compile at draft time — at minimum FCDS, SSN, DOB, GBD, ZIP, CSV, DOI, ACS, PUMS, NAACCR, IJPDS.
- **References:** Vancouver style with bracketed numerals in the text and DOIs for every entry that has one — verify `ijpds.csl` renders `[1]`-style brackets; include URLs where available.

---

## Figures, tables and code listings

Seven essential items plus one optional — the Data Resource Profile's length carries the forensics table (Table 3) and the stratified figure (Figure 2). Everything else proposed across the five drafts stays cut; the cut list is at the end of this section so the decisions are visible rather than silent.

| Label | Kind | Caption | What it shows | Produced by | Status |
|---|---|---|---|---|---|
| `tbl-release` (Table 1) | Table | The released files: contents, designed and realised overlap, targeted versus realised error rates, size and checksums. | Rows: `registry.csv`, `finder_500k.csv`, `finder_100k.csv`, bundle `.zip`. Columns: rows; distinct simulants; overlap target and realised (equal by construction in v0.3; pairs footnoted); SSN missing target/realised; street-name missing target/realised; size (MB); MD5 + SHA-256. Merges three separately proposed tables and absorbs `tbl-error-rates` as four columns. | `paper.qmd` chunk over `results/release_manifest.json` + `results/error_rates.json` + `results/linkage_baseline.json` + `config.yaml` | **Essential** |
| `fig-registry-age-sex` (Figure 1) | Figure | Realised age/sex and race/ethnicity composition of the simulated registry against the GBD neoplasm-prevalence weights and the simulated Florida population. | Age pattern of **all three released files** by sex across the 22 age bins (the author's spec), against the GBD weights and the Florida extract, plus a race/ethnicity composition panel (new, v0.3). Optional incidence panel — **only if the FCDS incidence provenance is confirmed**. Caption states the pass criterion is peak band and sex crossover, not level, and that weights are age/sex only (no race-specific prevalence). | `pipeline/qa_age_sex.py` → `results/registry_age_sex.csv` (extended with race/ethnicity) + `reference/*.csv` | **Essential** |
| `tbl-example-pair` (Table 2) | Table | The same simulant as it appears in the registry and in a finder file, with the noise mechanism named for each discrepancy. | 2–3 paired rows over the published columns plus `simulant_id`; discrepant cells marked; caption also names the fidelity giveaways (lowercased addresses, `city = "unincorporated"`, a 2019 birth in a 2020 extract). Doubles as the evidence behind §4.2's artifact bullet. | `pipeline/example_pair.py` → `results/example_pair.csv` with pinned `simulant_id`s so the table is stable across reruns | **Essential** |
| `tbl-common-names` (Table 3) | Table | Most common first and last names in the registry stand-in, with counts. | Top-10 first and last names, stratifier per decision #17; reader-friendly fidelity evidence and the visible mechanism behind the uniqueness statistics and any stratified differential. Replaces the m/u table, cut 2026-08-09 at the author's direction. | `pipeline/data_forensics.py` → `results/forensics.json` — **NEW 2026-08-09** | **Essential** |
| `tbl-linkage-baseline` (Table 4) | Table | Deterministic exact-match rules scored against the `simulant_id` ground truth, 500,000-record finder file. | Five rules only — name+DOB; SSN alone; either FCDS minimum field set; current FCDS field set; name+DOB-or-SSN — plus `lastname_dob` if space allows, × {predicted pairs, TP, FP, precision, recall, missed-match %, false-match %}. 100k finder noted in one sentence. | `pipeline/linkage_baseline.py` → `results/linkage_baseline.json` (exists for v0.2; re-run at v0.3) | **Essential** |
| `fig-stratified-baseline` (Figure 2) | Figure | Recall and precision of headline deterministic rules by race/ethnicity. | Two or three rules × strata, with true-pair counts per stratum shown so small-cell noise is visible. The equity result; if the differential is null, the null is reported (decision #15). Caption carries the §4.2 caveat: race-uniform noise, name-structure effects only. | `pipeline/linkage_baseline.py` (stratified extension) → `results/linkage_baseline_stratified.json` — **NEW 2026-08-08** | **Essential** |
| `lst-noise-demo` (Listing 1) | Code listing | Generating noised records with pseudopeople and a targeted noise override, on the bundled ~10k-simulant sample population. | 8–12 echoed lines: build the hierarchical `noise_config` **pulling the rate from `cfg['noise']['finder']['address_missing']`, not a hard-coded 0.05**; call `generate_decennial_census`; show `.head()` and a one-line realised-rate check. The paper tier's only live computation. | `paper.qmd` chunk (replaces the current `sample-demo` stub) | **Essential** |
| `lst-fcds-fixed-width` | Code listing | Converting finder-file rows to the current FCDS 360-character fixed-width Data Linkage Record Layout. | ~15 lines: uppercase names, DOB → `YYYYMMDD` with 9-fill, missing SSN → `999999999`, padding to position; then 2–3 emitted records. Targets the current layout; the 2007 Attachment 9 layout is cited for existence only. | `paper.qmd` chunk over a function in `src/` that **does not yet exist** | **Optional — cut first** |

**Cut, deliberately:** `tbl-access-comparison` (every cell is a cited fact, so it is not a Results table; the contrast becomes prose split between §1.2, §4.4 and §5); `tbl-benchmark-comparison` and `tbl-prior-benchmarks` (the same comparator survey proposed twice, now prose in §1.3); `tbl-schema-layout` (repo documentation); `tbl-noise-config` (four numbers, better as a sentence); `tbl-noise-rates` (absorbed into Table 1's columns); `lst-weighted-sample` (the SQL becomes a one-line display expression in §2.2 and the run-twice assertion lives in `tests/`); `fig-qa-incidence` (merged as a panel of Figure 1). The uniqueness, blocking, and sentinel-check statistics are deliberately **prose numbers**, not tables — a few sentences in §3.3–§3.4 backed by `results/forensics.json`. `tbl-mu` (per-field m/u probabilities) cut 2026-08-09 at the author's direction: Fellegi–Sunter framing is a distraction from the paper's point.

---

## Computed values referenced in the text

Canonical variable names, deduplicated across the five drafts. **Only `results/linkage_baseline.json` exists today** — every row marked *TO WRITE* is currently a number that lives in a working notebook and nowhere else.

**v0.3 rebuild pending (2026-08-08):** the stratified-trim fix regenerates every released file, so every measured value below — the "verified" ones and everything in `linkage_baseline.json` included — is a v0.2 number that will change at rebuild; re-measure all of them then. Rows whose values are now fixed *by construction* are marked accordingly.

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
| `overlap_500k_simulants` | 100,000 by construction in v0.3 — verify at rebuild (v0.2 measured 129,356) | `release_manifest.json` — **TO WRITE** | "Realised overlap is `{python} overlap_500k_simulants` simulants against a target of `{python} overlap_500k_target` — exact." |
| `overlap_100k_simulants` | 20,000 by construction in v0.3 — verify at rebuild (v0.2 measured 25,797) | `release_manifest.json` — **TO WRITE** | as above, 100k file |
| `overlap_finder_finder` | 0 by construction in v0.3 — verify at rebuild (v0.2 measured 2,508, undesigned) | `release_manifest.json` — **TO WRITE** | "The two finder files share no simulants, so the 100k file is a clean held-out replicate." |
| `match_prevalence_500k`, `match_prevalence_100k` | 0.200 by construction in v0.3 — verify at rebuild (v0.2: 0.258712, 0.257970) | `release_manifest.json` — **TO WRITE** | "Match prevalence is `{python} match_prevalence_500k` of finder rows, as designed." |
| `overlap_500k_pairs` | ≈100,000 + registry-duplicate pairs — re-measure at rebuild (v0.2: 129,357) | `linkage_baseline.json` (re-run at rebuild) | "Recall is computed over `{python} overlap_500k_pairs` true record pairs." |
| `overlap_100k_pairs` | re-measure at rebuild (v0.2: 25,797) | `linkage_baseline.json` (re-run at rebuild) | as above |
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
| `uniq_name_dob`, `uniq_lastname_dob`, `uniq_zip_dob_sex` | *TO COMPUTE (v0.3)* | `forensics.json` — **TO WRITE** | "`{python} uniq_name_dob` of registry simulants are unique on first + last name and date of birth." |
| common-name counts | *TO COMPUTE (v0.3)* | `forensics.json` — **TO WRITE** | Table 3 cells only. |
| `pct_dob_blank`, `pct_dob_unparseable`, `n_doe_names`, `n_ssn_repeated`, `n_ssn_noncompliant` | *TO COMPUTE (v0.3)* | `forensics.json` — **TO WRITE** | "`{python} pct_dob_unparseable` of non-blank dates of birth fail to parse." |
| stratified ladder metrics | *TO COMPUTE (v0.3)* | `linkage_baseline_stratified.json` — **TO WRITE** | Figure 2 cells; prose quotes at most one contrast, via a named variable. |
| race/ethnicity composition | *TO COMPUTE (v0.3)* | `registry_age_sex.csv` (extended) — **TO WRITE** | Figure 1 race/ethnicity panel; §3.2's descriptive fractions. |
| `pairs_block_dob`, `completeness_block_dob` | *TO COMPUTE (v0.3)* | `forensics.json` — **TO WRITE** | "Blocking on full date of birth yields `{python} pairs_block_dob` candidate pairs retaining `{python} completeness_block_dob` of true pairs." |
| `load_full_usa`, `load_fl_psp`, `load_fl_extract` (wall time + peak RAM each) | *TO MEASURE* | `environment.json` — **TO WRITE** | §3.1's three-way load benchmark; §2.1's friction narrative depends on it. |

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

@misc{faker_software,
  author       = {Faraglia, Daniele and {Faker contributors}},
  title        = {Faker: a {Python} package that generates fake data},
  howpublished = {\url{https://github.com/joke2k/faker}},
  year         = {2026},
  note         = {Accessed 2026-08-08. Record the version current at draft time. Cited only for what it does not provide: no error model, no cross-file identity}
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

**Resolved, 2026-08-08:** the journal-format questions are settled by the Data Resource Profile guidelines the author supplied verbatim; the earlier claims about a "Data Note" type (four-heading abstract with problems-first Results, 2,000–3,000-word limit, mandatory Background between Introduction and Methods) were wrong and are gone from this outline. One check remains: the DRP word limit itself, which the guidelines defer to the journal's Fee Structure table.

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
6. **Faker / commercial generators.** The author's 2026-08-08 Introduction outline names faker explicitly, so it is now cited as software (`faker_software`, trim tier) — package metadata plus an access date is the right form for a tool cited only to say what it does not do, and the "no error model, no cross-file identity" claim is verifiable against faker's own documentation. Commercial generators remain unnamed: the equivalent claim about them is still an unverified negative.
7. **The §2.1 simulation brief.** The author's summary (ACS + 2020 Decennial Census initialisation; twenty years of mortality/fertility/mobility from those sources and GBD) is authoritative but must be reconciled with the published description in Haddock et al. before print.
8. **The household partial-move behaviour** ("always a single person who moves to a new household or joins an existing one as an 'other nonrelative'") — the author's own [[double check]]; verify against the simulation code before §4.2 states it.
9. **The installs-vs-requests ratio** (pseudopeople PyPI installs ≈ 100× the access requests for the gated state/national files — the author's recollection, marked "check this"). If verified, it appears in §1.3 and §4.3; if not, both keep the unquantified hedge.
10. **The Census Bureau cooperative agreement** (number CB21RMD0160001, and whether it is the right instrument for the §7 acknowledgment).

---

## Work still to be done before rendering

Ordered by dependency. Items 1–3 must complete before any other number in the paper can be trusted.

1. **Commit what already exists.** `config.yaml`, `pipeline/`, `results/` and `reference/` are all untracked. Commit them now, before anything else — the paper's only computed artifact is currently invisible to git and to any reviewer of the repo.
2. **`pipeline/extract_florida.py` → `results/population_summary.json`.** Port the Florida filter from the working notebook. Computes: `fl_simulants` (21,123,234); `fl_share_census`; `pop_ssn_never` (the *population-level* never-had-an-SSN rate, a new quantity distinct from the registry-measured rate); the registry duplicate-row count with its verified mechanism.
3. **`pipeline/build_cohorts.py` → staged Parquet + cohort ID lists, rebuilt as v0.3.** Port the weighted sampling, the five salted hash streams, the SSA join and the ordering fixes; replace the notebook's downsampling cell with `stratified_trim` from `src/simulated_data_for_fcds_scale_rl/downsample.py` (implemented and unit-tested 2026-08-08; `uv run pytest`). The v0.2 checksums are obsolete *by design*, so **the acceptance tests become: (a) every design target hit exactly — overlaps 100,000 and 20,000, finder files disjoint — and (b) run-twice checksum identity on the v0.3 files.** On success, bump `dataset.version` to 0.3 and point `paths.release_dir` at the new release directory in `config.yaml` (both left at 0.2 for now so `pipeline/linkage_baseline.py` keeps running against the existing files). Carry `race_ethnicity` from the census observer into the staged Parquet and the released schema (new in v0.3, for the stratified results). Run via sbatch/srun, never on a login node. This is the single highest-risk item in the run list.
4. **`pipeline/apply_noise_and_package.py` → `results/release_manifest.json` and `results/error_rates.json`.** Manifest: per-file rows, distinct simulants, overlap by *both* definitions (distinct simulants and row pairs — this is what reconciles 129,356 vs 129,357), byte sizes, MD5 **and SHA-256** (upstream pseudopeople releases publish SHA-256; matching that practice costs nothing). Error rates: realised missingness per targeted column per file **plus the SSN-transposition rate, which has never been measured**, alongside the targets from `config.yaml`. Record the finder–finder overlap — which must be 0 in v0.3 (v0.2 measured 2,508) — and match prevalence per finder file — 0.200 by design — as verification outputs of the stratified trim. (Why finder SSN missingness lands at exactly 0.200 is now resolved: the noise step sets missingness by target *count* and tops up only the shortfall, so the finder files hit 20% exactly while the registry, whose structural floor already exceeds its 5% target, is left alone.)
5. **`pipeline/qa_age_sex.py` → `results/registry_age_sex.csv`.** Registry and Florida-population counts by age bin and sex, plus the GBD weights used; extended (2026-08-08) with race/ethnicity composition of the registry, both finder files, and the Florida extract. Backs both panels of Figure 1 and the §4.2 claim about where the registry's mass sits, which currently cannot be made because the realised distribution has never been computed.
6. **`pipeline/example_pair.py` → `results/example_pair.csv`.** Search the overlap for exemplars showing a nickname or typo, a transposed SSN, a blanked address field, and a swapped month/day; pin the chosen `simulant_id`s so Table 2 is stable across reruns. Verify such exemplars actually exist before promising all four.
7. **`pipeline/data_forensics.py` → `results/forensics.json`.** Rescoped 2026-08-09 (the m/u probabilities are cut at the author's direction): quasi-identifier uniqueness shares and blocking candidate/completeness counts (§3.4 prose), most common first/last names per decision #17 (Table 3), date blank/parse rates, and the sentinel checks — Doe-pattern names, repeated-digit and SSA-non-compliant SSNs (§3.3), all per §2.5's definitions.
8. **Extend `pipeline/linkage_baseline.py` and re-run against the v0.3 release** (every baseline number changes with the data). Add the current layout's *other* minimum combination (name + sex + DOB + ZIP + street address) as a tenth rule — the shipped files carry every field it needs, and without it the paper covers only half of FCDS's current submission floor. Compute the ladder within `race_ethnicity` strata → `results/linkage_baseline_stratified.json` (Figure 2), with true-pair counts per stratum. Record the node spec (cores, RAM) alongside `seconds`, or the timing claim must be dropped.
9. **`results/environment.json`.** Pseudopeople version used at generation time (the venv has 1.2.8, but dataset v0.2 predates it), Python version, DuckDB version, node spec, and the construction run's wall time and peak RAM — the numbers §4.1 needs to make any scale claim at all. Include the three-way load benchmark (full USA via pseudopeople; Florida via `state=`; Florida from the staged extract), wall time and peak RAM each — §2.1's friction narrative and §3.1's benchmark bullet both depend on it.
10. **Deposit and mint DOIs.** Build the deterministic zip, deposit on Zenodo, mint a dataset DOI and a code-archive DOI, and obtain the private reviewer access URL IJPDS requires at submission. The Data Availability Statement, the Data Access section, the abstract and Key Features cannot be finalised without these.
11. **Fix `paper.qmd` front matter and structure.** Author is literally "Your Name"; ORCID is all zeros; author details need the full IHME address; the title lacks the mandatory `Data Resource Profile: ` prefix; the abstract stub uses the five-heading Research Article format instead of the four-heading Data Resource Profile content; the section is titled "Highlights" instead of "Key Features" and does not follow the six-bullet roster; the body must run Background → Methods → Results → Discussion → Data Access → Conclusions with no Introduction section. Add the back-matter statements per §7 (Acknowledgments, Ethics, COI, Publication Consent, Funding, Data Availability, Abbreviations, plus an AI Disclosure since this manuscript is AI-assisted), and verify `ijpds.csl` renders bracketed Vancouver numerals.
12. **Render once and commit `_freeze/` with `results/`.** Per `CLAUDE.md`, freeze hashes `paper.qmd` only and does not watch `src/`, `config.yaml` or data, so a render is required after every `src/` change and the two directories must be committed together.

---

## Open decisions for the author

1. **Manuscript type — RESOLVED (2026-08-08): Data Resource Profile**, per the author; the journal's DRP guidelines are recorded in this outline and the structure above follows them. One residual check: the DRP word limit in the journal's Fee Structure table.
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
15. **Stratified equity results (Figure 2):** kept provisionally per the author (2026-08-09, "we'll see how it fits"). If the computed race/ethnicity differentials come out null, report the null (recommended — it is informative, and this outline pre-registers the mechanism being tested), or demote Figure 2 to one sentence? **Report the null, or demote?**
16. **Registry scope — living residents only?** The stand-in samples living 2020 residents; a real registry accumulates deceased cases, and the author asks whether deceased people should be included. Recommended: keep the living-prevalent scope for v0.3, state it as a deliberate choice in §3.2 and a limitation in §4.2 (it compounds the disease-is-a-bolt-on gap), and defer deceased inclusion to future work. **Keep scope, or expand?**
17. **Common-names table (Table 3) stratifier:** by race/ethnicity (recommended — it makes Figure 2's mechanism visible) or by birth cohort? **Race/ethnicity, or birth cohort?**