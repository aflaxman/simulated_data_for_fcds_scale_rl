# Outline: Data Resource Profile: A Florida-scale simulated dataset for developing and benchmarking record-linkage software for cancer data systems

> This is a planning document, the draft is in paper.qmd. Claims marked **verified** were
> measured or checked on this date; everything else is marked *TO WRITE*, *to confirm*, or *unverified* and should be
> treated as a claim the paper cannot yet make.

**Editor's note.** The single claim this paper makes is: *what blocks record-linkage research and development is access to realistic test data, not methods — and here is a simulated, ground-truthed benchmark at the scale and cancer demography of a real US state registry that anyone can download without asking permission, together with a difficulty portrait that tells a user how hard the linkage is and for whom.* It is for two audiences at once — cancer-registry staff and vendors who need somewhere to test matching software that is not their own confidential file, and the linkage-methods community that has metrics but no large shared corpus. The paper is an IJPDS **Data Resource Profile**, so the focus is the dataset description: contents, characteristics, quality, and demonstrated and suggested uses.

---

## Title, authors, keywords

*Data Resource Profile: A Florida-scale simulated dataset for developing and benchmarking record-linkage software for cancer data systems*


1. Abraham D. Flaxman (corresponding author), Institute for Health Metrics and Evaluation, University of Washington, Population Health Building/Hans Rosling Center, 3980 15th Ave. NE, Seattle, WA 98195 USA, UW Campus Box #351615. ORCID 0000-0001-6033-4713. **Verified** 2026-09-24 (address supplied by the author).
2. Anders Alexandersson, Florida Cancer Data System, University of Miami Miller School of Medicine, Miami, FL, USA. *To confirm:* affiliation wording (inferred from the FCDS monograph's `fcds.med.miami.edu` host and `references.bib`), full street address, and ORCID; author order as listed.

**Keywords (7):** record linkage; entity resolution; simulated data; cancer registry; benchmark dataset; reproducibility; pseudopeople.

---

## Key Features

- **What is unique:** a large, fully simulated,  multi-file dataset for linking individual people, with cross-file ground-truth (every record carries a `simulant_id`, so missed-match and false-match rates of any method can be computed exactly rather than estimated), designed to capture the record matching challenges faced by a Florida-scale cancer data system.

- **Why created:** linkage software for cancer registries must be developed and tested on names, dates of birth, addresses and SSNs, which are exactly the identifiers that confidentiality rules prevent registries from releasing. 

- **Details:** a simulated Florida drawn from the `{python} fl_pool` simulants recorded as residents in the simulated 2020, 2030 or 2040 censuses, including a registry stand-in of `{python} registry_rows` records whose age and sex distribution is that of the cases reported by the Florida Cancer Data System, and researcher finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records drawn from residents in 2040.

- **Data linkage:** the larger finder file includes `{python} overlap_500k_target` simulants in the registry and the smaller finder file includes `{python} overlap_100k_target` simulants. There is no overlap between the finder files.

- **Main categories of data:** simulated person-level identifiers including name, date of birth, sex, street-address fields, SSN, race/ethnicity, carrying plausible synthetic noise (typos, nicknames, month/day swaps, blanks, duplications).

- **Access:** direct download under a permissive licence with a DOI.

---

## Structured abstract (draft, 292 words counting each `{python}` placeholder as one word and excluding the four headings — recount before submission; ≤300 permitted)

The Data Resource Profile abstract keeps four headings but assigns each dataset-first content: **Introduction** = a brief summary of the dataset; **Methods** = how it was created, original sources, linkage; **Results** = where it is held, contents, quality; **Conclusion** = how to access, suggested uses, ongoing improvements. The pipeline-lessons conclusion of the Data Note draft is retired. Each `{python}` placeholder is counted as one word.

> **Introduction**
> We present a simulated resource for developing and benchmarking cancer-registry record linkage: a registry stand-in and two researcher finder files at the scale of the linkage workload in the Florida Cancer Data System (FCDS). This will allow linkage software to be evaluated on fields such as names, dates of birth, addresses and Social Security numbers (SSNs), which are typically unavailable to outside researchers due to confidentiality. Our simulated data includes a ground-truth identity key, so precision, recall, and other quality metrics can be calculated exactly after the data has been linked.

> **Methods**
> We started with the simulated United States population that was developed for pseudopeople and extracted the `{python} fl_pool` simulants ever recorded as Florida residents in its 2020, 2030 and 2040 censuses, each at their last appearance, so that the pool, like a registry, includes people who have since died or moved away. We then sampled a registry stand-in of `{python} registry_rows` records with the age and sex distribution of the cases FCDS reports, as well as finder files of 2040 residents with `{python} finder_500k_rows` and `{python} finder_100k_rows` records with exactly `{python} overlap_500k_target` and `{python} overlap_100k_target` simulants overlapping the registry (and no overlap between finder files). We used keyed-hash sampling and a stratified trim to make each file a reproducible random sample and used noise functions from pseudopeople together with additional noise to supply realistic errors.
>
> **Results**
> The files are an open deposit on Zenodo, checksummed for verification. Against the ground-truth key, deterministic linkage of name plus date of birth links `{python} r500_name_dob_recall` of true pairs at `{python} r500_name_dob_precision` precision; exact agreement on FCDS's current minimum submission set links `{python} r500_fcds_current_recall` with no false matches. We publish quasi-identifier uniqueness, per-field error rates, and linkage statistics stratified by race/ethnicity; registry SSN missingness sits above target because some simulants never held an SSN.
>
> **Conclusion**
> The dataset is openly accessible with a direct download and includes a DOI.  We hope it will be useful for benchmarking and tuning linkage software, studying differential linkage error, and teaching.

**Review notes on the 2026-09-24 abstract (for the de-slop pass; the outline below is already propagated to it):**

- *What changed and is now propagated:* the uptake-barrier "experiment" is gone (also from the Editor's note and Key Features), so §1.3, §4.3, §4.4 and §6 no longer stage it; "additional noise" replaces "targeted overrides" everywhere; "a reproducible random sample" is the plain term for the seeded pipeline; "we" is the two authors. **Redesign 2026-09-24 (later the same day):** the registry is drawn from the last-seen pool across the three censuses to FCDS's age/sex case shares, and the finder files from 2040 residents; the Methods sentence above and Key Features now say so, which puts the abstract at roughly 305 words — the author's trim.
- *Accuracy:* "evaluated on confidential fields" — the simulated fields are not confidential; say "on the fields that are confidential in real data". "matching the 2020 decennial census" — the extract is the simulants *recorded as Florida residents in the simulated 2020 census* (§2.1). "FCDS's current minimum field set" — these are minimum *submission* field sets, not FCDS's matching rule (§3.4's relabelling); one word fixes it. "realistic errors" — the rates are author-chosen and plausible until the monograph is confirmed (§2.3); "plausible" is the word the body can defend.
- *Conclusion:* "accessable" → "accessible"; "includes a DOI for definitive referencing" → "has a DOI"; "easily" sells. The one operational fact that separates this from pseudopeople's gated files — no application, no approval — was dropped and is worth its five words. The journal's Conclusion roster also asks for *ongoing improvements*, which the draft no longer names (§6 keeps them); a clause fits if "checksummed for verification" or "after the data has been linked" goes.
- *Length:* 292 words leaves no room for the two restorations above without a trim.
- *Lingo:* Key Features calls the 5M file "a cancer registry"; the abstract and §1.2 call it the "registry stand-in". Pick one; the lingo rule favours the latter.
- *Numbers:* every placeholder still resolves to the 2026-08-12 GBD-weighted build until v0.3 is rebuilt in place with the FCDS weights (decision #7; the number stays 0.3 because nothing was released); `registry_rows` and the SSN-missingness sentence in Results must be re-checked after it.

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

*Compressed from a full page in the Introduction draft plus a duplicate subsection and table in the Discussion draft, now organised along the author's two failure axes: **not realistic enough**, or **not openly available at registry scale**. The comparator landscape is stated **once, here**, in prose. `tbl-prior-benchmarks` and `tbl-benchmark-comparison` stay cut.*

- Axis one, realism and scale. Generic fake-data tools such as faker produce clean, plausible, unlinked records — no error model, no cross-file identity, so no linkage testbed [@faker_software]. Linkage-specific generators model the right errors at the wrong scale: in the only controlled head-to-head benchmark, only three of five tools exceeded one million records, GeCo needed about 13 hours to corrupt one million and produced nothing at ten million [@hildebrandt2020dapo]; the shipped FEBRL and SOG corpora are counted in thousands [@christen2008febrl; @tran2013geco; @talburt2009sog], and the public benchmark inventory confirms the pattern [@binette2022almost].
- Be scrupulous about the counter-examples, because a reviewer will be: the largest openly downloadable person benchmarks are real North Carolina voters — 10M records with as few as four attributes, excluding children, so age-structured opposite to a cancer registry [@saeedi2018famer]. The one prior ~20M-person microsimulation built to study linkage quality does not appear to have been released [@schnell2023microsim]. The only cancer-registry benchmark ships precomputed comparison vectors with no names or dates, so it cannot exercise blocking or string comparison [@schmidtmann2011krebsregister]. Synthea publishes a million rich synthetic patients but no identifier-error model and no cross-file ground truth [@walonoski2018synthea].
- Axis two, access — pseudopeople's slot in the lineage, stated as fact and without the uptake-barrier apparatus that the abstract and Key Features no longer carry (2026-09-24): pseudopeople clears the realism and scale bar (a simulated US population with a ground-truth identity key [@haddock2024simulated]), but the population it ships openly is a ~10,000-simulant sample and its state- and national-scale populations are available only on request [@keyes2026governance]. Then the project's own history, as history rather than as external endorsement now that its author is the second author: the 2023 FCDS Splink feasibility study ran on a 1,000,000 × 1,000,000 synthetic test file supplied privately by the first author, noted that "the datasets are not yet publicly available", and recommended making the test data public [@alexandersson2023splinkfcds]; the published follow-up comparison of fastLink, Match\*Pro and Splink ran at Rhode Island scale, roughly one twentieth of the population FCDS serves [@alexandersson2024comparing]. This dataset is the public release that study asked for, built as a new and larger corpus rather than a release of the file it used (the reviewer's "fulfillment" objection stands; say "responds to"). **Retired from the paper (2026-09-24):** the "appears to be a barrier to uptake" hedge, the installs-vs-requests ratio (needs-verification #9), and the monitoring "experiment" (§4.3, §6); the plain statement above replaces them.
- **Do not mention "GeCo3"** — it is an unrelated DNA compressor. Do not name commercial vendors; the digest marks that as an unverified negative. And note the positionality edge: describing pseudopeople's access process is the first author describing his own project, and the FCDS history is the second author's own work — §4.4's positionality sentence must cover both.

### 1.4 Objective, and the sources this resource is built from — ¶2 (~180 words)

- The objective sentence, close to the author's outline wording and in step with the abstract's Introduction: we set out to make a low-barrier dataset for record-linkage research and development at the scale of the Florida cancer registry's typical linkage challenge — a direct download with a DOI, no application, no approval, and a published ground-truth key — so that linkage software can be evaluated on the fields that are confidential in real data and typically unavailable to outside researchers. ("Extremely low-barrier" is retired; the mechanics say it.)
- The author's tension sentence (2026-08-09), one clause, planted here and delivered in §4.4: even though the data are fake, they look real enough to risk doing harm — valid-looking SSNs, synthetic-identity seed material, addresses that must not be geocoded.
- Close the Background with the sources overview the genre requires, one sentence each: the **simulated United States population developed for pseudopeople** (the abstract's name for it; thereafter "the source population") — an individual-based microsimulation initialised from American Community Survey public-use microdata, carrying `simulant_id` as ground-truth identity across all its observers [@haddock2024simulated; @pseudopeople_software]; **FCDS's reported cases by age and sex**, the registry's age/sex target (§2.2), with GBD neoplasm prevalence for Florida as the QA comparator only; and **FCDS's published submission layouts**, the design template for the schema and the deterministic rules [@fdoh_fcds_procedure_guide_2007; @fcds_linkage_layout].
- What the paper reports, in the author's tripartite order: (1) the data resource — an incidence-weighted registry stand-in and two finder files with exactly known overlap; (2) the process of its development — the seeded, checksummed pipeline, additional noise at the rates the second author specified from FCDS's monograph work (§2.3), and the trim bug that scoring against the ground-truth key caught before release; (3) a difficulty portrait and demonstration usage — quasi-identifier uniqueness, data forensics, and deterministic baselines overall and stratified by race/ethnicity (§3.3–§3.4).
- Still deliberately *not* re-quoting the counts that Results owns — the exact overlaps and file sizes stay out of the Background entirely. The generalisation sentence (illicit-drug epidemiology, social work, economics) stays in §6; it duplicated the planned Conclusions.

---

## 2. Methods

*Target ≈ 850 words across five subsections — the Data Resource Profile asks Methods to detail the original sources, the linkage methods, and the study population. The author's outline prompts map as follows: "approach to getting age structure right" → §2.2; "approach to ensuring specific overlaps" → §2.2 (the stratified trim); "approach to setting noise levels" → §2.3; his proposed Methods table of the three files is folded into Table 1 (Results), which shows targets and realised values side by side. Load order: `paper.qmd` must open with a setup chunk reading `config.yaml` into `cfg` and the `results/` summaries into `lb`, `pop`, `err`, `rel`, `forensics`, `strat` before any inline expression resolves.*

### 2.1 Source population and the Florida extract — ¶3 (~220 words)

- The simulation is described in detail elsewhere [@haddock2024simulated; @pseudopeople_software]; give the author's own brief (2026-08-09), reconciled with the published description (needs-verification #7): a population initialised with the size and demographics (age, sex, household structure) of the 2020 United States from publicly available American Community Survey and 2020 Decennial Census data; mortality, fertility, and mobility modelled over twenty years from those sources and the Global Burden of Disease Study; and fully simulated versions of the confidential fields linkage runs on — names, dates of birth, addresses, SSNs — recorded for use with the pseudopeople Python package. The underlying large-scale populations are available through a lightweight approval process [@keyes2026governance]. Record the artifact name `pseudopeople_simulated_population_usa_2_0_0` (not the internal `release_02_yellow` tag), the Vivarium microsimulation `vivarium_census_prl_synth_pop` with `simulant_id` as ground-truth identity across all observers, the pseudopeople package version, and DuckDB `{python} duckdb_version`.
- The friction narrative, in the author's voice and with numbers behind it: using the full-USA data was possible but slow, and even pseudopeople's existing affordances for loading a single state with distributed computing were a barrier — so we built a Florida-only extract with DuckDB, using AI-assisted coding by Claude (disclosed here and in the back-matter AI Disclosure). The three-way load benchmark in §3.1 is the evidence; without those numbers this paragraph makes no claim. What stays true and verified about the affordances (pseudopeople 1.2.8): `generate_decennial_census` *does* take `state=`/`year=` and has a Dask engine — never claim otherwise, the first author is a pseudopeople co-author and a reviewer will catch it; `generate_social_security` has **no** `state` parameter, so the SSN join is by hand; and there is no API for prevalence-weighted or overlap-controlled sampling, which is the whole cohort design.
- Extraction mechanics: DuckDB reads the census-observer Parquet directly, keeps the Florida rows of the 2020, 2030 and 2040 censuses (`cohorts.census_years`), one per simulant per census, and builds two pools: the *last-seen pool* — every simulant ever recorded in Florida, once, at their latest census, `{python} fl_pool` people — from which the registry stand-in is drawn, and the residents of `{python} finder_year` (`{python} fl_finder_pool` people), from which the finder files are drawn. (Redesign 2026-09-24, decision #16: a registry keeps people who have since died or moved away, and the 2020 census alone cannot supply FCDS's age/sex pattern at 5M.) The 2020 census count, `{python} fl_simulants`, is kept only for the external-scale check in §2.4. SSNs come from the Social Security observer joined on `simulant_id`; `race_ethnicity` is carried through from the census observer into the released schema (new in v0.3) — FCDS's own submission layout carries race, so the column is transaction-faithful, and it is what §3.3–§3.4's stratified statistics stratify on.
- Two-tier note: this is pipeline-tier code run manually; nothing in the rendered paper executes it. The benchmark numbers replace conjecture — no unmeasured "cannot load even one state" claims.

### 2.2 Cohort design and reproducible sampling — ¶3 (~180 words)

- Design in one paragraph, targets from `config.yaml`: a registry stand-in targeting `{python} cfg_registry_target` records with the age and sex distribution of the cases FCDS reports, and two finder files targeting `{python} cfg_finder_500k_target` and `{python} cfg_finder_100k_target` records with `{python} overlap_500k_target` and `{python} overlap_100k_target` overlapping simulants. The target is the `count` column of `reference/fcds_incidence_by_age_sex.csv` (`config.yaml`, `paths.age_sex_target`), 18 age bins by sex, taken as shares; each stratum contributes an exact quota (`allocate_by_share` in `src/`: largest-remainder rounding, capped at the stratum's pool size), filled by the smallest keyed hashes within the stratum, so the registry's age/sex shares equal FCDS's to within the rounding of the noise trim (`results/age_sex_qa.json` records the largest deviation). **Redesigned 2026-09-24:** the 2026-08-12 build weighted a random draw by GBD prevalence; the first FCDS build the same day weighted it by incidence rates, which at a 36% oversample fraction compressed the ratio between strata (§3.2); exact quotas remove that, and the last-seen pool (§2.1) makes 5M attainable at 37% of the tightest stratum where the 2020 census alone could not (men 80–84 would have needed 101%). The GBD table stays in `reference/` as the Figure 1 comparator.
- Why FCDS's case shares, and why a pool with the dead in it, in two sentences with the drawback beside the choice: the registry's own reported caseload is the age/sex pattern a linkage against FCDS meets, and a registry keeps every case it registered, including people who have since died or moved away, so the stand-in is drawn from everyone ever recorded in Florida across the three simulated censuses, each at their last appearance, which is why we prefer it; the cost is that registry records carry the vintage of a person's last census (2020, 2030 or 2040), realistic for a registry but no longer a snapshot of one year's residents, and that three censuses span twenty years where FCDS's caseload spans four decades. GBD all-neoplasm prevalence for Florida is the independent comparator for the *shape* check in §2.4. Drop the unverified conjectures about "name eras" and "address stability" — the sufficient rationale is matching the registry's age/sex structure to Florida cancer demography.
- **Add the load-bearing fact all five drafts omitted:** overlap members are drawn from the registry cohort and the remainder from outside it via separate hash streams, and the two files are then noised *independently* (`psp_registry` seed `{python} cfg_seed_registry`, `psp_finder` seed `{python} cfg_seed_finder`). That independence is what makes this a linkage problem rather than a join.
- **The true pairs are same-year records — say so, and weigh it (2026-09-24).** Overlap members are registry members whose last census is the finder year, so a true pair's registry row and finder row are the *same source record noised twice*: no move, no aging, no surname change lies between them. This is the simplest choice and the easiest case a linkage can face, and it is why address agreement among true pairs is `{python} agree_street_name_500k` (§3.3) where a real registry sees far less. The pool keeps every census year, so drawing the registry record of an overlap member from an earlier census than the finder file is a change to the overlap draw alone — the address-change extension of §4.3.
- Reproducible randomness, **stated once here and not restated in the Discussion**: DuckDB's `random()` is not reproducible across threads, so every draw is made a pure function of the record key — the Efraimidis–Spirakis exponential-race key with the uniform replaced by a keyed hash. Quote the expression exactly, including the constant `18446744073709551617.0` (= 2⁶⁴+1); the Discussion draft's "2^64" is a paraphrase, and a section whose claim is bit-identical checksums cannot paraphrase the formula that produces them. Five salts give independent streams from seed `{python} cfg_seed_sample`. In prose the plain term is the abstract's — each file is "a reproducible random sample" — and "a pure function of the seed" appears once, as the mechanism.
- **Add the most reusable pattern in the pipeline, which no draft stated:** row-level omission noise deletes rows, so exact targets are unreachable in one pass; cohorts are drawn at `{python} cfg_oversample`× target and trimmed back afterwards with `numpy.default_rng({python} cfg_seed_postprocess)` over sorted ID lists. The trim must be *stratified* — exactly the target number of overlap members, filler drawn from survivors outside the entire overlap pool, the registry keeping only the chosen members (`stratified_trim` in `src/simulated_data_for_fcds_scale_rl/downsample.py`, unit-tested in `tests/test_stratified_trim.py`). The v0.2 build trimmed unstratified and overshot its overlap targets by a third; §3.1 tells that story in two sentences as evidence the ground-truth QA loop works. Note the reason for oversampling is that the number dropped is *not known in advance*, not that noise is nondeterministic (it is seeded and deterministic; that determinism is the point of §2.2's row-order fixes).
- The two silent order-dependence bugs, one sentence each: the staged Parquet must be written `ORDER BY simulant_id` because pseudopeople walks rows in file order, and the SSA join must be sorted before numpy selection. The run-twice assertion moves to `tests/`, mentioned in half a sentence; `lst-weighted-sample` is cut.

### 2.3 Noise, schema and packaging — ¶2 (~80 words)

- Base layer: pseudopeople's full default suite, each mechanism at 1% per cell per file, so a first name carries six mechanisms (blank, nickname, fake name, phonetic, OCR, typo), a date of birth six (blank, copied from a household member, month/day swap, wrong digits, OCR, typo), a last name five; row noise is 1.45% non-response plus duplication of some children. Additional noise (the abstract's term; never "overrides") from `config.yaml`, values never typed: finder files `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` SSN transposition, `{python} cfg_finder_address_missing` on each address field; registry `{python} cfg_registry_ssn_missing` / `{python} cfg_registry_ssn_transposed` / `{python} cfg_registry_address_missing`. **Provenance resolved 2026-09-24:** these are the second author's specification, quoted in the working notebook of 2026-02-02 — "I propose the same customization as in the FCDS 2024 monograph: Finder file: 20% missing SSN, 1% transposition error SSN, 5% missing Address; FCDS file: 5% missing SSN, 0% (no) transposition error SSN, 1% missing Address" — so the paper states them as FCDS's own characterisation of a finder submission against its consolidated file, attributed to the second author, and cites the monograph once its reference is confirmed (needs-verification #4); it does not defend them as realistic beyond that. Rationale in one clause: a researcher's finder file is dirtier than a certified registry's consolidated file [@qiao2023lexisnexis].
- Adjacent-digit SSN transposition is not in pseudopeople's noise taxonomy, so it is a post-hoc numpy step — the concrete affordance gap §4.1 generalises.
- **What the noise does not include, stated here and weighed in §4.2:** the SSN carries no wrong-digit or borrowed-number errors beyond the transposition (pseudopeople does not noise the SSN column in the census, so `{python} agree_ssn_500k` of true pairs with both SSNs present agree exactly); there is no surname change at marriage, because the two records of a true pair are the same year's record (§2.2); noise is symmetric between files and independent across fields, where real finder files have systematic habits (a cohort that recorded nicknames, SSNs typed from memory); and both files share one format exactly. These are the four structural ways the benchmark is easier than a real linkage.
- Published columns: `simulant_id` plus first name, middle initial, last name, date of birth, sex, street number, street name, unit number, city, state, ZIP, SSN, and (from v0.3) race/ethnicity. Say the release covers **all fields required by either minimum matching rule, plus race** — not "exactly the fields FCDS requires", since the current submission layout also carries maiden name, full middle name, alias and birthplace. `tbl-schema-layout` is cut as repo documentation.
- Deterministic archive: zip built with `-X` and fixed member timestamps so archive metadata is deterministic; checksums published for the three CSVs and the bundle. Dataset version `{python} dataset_version`; `config.yaml` is the single source of truth.

### 2.4 Quality assurance and the linkage baseline — ¶2 (~90 words)

- QA check 1, external scale: the extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents (a cited literal — **needs a Census Bureau citekey**).
- QA check 2, registry demography: the realised age/sex composition of each file (from the source's true ages, written by the build as `results/registry_age_sex.csv`) against the FCDS case shares the registry was drawn to — `results/age_sex_qa.json` records the largest deviation of any stratum share from its target, expected within the rounding of the trim — against the simulated Florida pools (`results/fl_census_age_sex.csv`), and against GBD all-neoplasm prevalence for Florida as an independent comparator. Agreement with FCDS is a check of the sampler, not of fidelity, and the caption must say so. The FCDS table's provenance is now load-bearing — it is the Methods input, not an optional panel — and its header still reads "PROVENANCE — NEEDS CONFIRMATION BEFORE PUBLICATION"; the second author supplied it and can confirm the report, diagnosis-year span and denominator at source (decision #7). Until then the paper describes it as an FCDS age/sex table of reported cases with its confirmation status stated.
- Define passing so it is falsifiable, and **do not use monotonicity**: verified against the committed FCDS file (2026-09-24), the female rate peaks at 80–84 (1,839 per 100,000) and falls at 85+ (1,732), the male rate peaks at 75–79 (2,754), is flat at 80–84 (2,753) and falls at 85+ (2,676), and the male rate at 5–9 (13.9) is below 0–4 (24.5), so "rises monotonically with age" is falsified by the paper's own inputs. The sex pattern crosses twice: female rates exceed male from 20–24 through 50–54, male rates exceed female from 55–59 up. The criterion for the GBD comparator is agreement in peak band and in those crossovers, not in level — the registry matches FCDS case shares by construction while GBD estimates prevalence, so the comparator panel differs in level by design.
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
- Age and sex: realised composition of **all three released files** against the FCDS case shares the registry was drawn to and the simulated Florida pools, split by sex (**Figure 1**, per the author's spec: the pyramid with FCDS dots and the top-3 first names per group), with GBD all-neoplasm prevalence as a comparator panel. **Measured 2026-09-24 on the first FCDS build (superseded the same day):** weighting a random draw by FCDS incidence rates followed the FCDS age pattern to about age 60 and then fell short of it — 65+ held 51.6% of registry records against 62.0% of FCDS cases, M:F 1.00 at 65–69 against 1.34 among FCDS cases — because weighted successive sampling compresses weight ratios at a high sampling fraction, and because the 2020 census alone cannot supply FCDS's shares at 5M (men 80–84 would need 101%). **Rebuilt 2026-09-24 with exact stratum quotas from the last-seen pool (§2.2): the realised shares are within 0.041 percentage points of FCDS's in every stratum** (`results/age_sex_qa.json`), and 46% of registry records are people last seen in 2040, 27% in 2020 and 27% in 2030. Figure 1's FCDS dots then sit on the bars by construction — say so in the caption, and let the race/ethnicity panel and the comparison with the Florida pools carry the independent check. (The FCDS file is "the age pattern Anders provided" from the author's outline; now that he is a co-author its provenance can be confirmed at source, decision #7, and it must be, because it is the Methods input.)
- Clinical characterisation, carefully scoped: the resource carries no tumour variables, so the "clinical" description the genre asks for is the FCDS age/sex case-share matching itself — age/sex only — and the registry-vs-target comparison. Decision #16 is resolved (2026-09-24): the stand-in is drawn from everyone ever recorded in Florida across the three censuses, each at their last appearance, so it includes people who had died or moved away by 2040 while the finder files are 2040 residents; state the scope and the registry's vintage mix (rows by census year, `results/age_sex_qa.json`) here and the drawback in §4.2.
- Race/ethnicity (new in v0.3): composition of the registry and finder files by `race_ethnicity` against the simulated Florida population (**Figure 1 panel or a one-row table**). State plainly, here and again in §4.2: the sampling weights are age/sex only, so the registry's race/ethnicity mix is inherited through age–race correlation in the population, not modelled — race/ethnicity-specific cancer prevalence is *not* represented.
- Households in one sentence: family members share surnames and addresses by construction of the source population, so address- and surname-based blocking meets realistic co-residence collisions [@haddock2024simulated].
- What the data look like: **Table 2** — the same simulant as it appears in the registry and in a finder file, `simulant_id` printed so the reader can verify, discrepant cells marked, noise mechanism named per row; two or three pairs showing a nickname or typo, a transposed SSN, and a blanked field. Name the fidelity giveaways in the same breath (lowercased addresses, `city = "unincorporated"`, a 2019-born person in a 2020 extract) — linkage-relevant, and users must be told; cross-reference §4.2. Add the author's address warning here as fact and in §4.2 as caveat: pseudopeople addresses are deliberately **not real addresses**, so running them through geocoding tools yields failures or fictitious hits — a surprise users must be spared [@pseudopeople_software].

### 3.3 Error structure — ¶2 (~300 words)

- Realised noise rates per targeted field per file against their `config.yaml` targets, folded into Table 1's columns. The one deviation narrated in prose is the SSN floor: realised registry missingness `{python} registry_ssn_missing` against the `{python} cfg_registry_ssn_missing` target, because `{python} pop_ssn_never` of Florida simulants never held an SSN in the source population and the pipeline warns rather than blanking further (**two distinct variables** — population rate vs registry-measured rate; never render "5.77%" as a literal). Arguably more realistic than the target: the New York State Cancer Registry reported 3.4% of 1.4M records lacking SSN [@qiao2023lexisnexis].
- **Table 5 — agreement among true pairs, the difficulty portrait's core (measured 2026-09-24, `results/pair_agreement.json`, `pipeline/pair_agreement.py`):** for each released field, the share of the `{python} overlap_500k_pairs` true pairs whose two records agree exactly when both are present, and the share with a blank on either side. First name `{python} agree_first_name_500k` / `{python} blank_first_name_500k`, last name `{python} agree_last_name_500k` / `{python} blank_last_name_500k`, date of birth `{python} agree_dob_500k` / `{python} blank_dob_500k`, street name `{python} agree_street_name_500k` / `{python} blank_street_name_500k`, SSN `{python} agree_ssn_500k` / `{python} blank_ssn_500k` (0.940/0.021, 0.959/0.020, 0.936/0.020, 0.970/0.059, 0.991/0.214 at the 2026-09-24 build). Read across to the ladder in one sentence: `{python} name_dob_all_agree_500k` of true pairs agree exactly on first name, last name and date of birth together, and `{python} ssn_usable_500k` have a usable, agreeing SSN, so the best simple rule's missed-match rate (§3.4) is what those two channels leave behind. The 100k file's figures match to the third decimal; say so in one clause and do not tabulate them.
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
- Comparator, two clauses: name+DOB-style deterministic rules on real data link 88–93% with 97–99% correct [@li2006deterministic], so exact name+DOB here (`{python} r500_name_dob_recall`) is *harder* than real data on recall and the simulated difficulty sits in a realistic band; and the gap between the best deterministic rule and perfect recall (`{python} r500_best_missed`) is the headroom a probabilistic method has to show, about what such methods recover over deterministic rules in practice. Do not call the ladder "too good": the noise rates are FCDS's own specification (§2.3), and the ways the benchmark is easier than reality are structural, named in §4.2.
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
- **Easier than a real linkage in four structural ways** (measured 2026-09-24, Table 5), stated beside the numbers: (1) true pairs are same-year records — no move, no aging, no surname change between diagnosis and cohort enrolment, so address agreement among true pairs is `{python} agree_street_name_500k` where real registries see far less, and any address-based rule is flattered; (2) the SSN is pristine beyond the `{python} cfg_finder_ssn_transposed` transposition — no wrong digits, no family member's number, no placeholder patterns; (3) noise is symmetric between files and independent across fields, where real finder files have systematic habits; (4) formats match exactly and the finder files carry essentially no duplicates. The rates themselves are the registry's own specification (§2.3), so the paper does not defend them as realistic beyond that; the remedies are the extensions of §4.3, and the first of them is the one we would do next.
- **Imperfect fidelity may mis-rank algorithms.** If a load-bearing feature of the real problem is absent — differential missingness, name change at marriage, first/last name dependence, the thin rare-name tail, all documented gaps of the source population [@haddock2024simulated] — package comparisons here could rank tools differently than production data would. That is the one error this resource must warn its users against: treat results as necessary, not sufficient, and validate winners in situ [@alexandersson2024comparing].
- **Race/ethnicity caveats, stated next to the equity results they qualify (§3.4):** first names are not race-conditioned in the source population, noise injection is race-uniform, and no race-differential data quality is modelled — so the stratified differentials measure name-structure effects only, and real-world differential error is plausibly larger.
- **Disease is a bolt-on, not integrated into the simulation** (the author's own characterisation, 2026-08-09): cancer status alters neither mobility nor mortality — a cancer patient and a healthy simulant of the same age, sex and race/ethnicity behave identically — so survivorship structure is absent. The related scope choice (decision #16, resolved 2026-09-24): the registry now includes simulants who died or left after their last census, but death is not modelled as a registry event — no vital status, no death clearance; cross-reference the identity-resolution-only bullet's death-clearance gap.
- **Household dynamics are simplistic:** when only part of a household moves, it is always a single person who moves to a new household or joins an existing one as an "other nonrelative" — **verify against the simulation code before print** (needs-verification #8). And the schema carries **no phone numbers or email addresses**, fields real linkage workflows increasingly rely on.
- **Addresses must not be geocoded:** they are deliberately not real addresses (§3.2); a user who geocodes them gets failures or fictitious locations.
- **Known construction imperfections that remain:** the SSN-missingness floor (§3.3 — the config parameter is a target the pipeline can only move realised missingness *up* to, never down) and the visible artifacts (§3.2: lowercased addresses, "unincorporated", the 2019-born infant). One consumer-facing defect worth a clause because it will bite the first user: the CSVs quote the rare comma-containing field (a `street_number` of `"64,66"` appears in `finder_100k.csv`) seldom enough that DuckDB's CSV sniffer infers no quote character and then fails to read the file — anyone loading the release must name the quote character explicitly; shipping Parquet alongside CSV in a future version removes the whole class of problem.
- **A registry of last-seen records.** The stand-in matches FCDS's age/sex case shares by construction, but each record is a person's last simulated census (2020, 2030 or 2040), so a large share of the registry is people who had died or left Florida by 2040 while the finder files are 2040 residents (the share is in `results/age_sex_qa.json`); realistic for a registry, but the address vintage mix is the simulation's, not FCDS's, and three censuses span twenty years where FCDS's caseload spans four decades. The case mix is validated only at the age/sex level, with race/ethnicity inherited from the population rather than modelled (§3.2).
- **Locale and vintage.** Names, addresses and households are USA-circa-2020, and name distributions transfer poorly: GeCo required structural forking for Brazilian composite and multiple family names [@trentin2018brazil]. Conclusions about name-comparator choice do not port to Brazil, Australia or non-Latin-script registries, and any ethnic-bias finding reflects US-2020 name structure only [@mcgrathlone2021ethnicbias].

### 4.3 Uses: demonstrated, current, and suggested — ¶1 (~140 words)

- Demonstrated in this paper: the deterministic ladder doubles as a worked example — a user can reproduce Table 4 from the deposit and the archived code before trusting their own harness.
- Current and adjacent use, stated precisely because no external project uses *this* deposit yet: the second author's FCDS monograph programme ran on privately supplied pseudopeople data and recommended a public corpus (§1.3); this is it. The natural next step, which the authors are placed to do themselves, is to re-run that package comparison on this corpus and report rank agreement with FCDS's internal results — name it in §6 as the external-validity test still outstanding, not as an invitation to a third party.
- Suggested uses, in the author's terms first: cancer-registry analysts comparing alternative linkage solutions, and algorithm developers benchmarking methods and evaluating new directions without the overhead of access to confidential data on real patients. Then one clause each: regression-testing in continuous integration, which gate-free access makes possible at this scale for the first time; differential-linkage-error and blocking research [@mcgrathlone2021ethnicbias]; and evaluating synthetic-identifier generators against a common target [@lam2024synthetic].
- **Extensions, each a small change to the pipeline because the pool keeps every census year (2026-09-24):** (a) *address change* — draw the registry record of an overlap member from an earlier census than the finder file (the person's first Florida appearance, or a random one), so a true pair carries ten or twenty years between its two records: a move, aging, and, once pseudopeople models it, a surname change — the one we would do next, because it turns address agreement from `{python} agree_street_name_500k` into something a registry would recognise; (b) wrong-digit and borrowed-number errors on the SSN in the finder files; (c) asymmetric, cohort-specific noise habits; (d) duplicates within the finder files. Each is a new version with its own checksums, never a silent change to v0.3; ask the second author first whether Table 5 looks like FCDS's real finder submissions, since he set the rates on purpose.
- **Monitoring, demoted (2026-09-24):** the abstract, Key Features and Editor's note no longer frame the release as an experiment on pseudopeople's access gate, so the monitoring plan (download counts against PyPI installs and against access requests for the gated populations) is at most one clause under §6's ongoing improvements, or cut. If any figure is quoted, needs-verification #9 applies; otherwise that item closes.

### 4.4 Why open release, and what it risks — ¶2 (~120 words)

- **Fix the provenance argument.** Do not call ACS PUMS "public aggregate statistics" and do not claim "no real person's record contributed". PUMS is individual-level public-use microdata of real households, sampled to initialise the simulation. The defensible argument runs through PUMS's own disclosure protections (already released, de-identified, swapped, top-coded) plus the fact that there is no confidential dataset fitted to and therefore no membership to leak — which is what distinguishes this from the generative-model threat model that membership-inference attacks target [@stadler2022groundhog]. Under the regulator's test the question becomes coincidental resemblance, not identifiability [@ico2023pets].
- Name the residual risk: coincidental generation [@suchow2023coincidental]. With tens of millions of simulated Floridians some name+DOB+city combinations will match real people by chance. Weigh against it that every name is a recombination of names each shared by many real Americans by construction of the public source lists [@haddock2024simulated].
- **Argue the benefit case against the right counterfactual, in step with §1.3.** The Background now says only that identifiers are unavailable to outside researchers and that pseudopeople's large populations are available on request; this subsection owes the concrete benefit of removing even that request, not a claim that the request deters anyone. The existing pseudopeople gate is a public, logged GitHub request under a relational-governance process [@keyes2026governance] — inverting the risk calculus against *real registry data* instead is a false dilemma. State who a gate excludes in practice: CI systems and containerised reproductions cannot open an issue; classroom and workshop use at scale; and a fixed, checksummed artifact makes *this paper's own results* reproducible in a way a re-request cannot. Say these once, here.
- Guardrails as a short list: provenance documentation, determinism plus published checksums, a DOI deposit with versioning and a tombstoned withdrawal path [@zenodo_policies], prominent "simulated data" labelling, and a stated objection route — put with the author's honesty (2026-08-09): if someone objects to a simulated likeness of their name, *we have less recourse* than a controller of real data would. **Present the objection route as an untested proposal, not a novel contribution.** Changing the sampling salt re-draws *which* simulants are selected; it does not regenerate the names attached to a given simulant, so a complainant's name can reappear — and it destroys comparability with every published result on v0.2. If a mechanism is promised, it must be targeted suppression plus a tombstoned version bump, and it must actually be implemented on the deposit. Say "we are not aware of a comparable project that states one", which is what the evidence supports.
- **Add one sentence of positionality.** This section assesses the ethics of the first author's own simulator, using his own governance framing, and the paper's origin is a recommendation written by the second author that names the first author personally. Acknowledging both pre-empts a reviewer raising it less charitably; the COI statement carries the rest (§7).
- **Add the exposure no draft mentioned:** the files ship syntactically valid SSNs alongside full name, DOB and address. A released SSN can collide with a real issued number, and the corpus is usable as synthetic-identity seed material. The labelling guardrail should name the risk it mitigates, and contamination of a real registry system by simulated records should be raised.

---

## 5. Data Access

*Target ≈ 150 words. A required section for this genre — the paper's thesis made operational — and it feeds the Data Availability Statement.*

- Where: the Zenodo deposit — dataset DOI and version (run-list item 10) — with the pipeline archived under a code DOI and the repository linked.
- How: direct download; no application, no approval, no registration, no data-use agreement. Licence per decision #9 (CC0 recommended). Published MD5/SHA-256 checksums verify the download; `config.yaml` in the archive records every seed and target.
- Versioning and redress: versioned deposits with a tombstoned withdrawal path [@zenodo_policies]; the objection route presented as an untested proposal (§4.4); prominent "simulated data" labelling on the deposit landing page, naming the synthetic-identity-seed risk it mitigates (§4.4).
- Contact: the corresponding author. Key Features no longer carries the collaboration invitation (2026-09-24), so this is the one place it appears.
- At submission: IJPDS requires the dataset DOI plus a private reviewer URL; the Data Availability Statement (§7) uses the journal's "openly available in a public repository" wording, with repository name, DOI, and no access restrictions to declare.

## 6. Conclusions

*Target ≈ 120 words, ¶1.*

- What exists now, in one sentence, close to the author's wording: a set of simulated data files for testing record linkage in the size and shape of the challenges faced by the Florida state cancer registry — direct download, DOI, no application or approval, published ground-truth key, deterministic baselines.
- Second sentence, matching the abstract's Conclusion: what we hope it is used for — benchmarking and tuning linkage software, studying differential linkage error, and teaching — with the FCDS package-comparison re-run named as the external-validity test still outstanding (§4.3). The "we made this openly available *to see whether* the request process has been a barrier" framing of earlier drafts is retired with the monitoring plan.
- Implications of use, one sentence: results on this corpus are necessary-but-not-sufficient evidence about production performance — validate winners in situ (§4.2) [@alexandersson2024comparing].
- Generalisation, kept: the transaction this dataset is shaped like — a government-held population-scale file, a researcher cohort, a minimum-identifiers rule, no shareable ground truth — recurs in vital statistics and drug-epidemiology cohort follow-up, and beyond health in social work and economics. One clause closes the loop with §1.1: wherever that transaction recurs, the binding constraint on linkage research and development is access to realistic test data, and the pattern here — simulate at scale, publish without a gate — transfers even where this dataset does not.
- Ongoing improvements, one sentence, because the journal's Conclusion roster asks for them even though the abstract no longer names them (see the review notes above): Parquet distribution alongside CSV, probabilistic (Splink) baselines, an address-change version in which registry records predate the finder file (§4.3), and community-contributed rule submissions. Close with the author's invitation, verbatim: *let us know what you find!*

## 7. Required back-matter statements

All mandatory per the guidelines the author supplied (2026-08-08); one drafting note each.

- **Acknowledgments:** Anders Alexandersson is a co-author (2026-09-24), so the by-name thanks of earlier drafts is retired (decision #14 closed). Acknowledge the US Census Bureau for making the underlying population possible — but **rephrase the author's draft** ("regret that they got too busy to continue cooperating in our cooperative agreement" will read as a dig at a federal agency in print): e.g. acknowledge support under cooperative agreement CB21RMD0160001 and note the agreement concluded before this work; exact wording is the author's call (needs-verification #10 for the agreement number's applicability).
- **Ethics Statement:** state that ethical approval was not required and why — fully simulated data, no human subjects or participants; the source population derives from public-use microdata carrying its own disclosure protections (§4.4).
- **Conflict of Interests Statement:** ICJME form; disclose that the first author built pseudopeople, co-authored the source population, helps govern access to it, and is named personally in the monograph recommendation (decision #10 — recommended: disclose); and that the second author wrote the FCDS feasibility study and package comparison [@alexandersson2023splinkfcds; @alexandersson2024comparing] whose recommendation this profile responds to (§1.3, §4.3).
- **Publication Consent:** written acknowledgement of consent to publish and openly share the data — author-generated simulated data, so the author grants it; one sentence.
- **Funding Statement:** grant or "no specific funding" (decision #13); distinguish this work from the source population's Gates INV-060835 and Census CB21RMD0160001 funding; note salary sources if the funder requires.
- **Data Availability Statement:** placed just before References; the journal's open-repository wording with repository name, DOI/URL and reference number; no access restrictions to state.
- **Abbreviations:** compile at draft time — at minimum FCDS, SSN, DOB, GBD, ZIP, CSV, DOI, ACS, PUMS, NAACCR, IJPDS.
- **References:** Vancouver style with bracketed numerals in the text and DOIs for every entry that has one — verify `ijpds.csl` renders `[1]`-style brackets; include URLs where available.

---

## Figures, tables and code listings

Eight essential items plus one optional — the Data Resource Profile's length carries the forensics table (Table 3), the stratified figure (Figure 2) and the true-pair agreement table (Table 5, added 2026-09-24; fold it into Table 1 as columns if the display budget binds). **Master-graphic candidates (2026-09-24, author comparing):** `pipeline/draw_candidate_figures.py` renders three to `figures/` from `results/` — (1) the age/sex pyramid of the registry stacked by race/ethnicity with FCDS case shares as dots and the top-3 first names per group in the margins, (2) two record pairs with discrepancies washed and named, (3) the two side by side with a deposit inset. Whichever wins becomes Figure 1 (and the record pairs may replace Table 2 as a graphic). Everything else proposed across the five drafts stays cut; the cut list is at the end of this section so the decisions are visible rather than silent.

| Label | Kind | Caption | What it shows | Produced by | Status |
|---|---|---|---|---|---|
| `tbl-release` (Table 1) | Table | The released files: contents, designed and realised overlap, targeted versus realised error rates, size and checksums. | Rows: `registry.csv`, `finder_500k.csv`, `finder_100k.csv`, bundle `.zip`. Columns: rows; distinct simulants; overlap target and realised (equal by construction in v0.3; pairs footnoted); SSN missing target/realised; street-name missing target/realised; size (MB); MD5 + SHA-256. Merges three separately proposed tables and absorbs `tbl-error-rates` as four columns. | `paper.qmd` chunk over `results/release_manifest.json` + `results/error_rates.json` + `results/linkage_baseline.json` + `config.yaml` | **Essential** |
| `fig-registry-age-sex` (Figure 1) | Figure | Realised age/sex and race/ethnicity composition of the simulated registry against the FCDS incidence weights it was drawn with, GBD neoplasm prevalence as a comparator, and the simulated Florida population. | Age pattern of **all three released files** by sex across the 22 age bins (the author's spec), against the FCDS weights, the GBD comparator and the Florida extract, plus a race/ethnicity composition panel (new, v0.3). **The FCDS provenance must be confirmed regardless (decision #7)**, since it is now the Methods input. Caption states the pass criterion is peak band and sex crossover, not level, and that weights are age/sex only (no race-specific prevalence). | `pipeline/qa_age_sex.py` → `results/registry_age_sex.csv` (exists 2026-09-24) + `reference/*.csv`; drawn by `figures.pyramid` in `src/` | **Essential** |
| `tbl-example-pair` (Table 2) | Table | The same simulant as it appears in the registry and in a finder file, with the noise mechanism named for each discrepancy. | 2–3 paired rows over the published columns plus `simulant_id`; discrepant cells marked; caption also names the fidelity giveaways (lowercased addresses, `city = "unincorporated"`, a 2019 birth in a 2020 extract). Doubles as the evidence behind §4.2's artifact bullet. | `pipeline/example_pair.py` → `results/example_pair.csv` (exists 2026-09-24; pairs 1007_399543 and 1534_695157), drawn as a record-pair panel by `figures.record_card` in `src/` | **Essential** |
| `tbl-common-names` (Table 3) | Table | Most common first and last names in the registry stand-in, with counts. | Top-10 first and last names, stratifier per decision #17; reader-friendly fidelity evidence and the visible mechanism behind the uniqueness statistics and any stratified differential. Replaces the m/u table, cut 2026-08-09 at the author's direction. | `pipeline/data_forensics.py` → `results/forensics.json` — **NEW 2026-08-09** | **Essential** |
| `tbl-linkage-baseline` (Table 4) | Table | Deterministic exact-match rules scored against the `simulant_id` ground truth, 500,000-record finder file. | Five rules only — name+DOB; SSN alone; either FCDS minimum field set; current FCDS field set; name+DOB-or-SSN — plus `lastname_dob` if space allows, × {predicted pairs, TP, FP, precision, recall, missed-match %, false-match %}. 100k finder noted in one sentence. | `pipeline/linkage_baseline.py` → `results/linkage_baseline.json` (exists for v0.2; re-run at v0.3) | **Essential** |
| `tbl-pair-agreement` (Table 5) | Table | Agreement between the two records of each true pair, by field: share agreeing exactly when both present, share blank on either side. | One row per released field, 500k finder file (the 100k file matches to the third decimal, noted in prose); two summary rows — exact agreement on first name, last name and date of birth together; usable and agreeing SSN. The difficulty portrait's core and the evidence behind §4.2's structural-easiness bullet. | `pipeline/pair_agreement.py` → `results/pair_agreement.json` (exists 2026-09-24) | **Essential** |
| `fig-stratified-baseline` (Figure 2) | Figure | Recall and precision of headline deterministic rules by race/ethnicity. | Two or three rules × strata, with true-pair counts per stratum shown so small-cell noise is visible. The equity result; if the differential is null, the null is reported (decision #15). Caption carries the §4.2 caveat: race-uniform noise, name-structure effects only. | `pipeline/linkage_baseline.py` (stratified extension) → `results/linkage_baseline_stratified.json` — **NEW 2026-08-08** | **Essential** |
| `lst-noise-demo` (Listing 1) | Code listing | Generating noised records with pseudopeople and an additional noise setting, on the bundled ~10k-simulant sample population. | 8–12 echoed lines: build the hierarchical `noise_config` **pulling the rate from `cfg['noise']['finder']['address_missing']`, not a hard-coded 0.05**; call `generate_decennial_census`; show `.head()` and a one-line realised-rate check. The paper tier's only live computation. | `paper.qmd` chunk (replaces the current `sample-demo` stub) | **Essential** |
| `lst-fcds-fixed-width` | Code listing | Converting finder-file rows to the current FCDS 360-character fixed-width Data Linkage Record Layout. | ~15 lines: uppercase names, DOB → `YYYYMMDD` with 9-fill, missing SSN → `999999999`, padding to position; then 2–3 emitted records. Targets the current layout; the 2007 Attachment 9 layout is cited for existence only. | `paper.qmd` chunk over a function in `src/` that **does not yet exist** | **Optional — cut first** |

**Cut, deliberately:** `tbl-access-comparison` (every cell is a cited fact, so it is not a Results table; the contrast becomes prose split between §1.2, §4.4 and §5); `tbl-benchmark-comparison` and `tbl-prior-benchmarks` (the same comparator survey proposed twice, now prose in §1.3); `tbl-schema-layout` (repo documentation); `tbl-noise-config` (four numbers, better as a sentence); `tbl-noise-rates` (absorbed into Table 1's columns); `lst-weighted-sample` (the SQL becomes a one-line display expression in §2.2 and the run-twice assertion lives in `tests/`); `fig-qa-incidence` (merged as a panel of Figure 1). The uniqueness, blocking, and sentinel-check statistics are deliberately **prose numbers**, not tables — a few sentences in §3.3–§3.4 backed by `results/forensics.json`. `tbl-mu` (per-field m/u probabilities) cut 2026-08-09 at the author's direction: Fellegi–Sunter framing is a distraction from the paper's point.

---

## Computed values referenced in the text

Canonical variable names, deduplicated across the five drafts. **Five `results/` files now exist (2026-08-12):** `linkage_baseline.json`, `release_manifest.json`, `error_rates.json`, `population_summary.json`, `environment.json` — all measured on the v0.3 release. Still to write: `forensics.json`, `linkage_baseline_stratified.json`, `registry_age_sex.csv`.

**Rebuilt 2026-09-24 (v0.3, last-seen pool, FCDS case shares by exact quota, 2040 finder files; nothing was released, so the number stays):** every `results/` value below is from this build unless marked otherwise; registry rows 5,000,002 (2 duplication rows), age/sex shares within 0.041 pp of FCDS's, 46% of registry records last seen in 2040 and 27% each in 2020 and 2030, structural SSN missingness 5.68% against the 5% target. The run-twice checksum identity test has not yet been repeated for this design. **Earlier: v0.3 built and verified 2026-08-12:** `pipeline/build_cohorts.py` ran twice on the cluster; every design target hit exactly, and the two runs produced byte-identical files (run-twice checksum identity). The values below are v0.3 measurements; v0.2 history is noted where it differs.

| `{python}` variable | Known value | `results/` file | Sentence |
|---|---|---|---|
| `fl_pool` | 50,518,675 — **measured 2026-09-24** (`fl_census_age_sex.csv`; the build writes it as `fl_pool_last_seen`) | `population_summary.json` | "…the `{python} fl_pool` simulants ever recorded as Florida residents in the 2020, 2030 or 2040 census, each at their last appearance." |
| `fl_finder_pool`, `finder_year` | 22,959,862; 2040 — **measured 2026-09-24** (`fl_residents_finder_year`) | `population_summary.json` | "…finder files drawn from the `{python} fl_finder_pool` residents of `{python} finder_year`." |
| `fl_simulants` | 21,123,234 — **measured** (2020 census residents; kept only for the official-count check) | `population_summary.json` (exists) | "The simulated 2020 census records `{python} fl_simulants` Florida residents, `{python} fl_share_census` of the official count…" |
| `registry_rows_by_year`, `age_sex_max_dev` | 2020: 1,329,059; 2030: 1,376,079; 2040: 2,294,864; largest deviation 0.041 pp (men 45–49) — **measured at the 2026-09-24 build** | `age_sex_qa.json` (exists) | "…`{python} age_sex_max_dev` percentage points from the FCDS shares; `{python} registry_share_pre2040` of registry records are people last seen in 2020 or 2030." |
| `fl_share_census` | 0.98073 | `population_summary.json` (exists; denominator 21,538,187 is a cited literal) | "The extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents." |
| `pop_ssn_never` | 0.04183 over the last-seen pool (**measured 2026-09-24**; 0.04992 in the 2020 census alone) | `population_summary.json` (exists) | "…because `{python} pop_ssn_never` of the registry pool never held an SSN in the source population." |
| `registry_rows` | 5,000,012 (v0.2: 5,000,019) | `linkage_baseline.json` (exists) | "The registry stand-in holds `{python} registry_rows` rows…" |
| `registry_simulants` | 5,000,000 — exact by construction, **verified at build** | `linkage_baseline.json` (exists) | "…for `{python} registry_simulants` distinct simulants." |
| `registry_dupe_rows` | 12 (v0.2: 19) — duplication-noise pairs, rows differing in content; re-verify the two-rows-differ mechanism on v0.3 in `example_pair.py` | `release_manifest.json` (exists) | "The `{python} registry_dupe_rows` excess rows are the within-file duplication a real registry carries." |
| `registry_ssn_missing` | 0.05775 (v0.2: 0.057723) | `linkage_baseline.json` (exists) | "Registry SSN missingness reached `{python} registry_ssn_missing`, above its target." |
| `finder_500k_rows` | 500,000 | `linkage_baseline.json` (exists) | "…two finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records." |
| `finder_100k_rows` | 100,000 | `linkage_baseline.json` (exists) | as above |
| `finder_ssn_missing` | 0.200 | `linkage_baseline.json` (exists) | "SSN is blank in `{python} finder_ssn_missing` of finder records." |
| `overlap_500k_simulants` | 100,000 — **verified at build 2026-08-12** (v0.2 measured 129,356) | `release_manifest.json` (exists) | "Realised overlap is `{python} overlap_500k_simulants` simulants against a target of `{python} overlap_500k_target` — exact." |
| `overlap_100k_simulants` | 20,000 — **verified at build** (v0.2 measured 25,797) | `release_manifest.json` (exists) | as above, 100k file |
| `overlap_finder_finder` | 0 — **verified at build** (v0.2 measured 2,508, undesigned) | `release_manifest.json` (exists) | "The two finder files share no simulants, so the 100k file is a clean held-out replicate." |
| `match_prevalence_500k`, `match_prevalence_100k` | 0.200000 both — **verified at build** (v0.2: 0.258712, 0.257970) | `release_manifest.json` (exists) | "Match prevalence is `{python} match_prevalence_500k` of finder rows, as designed." |
| `overlap_500k_pairs` | 100,000 — **measured** (no overlap member sits on a duplicated registry row in v0.3; v0.2: 129,357) | `linkage_baseline.json` (exists) | "Recall is computed over `{python} overlap_500k_pairs` true record pairs." |
| `agree_<field>_500k`, `blank_<field>_500k` (first_name, last_name, dob, street_name, ssn, …) | 0.940/0.021, 0.959/0.020, 0.936/0.020, 0.970/0.059, 0.991/0.214 — **measured 2026-09-24** | `pair_agreement.json` (exists) | Table 5; "…first names agree exactly in `{python} agree_first_name_500k` of true pairs with both present…" |
| `name_dob_all_agree_500k`, `ssn_usable_500k` | 0.793, 0.779 — **measured 2026-09-24** | `pair_agreement.json` (exists) | "…`{python} name_dob_all_agree_500k` of true pairs agree exactly on name and date of birth together, and `{python} ssn_usable_500k` have a usable, agreeing SSN." |
| `overlap_100k_pairs` | 20,000 — **measured** (v0.2: 25,797) | `linkage_baseline.json` (exists) | as above |
| `overlap_500k_target` / `overlap_100k_target` | 100,000 / 20,000 | `config.yaml` (exists) | "…against targets of `{python} overlap_500k_target` and `{python} overlap_100k_target`." |
| `cfg_registry_target`, `cfg_finder_500k_target`, `cfg_finder_100k_target` | 5,000,000 / 500,000 / 100,000 | `config.yaml` (exists) | "The registry cohort targets `{python} cfg_registry_target` records…" |
| `cfg_oversample` | 1.15 (was 1.5; pseudopeople drops ~1.5% of rows) | `config.yaml` (exists) | "Cohorts are drawn at `{python} cfg_oversample`× target…" |
| `cfg_seed_sample`, `cfg_seed_registry`, `cfg_seed_finder`, `cfg_seed_postprocess` | 42, 42, 1, 999 | `config.yaml` (exists) | "All stochastic steps take their seeds from `config.yaml`…" |
| `cfg_finder_ssn_missing` / `_ssn_transposed` / `_address_missing` | 0.20 / 0.01 / 0.05 | `config.yaml` (exists) | "Finder files receive `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` transposition…" |
| `cfg_registry_ssn_missing` / `_ssn_transposed` / `_address_missing` | 0.05 / 0.00 / 0.01 | `config.yaml` (exists) | "…against the registry's `{python} cfg_registry_ssn_missing` target." |
| `err_street_500k`, `err_street_100k`, `err_street_reg` | 0.049842, 0.049950, 0.010068 — **measured, v0.3** | `error_rates.json` (exists) | Table 1 cells; "street name is blank in `{python} err_street_500k` of the 500k finder file." |
| `err_ssn_transposed` | 3,988 transposed of the 500k finder's valid SSNs (≈1.0%) — **measured at build** (was never measured for v0.2) | `error_rates.json` (exists) | "Adjacent SSN digits were transposed in `{python} err_ssn_transposed` of finder records." |
| `size_registry_mb`, `size_finder500k_mb`, `size_finder100k_mb`, `size_zip_mb` | 510.4, 49.7, 9.9, 214.7 — v0.3 (registry grew with the `race_ethnicity` column) | `release_manifest.json` (exists) | Table 1 cells; "…zipped to a `{python} size_zip_mb` MB bundle." |
| `md5_registry`, `md5_finder500k`, `md5_finder100k`, `md5_zip` | `b1ee6fca…`, `d337a546…`, `974eaa12…`, `cc91aea4…` — v0.3, identical across two independent builds; SHA-256 also recorded | `release_manifest.json` (exists) | Table 1 cells; "the published MD5 of the bundle is `{python} md5_zip`." |
| `fcds_rate_min`, `fcds_rate_max` | 12.09 (females 5–9), 2,753.68 (males 75–79) — **per 100,000; verified against the file 2026-09-24** | `reference/fcds_incidence_by_age_sex.csv` (exists; the registry weights since 2026-09-24) | "…from `{python} fcds_rate_min` (females 5–9) to `{python} fcds_rate_max` (males 75–79) per 100,000." |
| `fcds_rate_female_max` | 1,838.96 at ages 80–84 (**verified against the file**) | `reference/fcds_incidence_by_age_sex.csv` (exists) | Figure 1 caption; "the female rate peaks at `{python} fcds_rate_female_max` per 100,000." |
| `gbd_prev_min`, `gbd_prev_max` | 0.59, 32.36 (**percent units**) — comparator panel only since 2026-09-24, not the weights | `reference/gbd_neoplasm_prevalence_florida.csv` (exists) | Figure 1 comparator; "…GBD prevalence runs from `{python} gbd_prev_min`% (males under 1) to `{python} gbd_prev_max`% (males 95+)." |
| `gbd_prev_female_max` | 21.84 at ages 85–90 (**verified against the file**) — comparator only | `reference/gbd_neoplasm_prevalence_florida.csv` (exists) | Figure 1 caption, comparator panel. |
| `r500_name_dob_precision` / `_recall` / `_missed` | 0.99775 / 0.79448 / 0.20552 — v0.3 | `linkage_baseline.json` (exists) | "Name plus date of birth linked `{python} r500_name_dob_recall` at `{python} r500_name_dob_precision` precision." |
| `r500_ssn_only_precision` / `_missed` | 0.99978 / 0.21527 — v0.3 | `linkage_baseline.json` (exists) | "SSN alone reaches precision `{python} r500_ssn_only_precision` yet misses `{python} r500_ssn_only_missed`." |
| `r500_fcds_min_ssn_recall` | 0.65439 (FP = 0) — v0.3 | `linkage_baseline.json` (exists) | "…makes no false matches but finds only `{python} r500_fcds_min_ssn_recall` of true pairs." |
| `r500_fcds_min_monthyear_fp` / `_precision` | 5,550 / 0.93259 — v0.3 | `linkage_baseline.json` (exists) | "The month/year variant admits `{python} r500_fcds_min_monthyear_fp` false matches." |
| `r500_fcds_either_recall` / `_precision` | 0.81944 / 0.93657 — v0.3 | `linkage_baseline.json` (exists) | "Taking either field set raises recall to `{python} r500_fcds_either_recall`." |
| `r500_fcds_current_recall` | 0.59916 (FP = 0) — v0.3 | `linkage_baseline.json` (exists) | "Exact agreement on the current minimum field set links `{python} r500_fcds_current_recall` with no false matches." |
| `r500_best_recall` / `r500_best_precision` | 0.95550 / 0.99795 — v0.3 | `linkage_baseline.json` (exists) | "Name-and-birthdate-or-SSN links `{python} r500_best_recall` at `{python} r500_best_precision`." |
| `r500_lastname_dob_precision` | 0.65208 — v0.3 (v0.2: 0.70006) | `linkage_baseline.json` (exists) | "…collapses to precision `{python} r500_lastname_dob_precision`, showing the benchmark punishes weak keys." |
| `baseline_seconds_500k` | 7.1 — still needs the node spec (§3.4) | `linkage_baseline.json` (exists) | "The full ladder runs in `{python} baseline_seconds_500k` seconds." |
| `duckdb_version` | 1.5.4 | `linkage_baseline.json` (exists) | "Extraction, sampling and scoring run in DuckDB `{python} duckdb_version`." |
| `psp_version` | 1.2.8 — **recorded at v0.3 generation time** | `environment.json` (exists) | "…generated with pseudopeople `{python} psp_version`." |
| `dataset_version` | 0.3 | `config.yaml` / `linkage_baseline.json` (exists) | "This profile describes dataset version `{python} dataset_version`." |
| `build_wall_hours`, `build_node_spec` | 909 s wall, 18.3 GB peak RSS, hostname + CPU count recorded — **measured, v0.3 build** (the three-way load benchmark is still to add, item 9) | `environment.json` (exists) | "The full build completes in `{python} build_wall_hours` on `{python} build_node_spec`." |
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
2. **GBD source for the neoplasm prevalence table — demoted 2026-09-24.** The table is no longer the registry weights (those are FCDS incidence, decision #7), only the Figure 1 comparator. `reference/gbd_neoplasm_prevalence_florida.csv` still documents only an internal `vivarium_inputs` extraction and its header demands the round/release be recorded; if the comparator panel is kept it needs a GBD results-tool citation or the capstone paper plus the round in the CSV, and if the panel is dropped this item closes.
3. **US Census Bureau, Florida 2020 resident population (21,538,187).** The fact is verified (census.gov "Florida Was Third-Largest State in 2020"); no BibTeX entry exists. Either add a `@misc` with access date or drop the literal from prose — as of now the QA sentence cannot be cited.
4. **The "FCDS 2024 monograph."** `config.yaml` credits it with the choice of noise rates. Resolved in substance (2026-09-24): the rates are the second author's own specification, "the same customization as in the FCDS 2024 monograph", so the monograph is FCDS's record-linkage monograph programme, which he leads. Still needed before it is cited: the exact title, year and URL (the 2023 supplement is `alexandersson2023splinkfcds`; the 2024 volume is not yet in `references.bib`).
5. **The FCDS published incidence rates in `reference/fcds_incidence_by_age_sex.csv`.** Hand-transcribed, headed "PROVENANCE — NEEDS CONFIRMATION BEFORE PUBLICATION", and its counts total 3.2M across 18 age groups, far more than one year of Florida incidence. Confirm the report title, the diagnosis-year span and the rate denominator, or drop that panel of Figure 1.
6. **Faker / commercial generators.** The author's 2026-08-08 Introduction outline names faker explicitly, so it is now cited as software (`faker_software`, trim tier) — package metadata plus an access date is the right form for a tool cited only to say what it does not do, and the "no error model, no cross-file identity" claim is verifiable against faker's own documentation. Commercial generators remain unnamed: the equivalent claim about them is still an unverified negative.
7. **The §2.1 simulation brief.** The author's summary (ACS + 2020 Decennial Census initialisation; twenty years of mortality/fertility/mobility from those sources and GBD) is authoritative but must be reconciled with the published description in Haddock et al. before print.
8. **The household partial-move behaviour** ("always a single person who moves to a new household or joins an existing one as an 'other nonrelative'") — the author's own [[double check]]; verify against the simulation code before §4.2 states it.
9. **The installs-vs-requests ratio** (pseudopeople PyPI installs ≈ 100× the access requests for the gated state/national files — the author's recollection, marked "check this"). **Demoted 2026-09-24:** the uptake-barrier framing left the abstract, Key Features, §1.3, §4.3 and §6, so nothing in the paper now needs this figure; it closes unless the author restores a monitoring clause in §6.
10. **The Census Bureau cooperative agreement** (number CB21RMD0160001, and whether it is the right instrument for the §7 acknowledgment).

---

## Work still to be done before rendering

Ordered by dependency. Items 1–3 must complete before any other number in the paper can be trusted.

1. **Commit what already exists — DONE (`ddd88c5`).** `config.yaml`, `pipeline/`, `results/` and `reference/` are tracked.
2. **Folded into `pipeline/build_cohorts.py` (2026-08-12).** The Florida-extract summary is written by the build script as `results/population_summary.json`: `fl_simulants`; `fl_share_census`; `pop_ssn_never` (the *population-level* never-had-an-SSN rate, distinct from the registry-measured rate). The registry duplicate-row count lands in `release_manifest.json`.
3. **`pipeline/build_cohorts.py` — DONE 2026-08-12: ported, then run twice on the cluster and verified.** Both acceptance tests passed — every design target exact, and the two runs produced byte-identical files (run-twice checksum identity). Built via `sbatch --wrap` (note: `srun` from inside an interactive session's allocation tries to create a job *step* in it and fails — use sbatch). `config.yaml` now points at v0.3. Original scope, for the record: The script covers items 2–4 end to end: weighted sampling with the five salted hash streams (salt strings identical to v0.2 so the draws are comparable), staged Parquet `ORDER BY simulant_id`, `stratified_trim` from `src/` in place of the notebook's buggy downsampling cell, the ordered SSA join with targeted SSN noise (now importable and unit-tested in `src/simulated_data_for_fcds_scale_rl/ssn_noise.py`), `race_ethnicity` carried into the released schema, GBD weights read from `reference/` instead of hard-coded, deterministic zip via fixed-metadata `zipfile` (no external `zip` binary), and the four `results/` JSONs. **Acceptance tests are asserted in-script: every design target hit exactly — overlaps 100,000 and 20,000, finder files disjoint — with hard failure otherwise; run twice and compare checksums for the identity test.** Run `srun --mem=120G -c 8 uv run python pipeline/build_cohorts.py` — never on a login node. On success, bump `dataset.version` to 0.3 and point `paths.release_dir` at the new release directory in `config.yaml` (both left at 0.2 for now so `pipeline/linkage_baseline.py` keeps running against the existing files).
4. **Folded into `pipeline/build_cohorts.py` (2026-08-12).** The build writes `results/release_manifest.json` (per-file rows, distinct simulants, overlap by both definitions — simulants and true pairs — byte sizes, MD5 **and** SHA-256, finder–finder overlap = 0, match prevalence 0.200 by design) and `results/error_rates.json` (realised missingness per targeted column per file, the structural-SSN floor, and the SSN-transposition count — measured at build time from the noise step itself, resolving the never-measured `err_ssn_transposed`), plus `results/environment.json` (versions, node, wall time, peak RSS; the three-way load benchmark still to be added there per item 9).
5. **Age/sex/race composition and top names — folded into `pipeline/build_cohorts.py` (2026-09-24).** The build writes `results/registry_age_sex.csv`, `results/registry_top_names.csv` and `results/age_sex_qa.json` for all three files from the source's true ages (the released files carry no age or year column, and with mixed record vintages a date-of-birth-derived age would be wrong), so the standalone `qa_age_sex.py` was removed. `pipeline/qa_source_age_sex.py` → `results/fl_census_age_sex.csv` (DONE 2026-09-24) gives the Florida pools by sex and FCDS age bin for the 2020, 2030 and 2040 censuses and the last-seen pool: the Florida-population panel of Figure 1 and the basis of the registry-size and pool decision.
6. **`pipeline/example_pair.py` → `results/example_pair.csv` — DONE 2026-09-24:** two pairs found deterministically, 1007_399543 (nickname Wes/Wesley, street typo, blank SSN) and 1534_695157 (month/day swap, adjacent SSN digits swapped), covering all four wanted mechanisms within pairs of at most four discrepancies; pin them with `--ids` on reruns. Original scope: search the overlap for exemplars showing a nickname or typo, a transposed SSN, a blanked address field, and a swapped month/day; pin the chosen `simulant_id`s so Table 2 is stable across reruns. Verify such exemplars actually exist before promising all four.
7. **`pipeline/data_forensics.py` → `results/forensics.json`.** Rescoped 2026-08-09 (the m/u probabilities are cut at the author's direction): quasi-identifier uniqueness shares and blocking candidate/completeness counts (§3.4 prose), most common first/last names per decision #17 (Table 3), date blank/parse rates, and the sentinel checks — Doe-pattern names, repeated-digit and SSA-non-compliant SSNs (§3.3), all per §2.5's definitions.
8. **Extend `pipeline/linkage_baseline.py`** (the plain re-run against v0.3 is **done 2026-08-12**; the extensions below remain). Add the current layout's *other* minimum combination (name + sex + DOB + ZIP + street address) as a tenth rule — the shipped files carry every field it needs, and without it the paper covers only half of FCDS's current submission floor. Compute the ladder within `race_ethnicity` strata → `results/linkage_baseline_stratified.json` (Figure 2), with true-pair counts per stratum. Record the node spec (cores, RAM) alongside `seconds`, or the timing claim must be dropped.
9. **`results/environment.json`.** Pseudopeople version used at generation time (the venv has 1.2.8, but dataset v0.2 predates it), Python version, DuckDB version, node spec, and the construction run's wall time and peak RAM — the numbers §4.1 needs to make any scale claim at all. Include the three-way load benchmark (full USA via pseudopeople; Florida via `state=`; Florida from the staged extract), wall time and peak RAM each — §2.1's friction narrative and §3.1's benchmark bullet both depend on it.
10. **Deposit and mint DOIs.** Build the deterministic zip, deposit on Zenodo, mint a dataset DOI and a code-archive DOI, and obtain the private reviewer access URL IJPDS requires at submission. The Data Availability Statement, the Data Access section, the abstract and Key Features cannot be finalised without these.
11. **Fix `paper.qmd` front matter and structure — partly DONE 2026-09-24.** Done: two authors with the full IHME address, ORCID and corresponding email; a docx-only chunk that rebuilds the affiliation block from the front matter (Quarto's docx template prints names only); the `Data Resource Profile:` title prefix; Key Features as an unnumbered six-bullet section backed by a load chunk over `results/` and `config.yaml`; the body headings in DRP order. Still to do: the abstract — it carries `{python}` placeholders, which Quarto does not evaluate inside YAML metadata, so either generate it in the body from a chunk with `output: asis` (as the author block is) or accept typed numbers there, against the convention; the second author's street address and ORCID; the back-matter statements per §7 (Acknowledgments, Ethics, COI, Publication Consent, Funding, Data Availability, Abbreviations, plus an AI Disclosure since this manuscript is AI-assisted); and verify `ijpds.csl` renders bracketed Vancouver numerals.
12. **Render once and commit `_freeze/` with `results/`.** Per `CLAUDE.md`, freeze hashes `paper.qmd` only and does not watch `src/`, `config.yaml` or data, so a render is required after every `src/` change and the two directories must be committed together.
13. **`pipeline/pair_agreement.py` → `results/pair_agreement.json` — DONE 2026-09-24.** Per-field agreement between the two records of each true pair for both finder files (Table 5), plus the two ladder summaries.
14. **`notebooks/v03_acceptance_checks.ipynb` — DONE 2026-09-24.** The receiver's-eye checks, executed against the v0.3 files: 37 pass, 0 fail, 12 notes — checksums against the manifest, layout and sizes, overlaps and the key, the second author's noise rates (including the ~1% visible SSN swaps and the 5.7% registry SSN floor), age/sex against his FCDS table from true ages, FCDS's minimum field sets (96.9% of finder records satisfy a Procedure Guide set, 92.5% a current-layout set, which follows from the 20% blank SSNs he specified), formats, names and race/ethnicity, the worked pair, deterministic sanity against Li et al., and provenance. Re-run after every rebuild; it is also the template for the deposit's QA section.

---

## Open decisions for the author

1. **Manuscript type — RESOLVED (2026-08-08): Data Resource Profile**, per the author; the journal's DRP guidelines are recorded in this outline and the structure above follows them. One residual check: the DRP word limit in the journal's Fee Structure table.
2. **Title:** adopt the recommended title above, or one of the three runners-up? **Which one?**
3. **Overlap definition:** report the overlap as distinct simulants in both files (recommended, with pairs footnoted), or as record pairs? **Simulants or pairs?**
4. **FCDS rule vintage:** foreground the 2007/2016 Procedure Guide rule, the current Data Linkage Record Layout rule, or both with the ambiguity stated (recommended)? **Which?**
5. **"Jo Lam's proposed quality metrics":** did you mean the missed-match / false-match framing of Lam et al. 2024, or the unpublished ITALO reporting work? If ITALO, there is no citable artifact yet. **Lam et al. 2024, or ITALO?**
6. **Noise-rate provenance — RESOLVED in substance 2026-09-24:** the rates are the second author's specification, quoted in the working notebook of 2026-02-02 ("I propose the same customization as in the FCDS 2024 monograph: Finder file: 20% missing SSN, 1% transposition error SSN, 5% missing Address; FCDS file: 5% missing SSN, 0% transposition, 1% missing Address"), so the paper attributes them to him and to FCDS's monograph work. Still needed: the monograph's exact reference (needs-verification #4), and his confirmation that the paper may quote the specification as his and that Table 5 looks like FCDS's real finder submissions. **Confirmed?**
7. **FCDS incidence table — now the registry weights (author's decision 2026-09-24), so its provenance is mandatory, not optional.** `pipeline/build_cohorts.py` draws the registry stand-in to the age/sex shares of this table's `count` column (`config.yaml`, `paths.age_sex_target`); the GBD prevalence table is demoted to the Figure 1 comparator. Still needed before publication: the exact FCDS report title, year and URL, the diagnosis-year span the counts cover, and the denominator and period of the rates — the second author supplied the table and can confirm these at source. The in-place v0.3 rebuild with this design ran 2026-09-24 (last-seen pool, exact quotas; 11 min, 24 GB peak): registry age/sex shares within 0.04 percentage points of FCDS's, largest share of any stratum taken 0.42 (men 70–74); `results/` describe these files. **Provenance confirmed?**
8. **Objection/redress mechanism:** do you commit to implementing a working one (targeted suppression plus a tombstoned version bump) on the deposit, or present it explicitly as an untested proposal? A salt change does not work — it re-draws which simulants are selected, not the names attached to them. **Commit, or present as proposal?**
9. **Licence:** CC0 (recommended — attribution stacking is impractical for benchmark data embedded in test suites) or CC-BY? **CC0 or CC-BY?**
10. **Conflict of interests:** disclose that you built pseudopeople, co-authored the source population, help govern access to it, and are named personally in the monograph recommendation that motivates this paper, and that the second author wrote that recommendation — or declare "None"? Recommended: disclose both. **Disclose or not?**
11. **`person_linkage_case_study` attribution:** have you confirmed with Zeb Burke-Conte that he is the author and is content to be cited? **Yes or no?**
12. **Attachment 9 conversion demo:** keep `lst-fcds-fixed-width` (requires writing the converter in `src/`) or cut it as the first casualty of the word limit? **Keep or cut?**
13. **Funding:** what grant supports *this* work, as distinct from the underlying population's Gates INV-060835 and Census CB21RMD0160001 — or is it "no specific funding"? **Which?**
14. **Acknowledgment by name — RESOLVED (2026-09-24): Anders Alexandersson is a co-author**, so no acknowledgment is needed. Residual: his affiliation wording, full street address and ORCID for the author block (Title, authors), and whether the second-author disclosure in §7 is worded to his satisfaction.
15. **Stratified equity results (Figure 2):** kept provisionally per the author (2026-08-09, "we'll see how it fits"). If the computed race/ethnicity differentials come out null, report the null (recommended — it is informative, and this outline pre-registers the mechanism being tested), or demote Figure 2 to one sentence? **Report the null, or demote?**
16. **Registry scope — RESOLVED 2026-09-24: expand.** The stand-in is drawn from the last-seen pool (every simulant ever recorded in Florida in the 2020, 2030 or 2040 census, once, at their last appearance) and the finder files from 2040 residents, so the registry includes people who have since died or moved away, as FCDS's caseload does; this is what makes FCDS's age/sex shares attainable at 5M (§2.2; `results/fl_census_age_sex.csv`: 37% of the tightest stratum against 101% from the 2020 census alone). Residual: state the vintage mix in §3.2 and the drawback in §4.2.
17. **Common-names table (Table 3) stratifier:** by race/ethnicity (recommended — it makes Figure 2's mechanism visible) or by birth cohort? **Race/ethnicity, or birth cohort?**
18. **A record-year column in the registry?** The acceptance notebook (§5) shows that a user cannot recover the registry's age pattern from dates of birth: records carry the vintage of a person's last census (27% 2020, 27% 2030, 46% 2040) and the released schema has no record year, so ages computed as of any one date are off by ten or twenty years for half the file. A real registry record carries a diagnosis date and a date of last contact, so a `record_year` column would be realistic and would let users compute age at record; the cost is a shortcut for linkers — every finder member's registry record is dated 2040, so filtering the registry to that year discards 54% of candidates and every true non-match among them. Options: add the column and name the shortcut in §4.2; withhold it and explain the age issue in the data dictionary; or add it with noise. **Add, withhold, or noise it?**