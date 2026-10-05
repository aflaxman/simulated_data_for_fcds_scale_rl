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

- **Details:** a simulated Florida drawn from the `{python} fl_pool` simulated people recorded as residents in the simulated 2020, 2030 or 2040 censuses, including a simulated registry of `{python} registry_rows` records whose age and sex distribution is that of the cases reported by the Florida Cancer Data System, and researcher finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records drawn from residents in 2040.

- **Data linkage:** the larger finder file includes `{python} overlap_500k_target` people who are also in the registry and the smaller finder file includes `{python} overlap_100k_target`. There is no overlap between the finder files.

- **Main categories of data:** simulated person-level identifiers including name, date of birth, sex, street-address fields, SSN, race/ethnicity, and a diagnosis date on each registry record, carrying plausible synthetic noise (typos, nicknames, month/day swaps, blanks, duplications).

- **Access:** direct download under a permissive licence with a DOI.

---

## Structured abstract (draft, 292 words counting each `{python}` placeholder as one word and excluding the four headings — recount before submission; ≤300 permitted)

The Data Resource Profile abstract keeps four headings but assigns each dataset-first content: **Introduction** = a brief summary of the dataset; **Methods** = how it was created, original sources, linkage; **Results** = where it is held, contents, quality; **Conclusion** = how to access, suggested uses, ongoing improvements. The pipeline-lessons conclusion of the Data Note draft is retired. Each `{python}` placeholder is counted as one word.

> **Introduction**
> We present a simulated resource for developing and benchmarking cancer-registry record linkage: a simulated registry and two researcher finder files at the scale of the linkage workload in the Florida Cancer Data System (FCDS). This will allow linkage software to be evaluated on fields such as names, dates of birth, addresses and Social Security numbers (SSNs), which are typically unavailable to outside researchers due to confidentiality. Our simulated data includes a ground-truth identity key, so precision, recall, and other quality metrics can be calculated exactly after the data has been linked.

> **Methods**
> We started with the simulated United States population that was developed for pseudopeople and extracted the `{python} fl_pool` simulated people ever recorded as Florida residents in its 2020, 2030 and 2040 censuses, each at their last appearance, so that the pool, like a registry, includes people who have since died or moved away. We then sampled a simulated registry of `{python} registry_rows` records with the age and sex distribution of the cases FCDS reports, as well as finder files of 2040 residents with `{python} finder_500k_rows` and `{python} finder_100k_rows` records with exactly `{python} overlap_500k_target` and `{python} overlap_100k_target` people overlapping the registry (and no overlap between finder files). We used keyed-hash sampling and a stratified trim to make each file a reproducible random sample and used noise functions from pseudopeople together with additional noise to supply realistic errors.
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
- *Lingo:* Key Features calls the 5M file "a cancer registry"; the abstract and §1.2 call it the "simulated registry". Pick one; the lingo rule favours the latter.
- *Numbers:* every placeholder still resolves to the 2026-08-12 GBD-weighted build until v0.3 is rebuilt in place with the FCDS weights (decision #7; the number stays 0.3 because nothing was released); `registry_rows` and the SSN-missingness sentence in Results must be re-checked after it.

---

## 1. Background

*Combined target ≈ 700 words. A Data Resource Profile has **no Introduction section in the body**: the four-heading abstract carries the summary, and the body opens with Background — "a detailed overview of the rationale for creating the dataset and the various sources of data from which the resource was created." The author's four introduction beats survive intact as the Background's arc (big-data hypothesis → confidential-data barrier → simulated-data lineage → low-barrier objective), followed by the sources overview the genre asks for. Spell out "record linkage" throughout — to most readers "RL" means reinforcement learning, and the abbreviation should not appear in the paper.*

### 1.1 Rationale: record linkage under the "big data" hypothesis, and the data it cannot get — ¶2 (~180 words)

- Open on the hypothesis, one sentence: much of what population data science promises rests on the claim that existing data sources — administrative, clinical, registry — can yield insights without new, expensive and time-consuming data collection [@harron2017challenges]. Record linkage algorithms are a load-bearing ingredient of that claim, because reuse means combining sources never designed to be combined, and when linkage is wrong everything downstream inherits the error [@doidge2018demystifying].
- Then the concrete instance, kept from the previous draft because it is still the best ratio in the paper: Florida's reporting facilities send FCDS more than 310,000 case reports a year, which must resolve to roughly 145,000 newly diagnosed cases; the registry also links incidence to the state mortality file for passive follow-up [@fcds_welcome]. Cite with access date — the page carries no as-of date. Recognising that two differently spelled records describe one person *is* the product.
- The barrier, the outline's second beat: the identifiers linkage software runs on are exactly what confidentiality rules prevent from leaving the registry, and NAACCR states plainly that restrictive and varying state policies limit onward sharing of registry-derived data [@naaccr2023secondarysharing] — so testing stalls, and adoption follows. Three consequences, one clause each: separating linkage from analysis makes linkage a black box whose reliability researchers struggle to judge [@harron2017challenges]; access, where granted, is slow and costly — one 224,000-member occupational cohort spent about 700 hours and $22,440 over five years obtaining approvals and matches from state registries [@buchanich2009methodological]; and even a researcher who clears every hurdle gets no answer key, because real registry data carries no ground truth for which candidate pairs are the same person, so accuracy can only be estimated [@harron2017guide].
### 1.2 The transaction the dataset imitates — ¶1 (~120 words)

- Define "finder file" once, here, and never again: a researcher submits a cohort's identifiers, FCDS links them against the statewide incidence file, and returns matched records. **Lingo fixed per the Procedure Guide (author, 2026-08-09):** *finder file* = the researcher-submitted cohort; the two released 500k/100k files are the finder files; the 5M file is the *simulated registry* (statewide incidence file). Never call the registry a finder file — the author's working outline used "master database"/"match files", which must not survive into the draft. **This is the only place the FCDS minimum-fields rule is stated** — Methods refers back to it. State both vintages, because they differ and no document establishes which supersedes: the 2007/2016 Procedure Guide requires first + last name AND SSN AND sex, *or* first + last name AND month and year of birth AND sex [@fdoh_fcds_procedure_guide_2007]; the current Data Linkage Record Layout requires name + sex + DOB + SSN, *or* name + sex + DOB + ZIP + street address, in a fixed-width ASCII record [@fcds_linkage_layout]. The released files satisfy either. **\"Simulant\" (author's rule, 2026-09-25):** pseudopeople's word for a simulated person; introduce it once, in quotes, where `simulant_id` is first explained (§3.1), then write \"people\" or \"simulated people\" in prose, keeping \"simulant\" for the identifier itself and for reminders that no real person is involved. The Key Features and abstract follow the same rule.
- One sentence of friction, not a table (see the display-item budget): identifiable FCDS data requires serial DOH IRB and Cancer Registry Review Committee approval with notarized confidentiality pledges and destruction on completion [@fdoh_fcds_procedure_guide_2007]; linkage runs onsite only and carries a sliding fee schedule [@fcds_data_release_procedures; @fcds_fees_2020]. **Attribute turnaround figures to their vintage** ("per FCDS's 2017 release procedures") — the digest marks current times as unverified. This bullet now does double duty: it is §1.1's "expensive and time-consuming" claim made concrete for FCDS, so the vintage attribution has to be exact.

### 1.3 Simulated data is the proposed fix, and why the shelf is bare — ¶2 (~150 words)

*Compressed from a full page in the Introduction draft plus a duplicate subsection and table in the Discussion draft, now organised along the author's two failure axes: **not realistic enough**, or **not openly available at registry scale**. The comparator landscape is stated **once, here**, in prose. `tbl-prior-benchmarks` and `tbl-benchmark-comparison` stay cut.*

- Axis one, realism and scale. Generic fake-data tools such as faker produce clean, plausible, unlinked records — no error model, no cross-file identity, so no linkage testbed [@faker_software]. Linkage-specific generators model the right errors at the wrong scale: in the only controlled head-to-head benchmark, only three of five tools exceeded one million records, GeCo needed about 13 hours to corrupt one million and produced nothing at ten million [@hildebrandt2020dapo]; the shipped FEBRL and SOG corpora are counted in thousands [@christen2008febrl; @tran2013geco; @talburt2009sog], and the public benchmark inventory confirms the pattern [@binette2022almost].
- Be scrupulous about the counter-examples, because a reviewer will be: the largest openly downloadable person benchmarks are real North Carolina voters — 10M records with as few as four attributes, excluding children, so age-structured opposite to a cancer registry [@saeedi2018famer]. The one prior ~20M-person microsimulation built to study linkage quality does not appear to have been released [@schnell2023microsim]. The only cancer-registry benchmark ships precomputed comparison vectors with no names or dates, so it cannot exercise blocking or string comparison [@schmidtmann2011krebsregister]. Synthea publishes a million rich synthetic patients but no identifier-error model and no cross-file ground truth [@walonoski2018synthea].
- Axis two, access — pseudopeople's slot in the lineage, stated as fact and without the uptake-barrier apparatus that the abstract and Key Features no longer carry (2026-09-24): pseudopeople clears the realism and scale bar (a simulated US population with a ground-truth identity key [@haddock2024simulated]), but the population it ships openly is a ~10,000-simulant sample and its state- and national-scale populations are available only on request [@keyes2026governance]. Then the project's own history, as history rather than as external endorsement now that its author is the second author: the 2023 FCDS Splink feasibility study ran on a 1,000,000 × 1,000,000 synthetic test file supplied privately by the first author, noted that "the datasets are not yet publicly available", and recommended making the test data public [@alexandersson2023splinkfcds]; the published follow-up comparison of fastLink, Match\*Pro and Splink ran at Rhode Island scale, roughly one twentieth of the population FCDS serves [@alexandersson2024comparing]. This dataset is the public release that study asked for, built as a new and larger corpus rather than a release of the file it used (the reviewer's "fulfillment" objection stands; say "responds to"). **Retired from the paper (2026-09-24):** the "appears to be a barrier to uptake" hedge, the installs-vs-requests ratio (needs-verification #9), and the monitoring "experiment" (§4.3, §6); the plain statement above replaces them. The data-access thread, public on GitHub since 2023 [@pseudopeople_issue205], records the whole lineage — the 2023 request for Rhode Island-scale data with more SSN and date-of-birth noise, the 2024 monograph on about 700,000 records, the 2025 request for Florida-specific data, and the January 2026 specification of the 5M/500k/100k design, the 20% overlap and the noise rates — so cite it once as the provenance of the design and do not paraphrase it as history.
- **Do not mention "GeCo3"** — it is an unrelated DNA compressor. Do not name commercial vendors; the digest marks that as an unverified negative. And note the positionality edge: describing pseudopeople's access process is the first author describing his own project, and the FCDS history is the second author's own work — §4.4's positionality sentence must cover both.

### 1.4 Objective, and the sources this resource is built from — ¶2 (~180 words)

- The objective sentence, close to the author's outline wording and in step with the abstract's Introduction: we set out to make a low-barrier dataset for record-linkage research and development at the scale of the Florida cancer registry's typical linkage challenge — a direct download with a DOI, no application, no approval, and a published ground-truth key — so that linkage software can be evaluated on the fields that are confidential in real data and typically unavailable to outside researchers. ("Extremely low-barrier" is retired; the mechanics say it.)
- The author's tension sentence (2026-08-09), one clause, planted here and delivered in §4.4: even though the data are fake, they look real enough to risk doing harm — valid-looking SSNs, synthetic-identity seed material, addresses that must not be geocoded.
- Close the Background with the sources overview the genre requires, one sentence each: the **simulated United States population developed for pseudopeople** (the abstract's name for it; thereafter "the source population") — an individual-based microsimulation initialised from American Community Survey public-use microdata, carrying `simulant_id` as ground-truth identity across all its observers [@haddock2024simulated; @pseudopeople_software]; **FCDS's reported cases by age and sex**, the registry's age/sex target (§2.2), with GBD neoplasm prevalence for Florida as the QA comparator only; and **FCDS's published submission layouts**, the design template for the schema and the deterministic rules [@fdoh_fcds_procedure_guide_2007; @fcds_linkage_layout].
- What the paper reports, in the author's tripartite order: (1) the data resource — an incidence-weighted simulated registry and two finder files with exactly known overlap; (2) the process of its development — the seeded, checksummed pipeline, additional noise at the rates the second author specified from FCDS's monograph work (§2.3), and the trim bug that scoring against the ground-truth key caught before release; (3) a difficulty portrait and demonstration usage — quasi-identifier uniqueness, data forensics, and deterministic baselines overall and stratified by race/ethnicity (§3.3–§3.4).
- Still deliberately *not* re-quoting the counts that Results owns — the exact overlaps and file sizes stay out of the Background entirely. The generalisation sentence (illicit-drug epidemiology, social work, economics) stays in §6; it duplicated the planned Conclusions.

---

## 2. Methods

*Target ≈ 850 words across five subsections — the Data Resource Profile asks Methods to detail the original sources, the linkage methods, and the study population.  Load order: `paper.qmd` must open with a setup chunk reading `config.yaml` into `cfg` and the `results/` summaries into `lb`, `pop`, `err`, `rel`, `forensics`, `strat` before any inline expression resolves.*

Notes on what goes in methods section, based on read-through of Reesults section:

Descriptions and reference to pseudopeople data note, explaining that it offers a simulated decennial census for 2020, 2030, and 2040, at full scale.  We restricted this to simulated individuals living in Florida to create the sample frame for the registry.  We sampled from the 2040 decennial census population of Florida to create the finder files.

description of the approach to making things faster (some relevant notes below).

Describe the columns included


Every row of each file carries a `simulant_id`, the identifier of the simulated person it describes; the same identifier in two files means the same person, and this is the ground truth against which any other linkage of the files can be scored. The files also contain the fields that record linkage typically relies on: first name, middle initial, last name, date of birth, sex, race/ethnicity, street number, street name, unit number, city, state, ZIP code and social security number (SSN). Registry rows also carry a diagnosis date, which we placed on a day within the year of the census the record was drawn from, so that diagnoses fall in 2020, 2030 or 2040 only. Addresses carry real Florida cities and ZIP codes but simulated street addresses that are not real street locations. 



Describe strategy to sampling finder files to get precisely number of simulants desired, and 20% overlap between finder file and registry (and make finder files disjoint).

Describe noise strategy, including params for pseudopeople, and the custom ssn swap added after the pseudopeople call completed.


A registry row and a finder row that carry the same identifier are a "true pair", the unit on which every linkage result below is scored; the larger finder file holds `{python} overlap_500k_pairs` true pairs and the smaller `{python} overlap_100k_pairs`, and every other pairing of a registry row with a finder row is a true non-match. Every finder record is drawn from the 2040 census, and so is the registry record of every person who appears in a finder file; people last seen in 2020 or 2030 appear in the registry alone (@sec-discussion).

We examined demographic distributions of the registry and finder files to confirm that they matched expectations.  We also examined the most common names for different age groups as a face validity check, and spot checked a subset of matching records between the registry and finder files.

We calculate the missingness for each field, as well as the exact match rate for pairs that appear in the registry and the finder file. We also tallied how many SSNs had two digits swapped (a noise type that is not yet implemented in pseudopeople).  We also counted the number of invalid SSNs.  (anything else in results that needs to be set up in the methods section?)

To start to understand the linkability of these files, we counted the population-uniques for multiple sets of attributes, and also measured the precision and recall of a range of deterministic linkage strategies (e.g. exact agreement on first name, last name and date of birth).  Finally we measured the number of comparisons induced by some simple blocking rules.



Previous ideas for methods section, see if anything in here is worth incorporating, too.  At least some of the references should be useful additions.

### 2.1 Source population and the Florida extract — ¶3 (~220 words)

- The simulation is described in detail elsewhere [@haddock2024simulated; @pseudopeople_software]; give the author's own brief (2026-08-09), reconciled with the published description (needs-verification #7): a population initialised with the size and demographics (age, sex, household structure) of the 2020 United States from publicly available American Community Survey and 2020 Decennial Census data; mortality, fertility, and mobility modelled over twenty years from those sources and the Global Burden of Disease Study; and fully simulated versions of the confidential fields linkage runs on — names, dates of birth, addresses, SSNs — recorded for use with the pseudopeople Python package. The underlying large-scale populations are available through a lightweight approval process [@keyes2026governance]. Record the artifact name `pseudopeople_simulated_population_usa_2_0_0` (not the internal `release_02_yellow` tag), the Vivarium microsimulation `vivarium_census_prl_synth_pop` with `simulant_id` as ground-truth identity across all observers, the pseudopeople package version, and DuckDB `{python} duckdb_version`.
- The friction narrative, in the author's voice and with numbers behind it: using the full-USA data was possible but slow, and even pseudopeople's existing affordances for loading a single state with distributed computing were a barrier — so we built a Florida-only extract with DuckDB, using AI-assisted coding by Claude (disclosed here and in the back-matter AI Disclosure). The three-way load benchmark in §3.1 is the evidence; without those numbers this paragraph makes no claim. What stays true and verified about the affordances (pseudopeople 1.2.8): `generate_decennial_census` *does* take `state=`/`year=` and has a Dask engine — never claim otherwise, the first author is a pseudopeople co-author and a reviewer will catch it; `generate_social_security` has **no** `state` parameter, so the SSN join is by hand; and there is no API for prevalence-weighted or overlap-controlled sampling, which is the whole cohort design.
- Extraction mechanics: DuckDB reads the census-observer Parquet directly, keeps the Florida rows of the 2020, 2030 and 2040 censuses (`cohorts.census_years`), one per simulant per census, and builds two pools: the *last-seen pool* — every simulant ever recorded in Florida, once, at their latest census, `{python} fl_pool` people — from which the simulated registry is drawn, and the residents of `{python} finder_year` (`{python} fl_finder_pool` people), from which the finder files are drawn. (Redesign 2026-09-24, decision #16: a registry keeps people who have since died or moved away, and the 2020 census alone cannot supply FCDS's age/sex pattern at 5M.) The 2020 census count, `{python} fl_simulants`, is kept only for the external-scale check in §2.4. SSNs come from the Social Security observer joined on `simulant_id`; `race_ethnicity` is carried through from the census observer into the released schema (new in v0.3) — FCDS's own submission layout carries race, so the column is transaction-faithful, and it is what §3.3–§3.4's stratified statistics stratify on.
- **Scope statement (moved here from the Results draft, 2026-09-24, per the author):** Florida only, at city and ZIP granularity, with simulated street addresses that are not geocodable; registry records dated by a diagnosis year of 2020, 2030 or 2040 (their census vintage), finder files describing residents of `{python} finder_year`; no county, tract or facility identifiers and no tumour variables (§4.2). Also here (moved from §3.2): the source population's households share surnames and addresses by construction, so address- and surname-based blocking meets realistic co-residence collisions [@haddock2024simulated]. **Pointers from Results (2026-09-25 review):** §3.1 now says the pool is 50.5M people "counted across three censuses twenty years apart and including people who died or left the state between them" and points here; this bullet must explain the last-seen pool plainly enough that the number stops looking like an error (Florida has about 22M residents at any one census). §3.1 also says addresses carry real Florida cities and ZIP codes but simulated streets; state where each comes from in the source population (real place names and ZIP codes, synthetic street numbers and names) [@haddock2024simulated].
- Two-tier note: this is pipeline-tier code run manually; nothing in the rendered paper executes it. The benchmark numbers replace conjecture — no unmeasured "cannot load even one state" claims.

### 2.2 Cohort design and reproducible sampling — ¶3 (~180 words)

- Design in one paragraph, targets from `config.yaml`: a simulated registry targeting `{python} cfg_registry_target` records with the age and sex distribution of the cases FCDS reports, and two finder files targeting `{python} cfg_finder_500k_target` and `{python} cfg_finder_100k_target` records with `{python} overlap_500k_target` and `{python} overlap_100k_target` overlapping simulants. The target is the `count` column of `reference/fcds_incidence_by_age_sex.csv` (`config.yaml`, `paths.age_sex_target`), 18 age bins by sex, taken as shares; each stratum contributes an exact quota (`allocate_by_share` in `src/`: largest-remainder rounding, capped at the stratum's pool size), filled by the smallest keyed hashes within the stratum, so the registry's age/sex shares equal FCDS's to within the rounding of the noise trim (`results/age_sex_qa.json` records the largest deviation). **Redesigned 2026-09-24:** the 2026-08-12 build weighted a random draw by GBD prevalence; the first FCDS build the same day weighted it by incidence rates, which at a 36% oversample fraction compressed the ratio between strata (§3.2); exact quotas remove that, and the last-seen pool (§2.1) makes 5M attainable at 37% of the tightest stratum where the 2020 census alone could not (men 80–84 would have needed 101%). The GBD table stays in `reference/` as the Figure 1 comparator. The 20% overlap is the second author's specification [@pseudopeople_issue205]: finder-file overlaps at FCDS are often near 20% or lower, smaller overlaps are too unstable to benchmark, and 20% is the "small overlap" case of Enamorado et al. (needs-verification #11 for the citation). The GBD prevalence weighting of the 2026-08-12 build was the first author's proposal of 2026-02-05, accepted by the second author in the same thread; the return to FCDS's case shares is the first author's call of 2026-09-24 and should be stated as such. **Pointer from Results (2026-09-25):** §3.1 says "the 20% overlap was chosen to mirror the finder files FCDS receives" and points here; keep the second author's rationale in one sentence with the Enamorado citation (needs-verification #11).
- Why FCDS's case shares, and why a pool with the dead in it, in two sentences with the drawback beside the choice: the registry's own reported caseload is the age/sex pattern a linkage against FCDS meets, and a registry keeps every case it registered, including people who have since died or moved away, so the simulated registry is drawn from everyone ever recorded in Florida across the three simulated censuses, each at their last appearance, which is why we prefer it; the cost is that registry records carry the vintage of a person's last census (2020, 2030 or 2040), realistic for a registry but no longer a snapshot of one year's residents, and that three censuses span twenty years where FCDS's caseload spans four decades. GBD all-neoplasm prevalence for Florida is the independent comparator for the *shape* check in §2.4. Drop the unverified conjectures about "name eras" and "address stability" — the sufficient rationale is matching the registry's age/sex structure to Florida cancer demography.
- **Add the load-bearing fact all five drafts omitted:** overlap members are drawn from the registry cohort and the remainder from outside it via separate hash streams, and the two files are then noised *independently* (`psp_registry` seed `{python} cfg_seed_registry`, `psp_finder` seed `{python} cfg_seed_finder`). That independence is what makes this a linkage problem rather than a join. **Define overlap here, once (moved from §3.1, 2026-09-24):** distinct simulants present in both files; true record pairs are reported separately as the recall denominator, and in v0.3 the two coincide.
- **The true pairs are same-year records — say so, and weigh it (2026-09-24).** Overlap members are registry members whose last census is the finder year, so a true pair's registry row and finder row are the *same source record noised twice*: no move, no aging, no surname change lies between them. This is the simplest choice and the easiest case a linkage can face, and it is why address agreement among true pairs is `{python} agree_street_name_500k` (§3.3) where a real registry sees far less. The pool keeps every census year, so drawing the registry record of an overlap member from an earlier census than the finder file is a change to the overlap draw alone — the address-change extension of §4.3.
- Reproducible randomness, **stated once here and not restated in the Discussion**: DuckDB's `random()` is not reproducible across threads, so every draw is made a pure function of the record key — the Efraimidis–Spirakis exponential-race key with the uniform replaced by a keyed hash. Quote the expression exactly, including the constant `18446744073709551617.0` (= 2⁶⁴+1); the Discussion draft's "2^64" is a paraphrase, and a section whose claim is bit-identical checksums cannot paraphrase the formula that produces them. Five salts give independent streams from seed `{python} cfg_seed_sample`. In prose the plain term is the abstract's — each file is "a reproducible random sample" — and "a pure function of the seed" appears once, as the mechanism.
- **Add the most reusable pattern in the pipeline, which no draft stated:** row-level omission noise deletes rows, so exact targets are unreachable in one pass; cohorts are drawn at `{python} cfg_oversample`× target and trimmed back afterwards with `numpy.default_rng({python} cfg_seed_postprocess)` over sorted ID lists. The trim must be *stratified* — exactly the target number of overlap members, filler drawn from survivors outside the entire overlap pool, the registry keeping only the chosen members (`stratified_trim` in `src/simulated_data_for_fcds_scale_rl/downsample.py`, unit-tested in `tests/test_stratified_trim.py`). The v0.2 build trimmed unstratified and overshot its overlap targets by a third; §3.1 tells that story in two sentences as evidence the ground-truth QA loop works. Note the reason for oversampling is that the number dropped is *not known in advance*, not that noise is nondeterministic (it is seeded and deterministic; that determinism is the point of §2.2's row-order fixes).
- The two silent order-dependence bugs, one sentence each: the staged Parquet must be written `ORDER BY simulant_id` because pseudopeople walks rows in file order, and the SSA join must be sorted before numpy selection. The run-twice assertion moves to `tests/`, mentioned in half a sentence; `lst-weighted-sample` is cut.

### 2.3 Noise, schema and packaging — ¶2 (~80 words)

- Base layer: pseudopeople's full default suite, each mechanism at 1% per cell per file, so a first name carries six mechanisms (blank, nickname, fake name, phonetic, OCR, typo), a date of birth six (blank, copied from a household member, month/day swap, wrong digits, OCR, typo), a last name five; row noise is 1.45% non-response plus duplication of some children. Additional noise (the abstract's term; never "overrides") from `config.yaml`, values never typed: finder files `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` SSN transposition, `{python} cfg_finder_address_missing` on each address field; registry `{python} cfg_registry_ssn_missing` / `{python} cfg_registry_ssn_transposed` / `{python} cfg_registry_address_missing`. **Provenance resolved 2026-09-24:** these are the second author's specification, quoted in the working notebook of 2026-02-02 — "I propose the same customization as in the FCDS 2024 monograph: Finder file: 20% missing SSN, 1% transposition error SSN, 5% missing Address; FCDS file: 5% missing SSN, 0% (no) transposition error SSN, 1% missing Address" — so the paper states them as FCDS's own characterisation of a finder submission against its consolidated file, attributed to the second author, and cites the monograph once its reference is confirmed (needs-verification #4); it does not defend them as realistic beyond that. Rationale in one clause: a researcher's finder file is dirtier than a certified registry's consolidated file [@qiao2023lexisnexis].
- Adjacent-digit SSN transposition is not in pseudopeople's noise taxonomy, so it is a post-hoc numpy step — the concrete affordance gap §4.1 generalises.
- **Two mechanism sentences moved from Results (2026-09-24):** (1) missingness is set by target *count*, not an independent Bernoulli draw — the finder files' structural rate sits below their 20% target so the pipeline tops them up to exactly 20%, while the registry's structural rate already exceeds its 5% target so nothing further is blanked: one mechanism, two outcomes; (2) pseudopeople's duplicate-with-guardian row noise, which copies a child's or student's record at a guardian's address and so gives one person two rows, is switched off (`noise.duplicate_with_guardian: 0.0`, v0.4, 2026-10-01), so every file is exactly one row per person and the build asserts it. It touched the v0.3 registry only twice among five million people and the 100k finder file once, which no user could test, and within-file duplicate detection is out of scope anyway (§4.2). **Say here, because it is not obvious:** switching any pseudopeople noise type off re-draws the cell noise across the whole file, since the cells to noise are chosen by a binomial draw over the number of eligible rows; v0.4 is therefore a fresh realisation of the same design and rates, not v0.3 minus three rows (measured on the sample population 2026-10-01: about half of all records change). Street numbers are blank above the set rate because some source addresses carry none, and unit numbers are blank for most addresses by construction.
- **What the noise does not include, stated here and weighed in §4.2:** the SSN carries no wrong-digit or borrowed-number errors beyond the transposition (pseudopeople does not noise the SSN column in the census, so `{python} agree_ssn_500k` of true pairs with both SSNs present agree exactly); there is no surname change at marriage, because the two records of a true pair are the same year's record (§2.2); noise is symmetric between files and independent across fields, where real finder files have systematic habits (a cohort that recorded nicknames, SSNs typed from memory); and both files share one format exactly. These are the four structural ways the benchmark is easier than a real linkage. The second author's own 2023 request said real finder files carry 3–5% SSN errors — typos, transpositions and a family member's number [@pseudopeople_issue205] — so the pristine SSN is a known simplification of his later specification, not an oversight, and the extension in §4.3 is his ask.
- Published columns: `simulant_id` plus first name, middle initial, last name, date of birth, sex, street number, street name, unit number, city, state, ZIP, SSN, and (from v0.3) race/ethnicity. **The registry alone also carries `diagnosis_date` (added 2026-09-24):** a day drawn uniformly within the record's census year by keyed hash (`seeds.diagnosis_date`), so age at diagnosis, computable from the released fields, is within a year of the age the FCDS target was matched on; a finder file is a cohort roster and carries no such date. Dates heap on 2020, 2030 and 2040 by construction (§4.2). Say the release covers **all fields required by either minimum matching rule, plus race** — not "exactly the fields FCDS requires", since the current submission layout also carries maiden name, full middle name, alias and birthplace. `tbl-schema-layout` is cut as repo documentation. **Data-user facts a reviewer asked for (2026-09-25), to state here and in §5:** UTF-8 CSV with a header row; blanks are empty fields, never a sentinel; fields are quoted only when they contain a comma, which is rare enough that DuckDB's sniffer infers no quote character and fails unless it is named (§4.2 names this); dates are `MM/DD/YYYY`; SSNs are `ddd-dd-dddd`; the deposit should carry a data dictionary (field, type, blank convention, noise applied) alongside the manifest and `config.yaml` — write it as run-list item 16. §3.1 points here for the diagnosis date's three years: say that each registry record takes the year of the census it comes from and the date is a day within that year.
- Deterministic archive: zip built with `-X` and fixed member timestamps so archive metadata is deterministic; checksums published for the three CSVs and the bundle. Dataset version `{python} dataset_version`; `config.yaml` is the single source of truth.

### 2.4 Quality assurance and the linkage baseline — ¶2 (~90 words)

- QA check 1, external scale: the extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents (a cited literal — **needs a Census Bureau citekey**).
- **QA check 0, reproducibility (moved from §3.1, 2026-09-24):** MD5 and SHA-256 digests for each file and the bundle are published so a user can prove the file in hand is the file profiled; the build is a pure function of `config.yaml`'s seeds; and the run-twice identity test passed for the current design on 2026-09-24 (`results/run_twice.json`: a second build on another node reproduced all three CSVs byte for byte; the zip differs only by its archive prefix). Results states the fact in one sentence; the argument lives here. **Say what a rebuild needs (2026-09-25 review):** the archived pipeline and `config.yaml` are open, but the input they run on, the pseudopeople full US population, is available only on request [@keyes2026governance]; §3.1 now reads "a second build from the same configuration and the same source population, which is available on request" and points here. Name this honestly as the one non-open input: a user can verify the digests and rerun every linkage experiment on the released files without asking anyone, and can rebuild the files themselves only after the request. §4.4 owns the argument for why that is acceptable.
- QA check 2, registry demography: the realised age/sex composition of each file (from the source's true ages, written by the build as `results/registry_age_sex.csv`) against the FCDS case shares the registry was drawn to — `results/age_sex_qa.json` records the largest deviation of any stratum share from its target, expected within the rounding of the trim — against the simulated Florida pools (`results/fl_census_age_sex.csv`), and against GBD all-neoplasm prevalence for Florida as an independent comparator. Agreement with FCDS is a check of the sampler, not of fidelity, and the caption must say so. The FCDS table's provenance is now load-bearing — it is the Methods input, not an optional panel — and its header still reads "PROVENANCE — NEEDS CONFIRMATION BEFORE PUBLICATION"; the second author supplied it and can confirm the report, diagnosis-year span and denominator at source (decision #7). Until then the paper describes it as an FCDS age/sex table of reported cases with its confirmation status stated. **Wording (2026-09-25 review):** §3.2's sentence that the registry's shares are within 0.041 pp of FCDS's reads as a finding; a reviewer will credit fidelity that was given by design. The honest verb is "the sampler reproduces the target to within 0.041 pp in every stratum" — the author's call in §3.2, and the caption already says "by construction".
- Define passing so it is falsifiable, and **do not use monotonicity**: verified against the committed FCDS file (2026-09-24), the female rate peaks at 80–84 (1,839 per 100,000) and falls at 85+ (1,732), the male rate peaks at 75–79 (2,754), is flat at 80–84 (2,753) and falls at 85+ (2,676), and the male rate at 5–9 (13.9) is below 0–4 (24.5), so "rises monotonically with age" is falsified by the paper's own inputs. The sex pattern crosses twice: female rates exceed male from 20–24 through 50–54, male rates exceed female from 55–59 up. The criterion for the GBD comparator is agreement in peak band and in those crossovers, not in level — the registry matches FCDS case shares by construction while GBD estimates prevalence, so the comparator panel differs in level by design.
- Baseline: each rule is agreement on every key of a key-set, evaluated as DuckDB hash joins (disjunctions as UNIONs, avoiding a nested loop over ~5×10¹¹ pairs). Do not enumerate the ladder in prose — that is the Results table. Metrics: precision and recall, reported also as false-match and missed-match rates after Lam et al. [@lam2024synthetic]; F1 is computed but not used to rank, per the F-measure critique [@hand2018fmeasure]; specificity and accuracy are omitted because true non-matches grow quadratically [@christen2007quality]. Deterministic linkage is a legitimate floor, not a straw man — the distinction from probabilistic methods is largely one of implementation [@doidge2018demystifying], and SEER–Medicare runs a deterministic algorithm in production [@enewold2020seermedicare]. **Do not import SEER–Medicare's ~96% as a linkage-accuracy figure** — it is the share of SEER persons 65+ found in Medicare enrolment.
- **Cut from Methods entirely:** the headline-foreshadowing bullet (those numbers appear once, in Results) and the "optional, not yet run" linked-vs-unlinked extension.

### 2.5 Characterising the data: forensics and difficulty — ¶1 (~90 words)

- Define the measures once, here; Results reports the numbers. **Cut 2026-08-09: the m/u-probability table** — the author rules the Fellegi–Sunter framing a distraction from the paper's point; nothing may reintroduce it. (1) **Quasi-identifier uniqueness**: the share of registry simulants unique on first+last name+DOB, on last name+DOB, and on ZIP+DOB+sex, plus the count of distinct simulants sharing a full name. (2) **Data forensics**, per the author's outline: most common first and last names (stratifier per decision #17); per cent of dates blank, and of non-blank dates that fail to parse; sentinel checks — "John Doe"-pattern names, repeated-digit SSNs such as 111-11-1111, SSNs violating SSA issuance rules. (3) **Stratified baselines**: the §2.4 ladder recomputed within `race_ethnicity` strata. Noise injection is race-uniform by design, so any differential is inherited from population structure — chiefly the race/ethnicity-conditioned surname sampling of the source population [@haddock2024simulated]; the fidelity caveats live in §4.2. (4) **Blocking feasibility**: candidate-pair counts and ground-truth pairs-completeness under blocking on full DOB and on last-name initial plus birth year.

---

## 3. Results

*Target ≈ 1,100 words. Genre spec: "a detailed description of the dataset created including its structure, characteristics (e.g. demographic, clinical, social) and data quality." The pivot (2026-08-08): Results is a **difficulty portrait**, not an inventory plus confessions — every number here should predict something about a user's experience. Four subsections: structure, population characteristics, error structure, linkage difficulty.*

### 3.1 Structure, contents, and where the data are held — ¶3 + Table 1 (drafted in `paper.qmd` 2026-09-24; ¶1 is the author's)

- ¶1 (author's): three CSVs on Zenodo under a DOI (run-list item 10), described in Table 1; a simulated registry of `{python} registry_simulants` people and finder files of `{python} finder_500k_simulants` and `{python} finder_100k_simulants` people, drawn from a pool of `{python} fl_pool` Florida residents of the simulated 2020, 2030 or 2040 census.
- ¶2, contents: every row carries `simulant_id`, the same identifier meaning the same person in all three files, the ground truth any linkage is scored against; the released fields; the registry's diagnosis date (2020, 2030 or 2040); Florida addresses to city and ZIP with simulated streets; each data file exactly one row per person since v0.4 (stated in Table 1's caption and asserted in the load chunk; the duplication mechanism and its switch are §2.3's). **Table 1 (2026-10-01)** drops the People column, since rows equal people, and gains a row for `data_dictionary.csv` (15 fields, MD5); ¶1 says the archive holds three data files and a data dictionary, and the deposit paragraph says the dictionary gives each field's type, format, blank convention, source and noise mechanisms, with the manifest and `config.yaml` as deposit files beside the zip rather than inside it.
- ¶3, structure and deposit: the overlaps as facts (`{python} overlap_500k_simulants` and `{python} overlap_100k_simulants` people, `{python} pct(match_prevalence_500k, 0)` of each file; the finder files share no people); **"true pair" defined here (reviewer pass, 2026-09-27)** as a registry row and a finder row carrying the same identifier, the unit every linkage result is scored on, with `{python} overlap_500k_pairs` and `{python} overlap_100k_pairs` of them and every other pairing a true non-match; the vintage sentence moved here from §3.2 (every finder record and its registry record are 2040; people last seen in 2020 or 2030 are in the registry alone, pointer to §4.2); the diagnosis-date sentence in ¶2 now says the date was *placed* on a day within the record's census year, with a pointer to §4.2's heaping bullet; the run-twice sentence points to §5 for the source population on request; the deposit's manifest of MD5 and SHA-256 digests, the configuration with every seed and target, the pipeline under a code DOI; one sentence that a second build reproduced the files byte for byte (`results/run_twice.json`).
- **Table 1** (`tbl-release`): file, rows, people, people shared with the registry, MB, MD5; SHA-256 in the deposited manifest. The blank-share columns moved to `tbl-errors` in §3.3 (author's call, 2026-09-24).
- **Moved out of Results (2026-09-24):** the duplication and target-count mechanisms → §2.3; the definition of overlap → §2.2 (the v0.2 trim story was already there); the checksum and run-twice argument → §2.4 QA check 0; the geography and time-span scope sentence → §2.1 (the author's note); FCDS's expectation of uniqueness → §4.2; the three-way load benchmark → §4.1.

### 3.2 Population characteristics — ¶4 + Figures 1 and 2 (drafted 2026-09-24)

- ¶1, age and sex: the registry has the age and sex distribution of cases reported to FCDS 1995–2023 [@pseudopeople_issue205], within `{python} age_sex_max_dev` percentage points in every stratum (Figure 1); the shares 65 and over, under 40, and female for the registry (`{python} over65_reg`, `{python} under40_reg`, `{python} female_reg`) against the larger finder file, which has the age structure of Florida's 2040 residents (`{python} over65_500k`, `{python} under40_500k`, `{python} female_500k`). The mean age of earlier drafts was replaced by these shares, which the composition file supports exactly.
- ¶2, race and ethnicity: registry against finder shares for White, Latino, Black, Asian and other/multiracial (`race_reg`, `race_500k`); the two finder files agree to within `{python} finder_files_max_diff_pp` percentage points on every share in the section (computed in the chunk, not asserted).
- ¶3, vintage: `{python} share_2020`, `{python} share_2030` and `{python} share_2040` of registry records by census year, one sentence with a pointer back to §3.1 (the diagnosis-date clause and the 2040 finder sentence moved to §3.1, 2026-09-27). ¶1 now presents the `{python} age_sex_max_dev` agreement as a check that the sampler hit its quota, not a finding, and says "the simulated population's Florida residents in 2040" for the finder files; the Figure 2 sentence adds that a pair's two records are one census record noised twice, so every difference is an injected error, with a pointer to §4.2's same-year bullet.
- ¶4, names: the three commonest first names per age group run from `{python} boys_0_4` to `{python} men_85` and from `{python} girls_0_4` to `{python} women_85`, read from `results/registry_top_names.csv` and printed in Figure 1's margins.
- **Figure 1** (`fig-registry-age-sex`): the pyramid, drawn in the paper by `figures.pyramid`; the caption says the FCDS dots sit on the bar ends by construction. **Figure 2** (`fig-example-pair`): three pairs chosen by profile (author's spec 2026-09-25: a verified nickname with further errors; an address with two or more fields altered; a month/day swap beside an SSN digit swap), drawn by `figures.record_card` and introduced by one sentence that names the three; the caption says every difference is noise because a pair's two records share a census year. Nicknames are verified against pseudopeople's own `nicknames.csv`, so `record_diff.classify` now distinguishes `nickname` from `different name` (fake-name noise).
- **Moved out of Results (2026-09-24):** the clinical-characterisation scope → §4.2 (identity-resolution bullet); race/ethnicity inherited through age, not modelled → §4.2 (already there); households → §2.1; the fidelity giveaways and the geocoding warning → §4.2.

### 3.3 Error structure — ¶3 + Table 2 (drafted 2026-09-24)

- ¶1 introduces **Table 2** (`tbl-errors`, Table 2 in the paper's order): for each released field, blank shares in the registry and the larger finder file with the set rate in parentheses (FCDS's specification for SSN and address fields, pseudopeople's 1% default elsewhere), and, among the `{python} overlap_500k_pairs` true pairs, the share agreeing exactly when both present and the share blank on either side; the smaller finder file matches the larger to within `{python} errors_100k_max_diff_pp` percentage points on every figure. The per-file blank shares come from `results/pair_agreement.json` (`blank_share_by_file`, added 2026-09-24).
- ¶2, SSN: blank in `{python} finder_ssn_missing` of finder records (as specified) and `{python} registry_ssn_missing` of registry records against `{python} cfg_registry_ssn_missing`; **corrected 2026-09-27:** the build blanked no registry SSN (`error_rates.json` `ssn_blanked` = 0), so every blank is structural, and the share exceeds both the target and the pool's `{python} pop_ssn_never` because SSN coverage in the source population varies with age (blank for 3.8% of registry people under 40 at diagnosis against 6.4% at 40–64 and 5.8% at 65–79; `forensics.json` `ssn_blank_by_age_band`), and the registry's ages are those with the least coverage; **by race/ethnicity (2026-09-27, `ssn_blank_by_race`):** finder file Asian 28.9%, Latino 23.5%, Black 19.3%, White 17.8%; registry Asian 21.5%, Latino 15.2%, Black 5.4%, White 1.9%, with a forward pointer to §3.4's SSN-rule differential; `{python} err_ssn_transposed` (1.0% of those present) finder SSNs carry an adjacent swap; `{python} err_ssn_transposed` finder SSNs carry an adjacent swap; SSNs agree in `{python} agree_ssn_500k` of pairs with both present.
- ¶3, names, dates and addresses: agreement when both present (`{python} agree_first_name_500k`, `{python} agree_last_name_500k`, `{python} agree_dob_500k`, blank on one side in about `{python} blank_first_name_500k`); the two summary shares that bound §3.4's exact-match rules (`{python} name_dob_all_agree_500k` agree on name and date of birth together, `{python} ssn_usable_500k` have a usable, agreeing SSN); address agreement `{python} agree_street_name_500k` and blanks `{python} blank_street_name_500k`; unit numbers blank for `{python} unit_blank_reg` of registry records and street numbers blank above their set rates, both from the source.
- **Moved out of Results (2026-09-24):** the target-count missingness mechanism → §2.3; the New York State Cancer Registry comparison → §4.2; the Li et al. comparator and "do not call it too good" → §4, per the author's move.
- ¶4, sentinels (placed 2026-09-27 from `forensics.json`): dates of birth blank in `{python} dob_blank_reg` of registry records and `{python} dob_unparseable_reg` of those present unparseable; `{python} doe_names_reg` Doe-pattern names in the registry; no repeated-digit SSN in any file (asserted in the load chunk); `{python} ssn_not_issuable_500k` non-issuable SSNs in the larger finder file (made by the digit swap) and `{python} ssn_not_issuable_reg` in the registry. ¶1 also defines "agree exactly" as character-for-character string identity and says the §3.4 rules lower-case and trim first; Table 2's caption says street and unit numbers include source blanks.
- **Still to compute, optional:** the most common first and last names table (top-10 overall; Figure 1 carries the top-3 by age and sex, so this may be cut) and per-field *disagreement* by `race_ethnicity` (blankness by race is done, above).

### 3.4 Linkage difficulty — ¶5 + Table 3 + Figure 3 (drafted 2026-09-24)

*For the author — what the ladder is (2026-08-09, unchanged): each rule is one or two field-sets; a registry-row × finder-row pair is a predicted match if it agrees exactly on every field of at least one set; each set is one DuckDB hash join, so the ladder runs in seconds; every predicted pair is definitively true or false against `simulant_id`. The code is `pipeline/linkage_baseline.py` (eleven rules since 2026-09-24, with the current layout's address set and its "either" added, and a race-stratified pass), the numbers are `results/linkage_baseline.json` and `results/linkage_baseline_stratified.json`, re-run 2026-09-24 on an 8-CPU allocation.*

- ¶1, quasi-identifier uniqueness (`results/forensics.json`, `pipeline/data_forensics.py`, DONE 2026-09-24): `{python} uniq_name_dob` (97.0%) of registry people are unique on first name + last name + date of birth, `{python} uniq_lastname_dob` (88.8%) on last name + date of birth, `{python} uniq_zip_dob_sex` (81.6%) on ZIP + date of birth + sex; `{python} shared_fullname` (47%) share a full name with someone else.
- ¶2 and **Table 3** (`tbl-ladder`): eight rows of the eleven-rule ladder on the 500k file (name+DOB; SSN alone; the two Procedure Guide sets and their union; the current layout's union; name+DOB or SSN; last name+DOB), with predicted, true and false pairs, then recall, missed-match, precision and false-match as percentages (reviewer pass, 2026-09-27; the caption defines Guide = Procedure Guide [@fdoh_fcds_procedure_guide_2007] and layout = Data Linkage Record Layout [@fcds_linkage_layout], and the prose cites both); the prose walks the ladder with `r500_*` variables and ends with the one-sentence relabelling: exact agreement on the field sets FCDS requires a submission to carry, not the registry's own matching procedure. New 2026-09-24: the layout's address set finds 56.1% with no false matches, and either layout set 71.7%.
- ¶3, blocking feasibility (forensics): `{python} n_pairs_naive` (2.5 trillion) pairs unblocked; full date of birth leaves `{python} pairs_block_dob` (58 million) candidates and keeps `{python} completeness_block_dob` (91.7%) of true pairs, which the text now identifies as the pairs whose dates of birth are present and agree on both sides (Table 2: 93.6% × 98.0%; asserted in the chunk, 2026-09-27); last-name initial + birth year leaves `{python} pairs_block_ln_yob` (1.23 billion) and keeps `{python} completeness_block_ln_yob` (90.7%).
- ¶4 and **Figure 3** (`fig-stratified`, `figures.stratified_baseline`): missed-match and false-match rates of name+DOB, SSN alone and their union by the finder record's race/ethnicity (five groups, true-pair counts shown). **Measured 2026-09-24, decision #15 answered by the data:** the name+DOB differential is null (missed 20.5–20.9% across groups; false-match 0.08–0.28%), the SSN differential is not (missed 34% Asian, 29% Latino, 21% Black, 19% White), and it carries into the union rule (7.2% Asian against 3.9% White). Results states the numbers; the reason (SSN coverage in the source population differs by group; noise is race-uniform) is §4.2's.
- ¶5, cost: `{python} n_rules` rules in `{python} baseline_seconds_500k` (3.8) seconds with 8 threads on an eight-core allocation (`linkage_baseline.json` now records the node); the 100k file's recall within `{python} ladder_100k_max_diff` (0.8) points of the 500k file's on every rule.
- **Not in the draft, deliberately:** the Li et al. comparator (moved to §4 by the author), "do not call it too good" (§4.2), the sentinel checks (§3.3's forensics: 11 Doe-pattern names, 0 repeated-digit SSNs, 0 non-issuable SSNs, 1.0% blank and 1.4% unparseable dates of birth — say them in §3.3 if wanted), and what is not here (no normalised or blocked variant, no probabilistic run), which §6 names as remaining work.


---

## 4. Discussion

*Target ≈ 750 words, four subsections. Genre spec: strengths and limitations, projects currently using the dataset, and suggestions for how other researchers could use it. The comparator survey lives in §1.3; the reproducibility mechanism lives in §2.2; the old standalone Limitations section merges into §4.2; access mechanics move to §5 Data Access. Only the 95.6%-vs-59.8% gap survives as a re-quoted figure. A Discussion of this length owns zero figures and zero tables.*

- **Pointers the Discussion must honour (2026-10-04).** Methods and Results now send the reader to §4 four times, and each needs a sentence or a paragraph where it lands: (1) §2.2: a true match is one census record noised twice, so no move, ageing or surname change separates its two records, the easiest case a linkage can face (the "easier than a real linkage" bullet in §4.2; the address-change extension in §4.3); (2) §2.3: what the noise leaves out, no wrong SSN digits and no relative's number, no surname change, noise symmetric between the files and independent across fields, one format for both (§4.2); (3) §2.3 and §3.1: diagnosis dates heap on 2020, 2030 and 2040 (§4.2's heaping bullet; the yearly observer in §4.3); (4) §3.3 and §3.4: SSN coverage differs by race/ethnicity in the source population, which §3.3 now reports as blank shares by group and §3.4 shows turning into a missed-match differential for the SSN rule and the best simple rule (§4.2's race/ethnicity caveats bullet). Not a pointer but owed: §3.2 no longer explains the registry's race mix, so §4.2's "race mix is pseudopeople's" bullet must say that it follows from the registry's ages.
- **Superseded mechanics (2026-10-04):** the oversample-and-stratified-trim story in §2.2 and §2.3 of this outline is history, not method. All pseudopeople row noise is off (non-response, omit-row, duplicate-with-guardian), every cohort is drawn at its exact target, and the second finder file's draw excludes the first's members; the paper's Methods §2.2 and the technical appendix say so. Discussion §4.1 may still use the v0.2 overshoot as the engineering lesson (ground-truth QA caught it), but should not describe the trim as current.

### 4.1 Strengths, and the engineering lessons in one paragraph — ¶2 (~160 words)

- Strengths in two sentences, without re-quoting numbers: state scale with the age/sex demography of cancer; exact ground truth; zero-barrier access; determinism verified by published checksums. Each is claimed once here and argued elsewhere — a summary, not a reprise.
- **The three-way load benchmark (moved from §3.1, 2026-09-24; still TO MEASURE):** wall time and peak memory to load the full USA via pseudopeople, Florida via the `state=` filter, and Florida from the staged extract, from `results/environment.json`; it justifies the extract (§2.1) and belongs with the engineering lessons, not among the dataset's results.
- The composition pattern, stated so a reader can reuse it: do the heavy relational work (filter, dedupe, SSA join, weighted sampling) in out-of-core SQL, stage the result as a Parquet directory mimicking the source layout, and point the simulator's `source` at it. The two tools compose through the filesystem. Treat the simulator as one stage of a pipeline you own, not as the pipeline — which is also why the bespoke SSN-transposition step was cheap to add.
- The reproducibility lesson in two sentences, no mechanism restated: **a seed pins the random stream, not the pairing of stream to rows.** Any pipeline whose row order is not contractually fixed can pass every unit test and still be irreproducible; simulation tools should document their row-order sensitivity. This generalises to any parallel engine because it removes the RNG from the engine entirely.
- The Dask comparison, honestly scoped. Keep it **qualitative**: DuckDB is single-node and SQL-only; Dask and Spark buy horizontal scale-out and arbitrary Python at the cost of orchestration and worker tuning [@person_linkage_case_study]. **Delete** the assertion that the prior project suffers "non-deterministic partition/row ordering that fights reproducibility" — it is an unsupported negative characterisation of a named colleague's repository, and even the authorship attribution is an inference the author must confirm. **Delete** the 8.7-second figure from this paragraph: that is the downstream linkage timing, not the build, and says nothing about whether a 21M-simulant construction fits one node. Either report the construction wall time, peak RAM and node spec, or make no scale claim. Note that Splink runs on a DuckDB backend, so the same engine serves construction and the experiments the dataset is for [@linacre2022splink].

### 4.2 Fidelity and limitations — ¶3 (~350 words; merges the old standalone Limitations section)

- The argument that licenses the simplification: for a *linkage* benchmark, difficulty is set by the joint distribution of the identifying fields — name frequency spectra, DOB collision rates within blocks, household co-residence, field-level error and missingness. Age enters only through those channels. The last-name+DOB rule's precision of `{python} r500_lastname_dob_precision` is the mechanism made visible, and it is inherited from the source population's demographically structured names and households, not from the cancer weighting.
- Where the argument breaks down, stated before a reviewer states it: if linkage error interacts with age- or ancestry-specific name structure, a mis-shaped mix changes measured *rankings*, not just error levels [@mcgrathlone2021ethnicbias]; the source draws first and last names independently and floors name frequency at public-list thresholds, so the rare-name tail is thinner than reality [@haddock2024simulated]; and missingness here is largely at random within targeted fields, whereas real registry missingness is differential.
- Anchor the tolerance: synthetic identifiers reproduced real linkage-quality estimates within fractions of a percentage point at small scale [@lam2024synthetic] — evidence that ranking and stressing methods tolerates fidelity gaps that inference would not [@ruggles2025shortcomings].
- **Identity resolution only.** No tumour site, histology, stage, diagnosis date or treatment; no natural history of cancer — the resource exercises finder-file-to-registry *identity* matching, not tumour consolidation or death clearance. And the gap that matters more to a registry audience: the registry is exactly one row per person (pseudopeople's row duplication is switched off since v0.4), so within-file duplicate detection — the central registry task, the one NAACCR certifies at under 0.1% for Gold [@naaccr2026certification] — is not exercised at all. The clinical characterisation the genre asks for is therefore the FCDS age/sex case-share matching alone, stated as a limit here (moved from §3.2, 2026-09-24).
- **Easier than a real linkage in four structural ways** (measured 2026-09-24, Table 4), stated beside the numbers: (1) true pairs are same-year records — no move, no aging, no surname change between diagnosis and cohort enrolment, so address agreement among true pairs is `{python} agree_street_name_500k` where real registries see far less, and any address-based rule is flattered; (2) the SSN is pristine beyond the `{python} cfg_finder_ssn_transposed` transposition — no wrong digits, no family member's number, no placeholder patterns; (3) noise is symmetric between files and independent across fields, where real finder files have systematic habits; (4) formats match exactly and the finder files carry essentially no duplicates. The rates themselves are the registry's own specification (§2.3), so the paper does not defend them as realistic beyond that; the remedies are the extensions of §4.3, and the first of them is the one we would do next. **Two promises Results now makes to this section (2026-09-25):** Figure 2's caption says every difference between a pair's records is noise "rather than a change in the person's life", so this bullet must say what that leaves out (moves, name changes, cohort-specific habits, §4.3's extensions); and Figure 2's lead says the three pairs were "chosen to show three kinds of error", so say here that a typical true pair differs in fewer fields — Table 2's shares (79% agree on first name, last name and date of birth together; 94% of first names agree when both present) are the typical case, and the figure is the tail.
- **Imperfect fidelity may mis-rank algorithms.** If a load-bearing feature of the real problem is absent — differential missingness, name change at marriage, first/last name dependence, the thin rare-name tail, all documented gaps of the source population [@haddock2024simulated] — package comparisons here could rank tools differently than production data would. That is the one error this resource must warn its users against: treat results as necessary, not sufficient, and validate winners in situ [@alexandersson2024comparing].
- **The race/ethnicity mix is pseudopeople's, not FCDS's (reviewer pass, 2026-09-27, item 7):** Results makes no claim about it beyond the shares; compare the finder file's mix with Florida's official 2020 Census shares here, with a Census Bureau citekey (needs verification), and say that the registry's mix follows from its ages, since race/ethnicity was not a sampling stratum (§2.2).
- **Race/ethnicity caveats, stated next to the equity results they qualify (§3.4):** first names are not race-conditioned in the source population, noise injection is race-uniform, and no race-differential data quality is modelled — so the stratified differentials measure name-structure effects only, and real-world differential error is plausibly larger. **Measured 2026-09-24 (Figure 3):** the name+DOB rule shows no differential (missed 20.5–20.9%, false-match 0.08–0.28% across groups), the SSN rule does (missed 34% for Asian, 29% for Latino, 19% for White people), and it carries into the best simple rule (7.2% against 3.9% missed). The mechanism is SSN coverage in the source population, which is lower for Asian and Latino simulants, not the noise, which is race-uniform — an inherited, realistic differential, and the sentence to put beside Figure 3 here. **Pointer from §3.2 (2026-09-25):** the paper now says the registry's race/ethnicity mix differs from the finder files' "because of the registry's older ages" and points here; say it plainly — the only design input is age and sex, race/ethnicity varies with age in the source population, so an older registry is Whiter and less Latino than the 2040 residents, and nothing race-specific was modelled. Name the folded "other" group here too (AIAN, NHOPI, multiracial, unknown), since §3.2 names it in a parenthesis.
- **Disease is a bolt-on, not integrated into the simulation** (the author's own characterisation, 2026-08-09): cancer status alters neither mobility nor mortality — a cancer patient and a healthy simulant of the same age, sex and race/ethnicity behave identically — so survivorship structure is absent. The related scope choice (decision #16, resolved 2026-09-24): the registry now includes simulants who died or left after their last census, but death is not modelled as a registry event — no vital status, no death clearance; cross-reference the identity-resolution-only bullet's death-clearance gap.
- **Household dynamics are simplistic:** when only part of a household moves, it is always a single person who moves to a new household or joins an existing one as an "other nonrelative" — **verify against the simulation code before print** (needs-verification #8). And the schema carries **no phone numbers or email addresses**, fields real linkage workflows increasingly rely on.
- **Addresses must not be geocoded:** they are deliberately not real addresses (§3.2); a user who geocodes them gets failures or fictitious locations. Name the other fidelity giveaways here too (moved from §3.2): lowercased addresses and cities, `city = "unincorporated"`, and that a true pair's two records are the same year's record noised twice.
- **Known construction imperfections that remain:** the SSN-missingness floor (§3.3 — the config parameter is a target the pipeline can only move realised missingness *up* to, never down; and, measured 2026-09-27, the registry's floor sits above the pool's never-held share because SSN coverage in the source population is lowest at ages 40–79, where the registry's people are, so the excess is an age effect and not a defect of the sampler) and the visible artifacts (§3.2: lowercased addresses, "unincorporated", the 2019-born infant). One consumer-facing defect worth a clause because it will bite the first user: the CSVs quote the rare comma-containing field (a `street_number` of `"64,66"` appears in `finder_100k.csv`) seldom enough that DuckDB's CSV sniffer infers no quote character and then fails to read the file — anyone loading the release must name the quote character explicitly; shipping Parquet alongside CSV in a future version removes the whole class of problem. For comparison (moved from §3.3): the New York State Cancer Registry reported 3.4% of 1.4M records lacking SSN [@qiao2023lexisnexis], so the registry's floor sits on the realistic side of its target. FCDS expects its own data to be unique [@pseudopeople_issue205]; the files are, to within the duplicated rows (moved from §3.1).
- **Diagnosis dates heap on three years.** Each registry record's diagnosis date is a day within its census year, so diagnoses fall in 2020, 2030 or 2040 only (27/28/46%); the age at diagnosis is right to within a year, but the calendar pattern is not a registry's. A yearly observer would spread them (§4.3 extensions, decision #19: the 1040 observer could, the ACS cannot — its Florida pool is under a million people).
- **A registry of last-seen records.** The simulated registry matches FCDS's age/sex case shares by construction, but each record is a person's last simulated census (2020, 2030 or 2040), so a large share of the registry is people who had died or left Florida by 2040 while the finder files are 2040 residents (the share is in `results/age_sex_qa.json`); realistic for a registry, but the address vintage mix is the simulation's, not FCDS's, and three censuses span twenty years where FCDS's caseload spans four decades. The case mix is validated only at the age/sex level, with race/ethnicity inherited from the population rather than modelled (§3.2). **Pointer from §3.2 (2026-09-25):** the paper now says "people last seen in 2020 or 2030 appear in the registry alone"; say here that these 2.7M people are the true non-matches a real linkage must reject, that they carry older addresses and diagnosis years, and that this is the realistic part of the design (deceased and departed cases are most of a registry's caseload) even though no finder record can ever link to them.
- **Locale and vintage.** Names, addresses and households are USA-circa-2020, and name distributions transfer poorly: GeCo required structural forking for Brazilian composite and multiple family names [@trentin2018brazil]. Conclusions about name-comparator choice do not port to Brazil, Australia or non-Latin-script registries, and any ethnic-bias finding reflects US-2020 name structure only [@mcgrathlone2021ethnicbias].

- Moved from results to discussion, but maybe not to the best place in the discussion: Comparator, two clauses: name+DOB-style deterministic rules on real data link 88–93% with 97–99% correct [@li2006deterministic], so exact name+DOB here (`{python} r500_name_dob_recall`) is *harder* than real data on recall and the simulated difficulty sits in a realistic band; and the gap between the best deterministic rule and perfect recall (`{python} r500_best_missed`) is the headroom a probabilistic method has to show, about what such methods recover over deterministic rules in practice. Do not call the ladder "too good": the noise rates are FCDS's own specification (§2.3), and the ways the benchmark is easier than reality are structural, named in §4.2.
- Blocking feasibility in two sentences: the naive comparison space is ~5×10¹¹ pairs; blocking on full DOB yields `{python} pairs_block_dob` candidate pairs retaining `{python} completeness_block_dob` of true pairs (and one more key, per §2.5) — the first numbers any probabilistic user needs for compute planning.


### 4.3 Uses: demonstrated, current, and suggested — ¶1 (~140 words)

- Demonstrated in this paper: the deterministic ladder doubles as a worked example — a user can reproduce Table 3 from the deposit and the archived code before trusting their own harness.
- Current and adjacent use, stated precisely because no external project uses *this* deposit yet: the second author's FCDS monograph programme ran on privately supplied pseudopeople data and recommended a public corpus (§1.3); this is it. The natural next step, which the authors are placed to do themselves, is to re-run that package comparison on this corpus and report rank agreement with FCDS's internal results — name it in §6 as the external-validity test still outstanding, not as an invitation to a third party. **Strengthen for the roster's "has been and/or is currently being used" (2026-09-24):** two things can be said honestly and should be. First, the lineage has been used — the second author's 2023 feasibility study and 2024 package comparison ran on the privately supplied predecessor files, so the design has already carried a registry's software evaluation once; say what those studies found in one clause each, since they are the closest thing to a use case. Second, ask the second author whether FCDS is re-running its comparison on v0.3 now; if yes, state it with a date as current use, if not, state it as the planned first use, with the rank-agreement test as its outcome measure. Do not let "currently being used" rest on this paper's own baselines. **Confirmed 2026-09-24 from the public data-access thread [@pseudopeople_issue205]:** FCDS's FY26 project (July 2025 to June 2026) is *Comparing the accuracy and speed of Match\*Pro, fastLink, and splink at the Florida Cancer Data System* — FCDS runs Match\*Pro for the NAACCR Virtual Pooled Registry's Phase 1 linkages and fastLink for its regular linkage requests — and its design is these files: a large linkage of a 500,000-record finder file against the 5M registry for the main comparison and a 100,000-record file for two sensitivity analyses, at the 20% overlap the second author specified as realistic and hard. Results go to FDOH and to the three software teams, with a Journal of Registry Management submission and public release of the derived data planned for 2026–27. That is the current use: state it with these facts and cite the thread, which also records that the second author expected uniqueness, more SSN noise than pseudopeople's default, and reproducible 5M files.
- Suggested uses, in the author's terms first: cancer-registry analysts comparing alternative linkage solutions, and algorithm developers benchmarking methods and evaluating new directions without the overhead of access to confidential data on real patients. Then one clause each: regression-testing in continuous integration, which gate-free access makes possible at this scale for the first time; differential-linkage-error and blocking research [@mcgrathlone2021ethnicbias]; and evaluating synthetic-identifier generators against a common target [@lam2024synthetic].
- **Extensions, each a small change to the pipeline because the pool keeps every census year (2026-09-24):** (a) *address change* — draw the registry record of an overlap member from an earlier census than the finder file (the person's first Florida appearance, or a random one), or draw the *finder* record from an earlier census so the cohort predates the linkage year (the author's suggestion of 2026-09-24), so a true pair carries years between its two records. **Measured 2026-09-24 on the source census:** of Florida simulants present in two consecutive censuses, 10.0% (2020→2030) and 8.5% (2030→2040) have a different address, 25.6% across 2020→2040, and 12.7% of those aged 50–69 at the start; every move changes the ZIP and the simulation never changes a surname. Real Floridians move at several times that rate, so a multi-year design would put a different address on roughly a tenth to a quarter of true pairs, not the majority a real cohort would show — worth having, and worth saying that the simulation's mobility, not the design, is the binding limit (decision #20): a move, aging, and, once pseudopeople models it, a surname change — the one we would do next, because it turns address agreement from `{python} agree_street_name_500k` into something a registry would recognise; (b) wrong-digit and borrowed-number errors on the SSN in the finder files; (c) asymmetric, cohort-specific noise habits; (d) duplicates within the finder files. Each is a new version with its own checksums, never a silent change to v0.3; ask the second author first whether Table 4 looks like FCDS's real finder submissions, since he set the rates on purpose.
- **Monitoring, demoted (2026-09-24):** the abstract, Key Features and Editor's note no longer frame the release as an experiment on pseudopeople's access gate, so the monitoring plan (download counts against PyPI installs and against access requests for the gated populations) is at most one clause under §6's ongoing improvements, or cut. If any figure is quoted, needs-verification #9 applies; otherwise that item closes.

### 4.4 Why open release, and what it risks — ¶2 (~120 words)

- **Fix the provenance argument.** Do not call ACS PUMS "public aggregate statistics" and do not claim "no real person's record contributed". PUMS is individual-level public-use microdata of real households, sampled to initialise the simulation. The defensible argument runs through PUMS's own disclosure protections (already released, de-identified, swapped, top-coded) plus the fact that there is no confidential dataset fitted to and therefore no membership to leak — which is what distinguishes this from the generative-model threat model that membership-inference attacks target [@stadler2022groundhog]. Under the regulator's test the question becomes coincidental resemblance, not identifiability [@ico2023pets].
- Name the residual risk: coincidental generation [@suchow2023coincidental]. With tens of millions of simulated Floridians some name+DOB+city combinations will match real people by chance. Weigh against it that every name is a recombination of names each shared by many real Americans by construction of the public source lists [@haddock2024simulated].
- **Argue the benefit case against the right counterfactual, in step with §1.3.** The Background now says only that identifiers are unavailable to outside researchers and that pseudopeople's large populations are available on request; this subsection owes the concrete benefit of removing even that request, not a claim that the request deters anyone. The existing pseudopeople gate is a public, logged GitHub request under a relational-governance process [@keyes2026governance] — inverting the risk calculus against *real registry data* instead is a false dilemma. State who a gate excludes in practice: CI systems and containerised reproductions cannot open an issue; classroom and workshop use at scale; and a fixed, checksummed artifact makes *this paper's own results* reproducible in a way a re-request cannot. Say these once, here. **Own the asymmetry §3.1 now states (2026-09-25):** the released files are open but the input they were built from is gated, so verification (digests, linkage experiments) is open while rebuilding requires the access request. Say why that is acceptable — the files, not the population, are what linkage research and development needs, and the request is public and logged — and say where the request goes.
- Guardrails as a short list: provenance documentation, determinism plus published checksums, a DOI deposit with versioning and a tombstoned withdrawal path [@zenodo_policies], prominent "simulated data" labelling, and a stated objection route — put with the author's honesty (2026-08-09): if someone objects to a simulated likeness of their name, *we have less recourse* than a controller of real data would. **Present the objection route as an untested proposal, not a novel contribution.** Changing the sampling salt re-draws *which* simulants are selected; it does not regenerate the names attached to a given simulant, so a complainant's name can reappear — and it destroys comparability with every published result on v0.2. If a mechanism is promised, it must be targeted suppression plus a tombstoned version bump, and it must actually be implemented on the deposit. Say "we are not aware of a comparable project that states one", which is what the evidence supports.
- **Add one sentence of positionality.** This section assesses the ethics of the first author's own simulator, using his own governance framing, and the paper's origin is a recommendation written by the second author that names the first author personally. Acknowledging both pre-empts a reviewer raising it less charitably; the COI statement carries the rest (§7).
- **Add the exposure no draft mentioned:** the files ship syntactically valid SSNs alongside full name, DOB and address. A released SSN can collide with a real issued number, and the corpus is usable as synthetic-identity seed material. The labelling guardrail should name the risk it mitigates, and contamination of a real registry system by simulated records should be raised.

---

## 5. Data Access

*Target ≈ 150 words. A required section for this genre — the paper's thesis made operational — and it feeds the Data Availability Statement.*

- Where: the Zenodo deposit — dataset DOI and version (run-list item 10) — with the pipeline archived under a code DOI and the repository linked. **Contents of the deposit, listed for the reader (2026-09-25 review):** the three CSVs and the zip; the manifest with MD5 and SHA-256 digests; `config.yaml` with every seed and design target; a data dictionary (run-list item 16); a README with the read-me-first facts (header row, empty fields for blanks, name the quote character in DuckDB, dates and SSNs as formatted).
- How: direct download; no application, no approval, no registration, no data-use agreement. Licence per decision #9 (CC0 recommended). Published MD5/SHA-256 checksums verify the download; `config.yaml` in the archive records every seed and target. State the file facts a user needs before the first `read_csv` (2026-09-25): UTF-8, header row, blanks as empty fields, rare quoted fields; Parquet alongside CSV is planned (§6).
- Versioning and redress: versioned deposits with a tombstoned withdrawal path [@zenodo_policies]; the objection route presented as an untested proposal (§4.4); prominent "simulated data" labelling on the deposit landing page, naming the synthetic-identity-seed risk it mitigates (§4.4).
- Contact: the corresponding author. Key Features no longer carries the collaboration invitation (2026-09-24), so this is the one place it appears.
- **The source population, on request (pointer from §3.1's run-twice sentence, 2026-09-27):** the released files need no approval, but rebuilding them, or building a different cut, needs the pseudopeople simulated US population, which is available through the lightweight approval process described in [@keyes2026governance]; say so here in one sentence, with the artifact name from §2.1.
- **Governance, stated as such (added 2026-09-24).** The journal's roster asks for "how to access the data and governance", and §4.4 argues the governance without ever naming it; give it one paragraph here, plain and in this order. *Custodians:* the two authors, with the corresponding author as the contact, IHME hosting the code repository and Zenodo the files. *Licence:* decision #9, which must be resolved before submission — CC0 recommended, so that benchmark rows embedded in test suites carry no attribution debt. *Terms of use, as a courtesy note rather than a contract:* the data are simulated and must not be treated as real; addresses are not geocodable (§3.2); SSNs are syntactically valid but fictitious and must not be used as identifiers outside the benchmark; there is no re-identification to attempt. *Versioning:* semantic versions, each with published MD5/SHA-256 checksums and a frozen `config.yaml`; a superseded version stays available with a tombstone pointing forward [@zenodo_policies], so results published against a version remain reproducible; changes are proposed as issues on the repository and released only as a new version, never by editing a deposited file. *Redress:* the objection route of §4.4, presented as an untested proposal unless decision #8 commits to implementing targeted suppression plus a tombstoned version bump. *Relation to pseudopeople's governance:* this deposit sits deliberately outside the lightweight request process that governs the large-scale pseudopeople populations [@keyes2026governance]; say so, and say what the request process still protects (the full populations and their other observers). *Sustainability:* Zenodo's retention commitment for the files; the code under a DOI; no funding-dependent service to keep alive. *Contributions:* community rule submissions (§6) are accepted through the repository and credited in the next version's changelog.
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
- **Funding Statement:** grant or "no specific funding" (decision #13); distinguish this work from the source population's Gates INV-060835 and Census CB21RMD0160001 funding; note salary sources if the funder requires. The second author's project is funded by FDOH (Contract CODJU) and CDC's National Program of Cancer Registries (DP003872-04), per the data-access thread [@pseudopeople_issue205]; confirm the wording with him.
- **Data Availability Statement:** placed just before References; the journal's open-repository wording with repository name, DOI/URL and reference number; no access restrictions to state.
- **Abbreviations:** compile at draft time — at minimum FCDS, SSN, DOB, GBD, ZIP, CSV, DOI, ACS, PUMS, NAACCR, IJPDS.
- **References:** Vancouver style with bracketed numerals in the text and DOIs for every entry that has one — verify `ijpds.csl` renders `[1]`-style brackets; include URLs where available.

---

## Figures, tables and code listings

Eight essential items plus one optional — the Data Resource Profile's length carries the forensics table (Table 2), the stratified figure (Figure 3) and the true-pair agreement table (Table 4, added 2026-09-24; fold it into Table 1 as columns if the display budget binds). Numbering below is after the 2026-09-24 renumbering (record pairs became Figure 2). **Master-graphic candidates (2026-09-24, author comparing):** `pipeline/draw_candidate_figures.py` renders three to `figures/` from `results/` — (1) the age/sex pyramid of the registry stacked by race/ethnicity with FCDS case shares as dots and the top-3 first names per group in the margins, (2) two record pairs with discrepancies washed and named, (3) the two side by side with a deposit inset. **Decided 2026-09-24: candidates 1 and 2 as separate figures.** The pyramid is Figure 1 and the record pairs are Figure 2, replacing the example-pair table; the stratified equity figure becomes Figure 3, and the tables renumber to 1–4. Everything else proposed across the five drafts stays cut; the cut list is at the end of this section so the decisions are visible rather than silent.

| Label | Kind | Caption | What it shows | Produced by | Status |
|---|---|---|---|---|---|
| `tbl-release` (Table 1) | Table | The released files: contents, designed and realised overlap, targeted versus realised error rates, size and checksums. | Rows: `registry.csv`, `finder_500k.csv`, `finder_100k.csv`, bundle `.zip`. Columns as drafted 2026-09-24: file, rows, people, people shared with the registry, MB, MD5 (SHA-256 in the deposited manifest). The blank-share columns moved to `tbl-errors` at the author's request. | `paper.qmd` chunk over `results/release_manifest.json` + `results/error_rates.json` + `results/linkage_baseline.json` + `config.yaml` | **Essential** |
| `fig-registry-age-sex` (Figure 1) | Figure | Who is in the simulated registry: shares of records by age group and sex, stacked by race/ethnicity, against the FCDS case shares the registry was drawn to (dots), with the three commonest first names per group in the margins. | The pyramid of candidate 1 (`figures.pyramid`, chosen 2026-09-24): 18 FCDS age bins by sex for the registry, dots on the bar ends by construction, names in the margins; the finder files and the GBD comparator go to a one-row table or a sentence rather than a panel. **The FCDS provenance must be confirmed regardless (decision #7)**, since it is now the Methods input. Caption states the pass criterion is peak band and sex crossover, not level, and that weights are age/sex only (no race-specific prevalence). | `pipeline/qa_age_sex.py` → `results/registry_age_sex.csv` (exists 2026-09-24) + `reference/*.csv`; drawn by `figures.pyramid` in `src/` | **Essential** |
| `fig-example-pair` (Figure 2) | Figure | The same simulant as it appears in the registry and in a finder file, with the noise mechanism named for each discrepancy. | 2–3 paired rows over the published columns plus `simulant_id`; discrepant cells marked; caption also names the fidelity giveaways (lowercased addresses, `city = "unincorporated"`, a 2019 birth in a 2020 extract). Doubles as the evidence behind §4.2's artifact bullet. | `pipeline/example_pair.py` → `results/example_pair.csv` (exists 2026-09-24; pairs 1007_399543 and 1534_695157), drawn as a record-pair panel by `figures.record_card` in `src/` | **Essential** |
| `tbl-common-names` (Table 2) | Table | Most common first and last names in the simulated registry, with counts. | Top-10 first and last names, stratifier per decision #17; reader-friendly fidelity evidence and the visible mechanism behind the uniqueness statistics and any stratified differential. Replaces the m/u table, cut 2026-08-09 at the author's direction. | `pipeline/data_forensics.py` → `results/forensics.json` — **NEW 2026-08-09** | **Essential** |
| `tbl-linkage-baseline` (Table 3) | Table | Deterministic exact-match rules scored against the `simulant_id` ground truth, 500,000-record finder file. | Five rules only — name+DOB; SSN alone; either FCDS minimum field set; current FCDS field set; name+DOB-or-SSN — plus `lastname_dob` if space allows, × {predicted pairs, TP, FP, precision, recall, missed-match %, false-match %}. 100k finder noted in one sentence. | `pipeline/linkage_baseline.py` → `results/linkage_baseline.json` (exists; eleven rules, re-run 2026-09-24); `tbl-ladder` in the draft shows eight rows | **Essential** |
| `tbl-errors` (Table 2 in the paper's order; drafted 2026-09-24) | Table | Error structure by field: blank shares in the registry and the larger finder file with the set rate, and, among true pairs, agreement when both present and blank on either side. | One row per released field, 500k finder file (the 100k file matches to the third decimal, noted in prose); two summary rows — exact agreement on first name, last name and date of birth together; usable and agreeing SSN. The difficulty portrait's core and the evidence behind §4.2's structural-easiness bullet. | `pipeline/pair_agreement.py` → `results/pair_agreement.json` (exists 2026-09-24) | **Essential** |
| `fig-stratified-baseline` (Figure 3) | Figure | Recall and precision of headline deterministic rules by race/ethnicity. | Two or three rules × strata, with true-pair counts per stratum shown so small-cell noise is visible. The equity result; if the differential is null, the null is reported (decision #15). Caption carries the §4.2 caveat: race-uniform noise, name-structure effects only. | `pipeline/linkage_baseline.py` → `results/linkage_baseline_stratified.json` (exists 2026-09-24), drawn by `figures.stratified_baseline`; missed-match and false-match rates rather than recall and precision, so both axes start at zero | **Essential** |
| `lst-noise-demo` (Listing 1) | Code listing | Generating noised records with pseudopeople and an additional noise setting, on the bundled ~10k-simulant sample population. | 8–12 echoed lines: build the hierarchical `noise_config` **pulling the rate from `cfg['noise']['finder']['address_missing']`, not a hard-coded 0.05**; call `generate_decennial_census`; show `.head()` and a one-line realised-rate check. The paper tier's only live computation. | `paper.qmd` chunk (replaces the current `sample-demo` stub) | **Essential** |
| `lst-fcds-fixed-width` | Code listing | Converting finder-file rows to the current FCDS 360-character fixed-width Data Linkage Record Layout. | ~15 lines: uppercase names, DOB → `YYYYMMDD` with 9-fill, missing SSN → `999999999`, padding to position; then 2–3 emitted records. Targets the current layout; the 2007 Attachment 9 layout is cited for existence only. | `paper.qmd` chunk over a function in `src/` that **does not yet exist** | **Optional — cut first** |

**Cut, deliberately:** `tbl-access-comparison` (every cell is a cited fact, so it is not a Results table; the contrast becomes prose split between §1.2, §4.4 and §5); `tbl-benchmark-comparison` and `tbl-prior-benchmarks` (the same comparator survey proposed twice, now prose in §1.3); `tbl-schema-layout` (repo documentation); `tbl-noise-config` (four numbers, better as a sentence); `tbl-noise-rates` (absorbed into Table 1's columns); `lst-weighted-sample` (the SQL becomes a one-line display expression in §2.2 and the run-twice assertion lives in `tests/`); `fig-qa-incidence` (merged as a panel of Figure 1). The uniqueness, blocking, and sentinel-check statistics are deliberately **prose numbers**, not tables — a few sentences in §3.3–§3.4 backed by `results/forensics.json`. `tbl-mu` (per-field m/u probabilities) cut 2026-08-09 at the author's direction: Fellegi–Sunter framing is a distraction from the paper's point.

---

## Computed values referenced in the text

Canonical variable names, deduplicated across the five drafts. **Five `results/` files now exist (2026-08-12):** `linkage_baseline.json`, `release_manifest.json`, `error_rates.json`, `population_summary.json`, `environment.json` — all measured on the v0.3 release. Still to write: `forensics.json`, `linkage_baseline_stratified.json`, `registry_age_sex.csv`.

**Rebuilt 2026-10-01 as v0.4** (pseudopeople's duplicate-with-guardian row noise off, so every file is one row per person; `data_dictionary.csv` inside the zip; a fresh noise realisation, see §2.3): every value below is from this build unless marked otherwise, and the earlier figures in this table are the v0.3 values until re-measured. The run-twice identity test was repeated for the new configuration: the first duplication-off build (as 0.3, Slurm 50423230) and the second (as 0.4, Slurm 50430271) are compared in `results/run_twice.json`.

**Rebuilt 2026-09-24 (v0.3, last-seen pool, FCDS case shares by exact quota, 2040 finder files; nothing was released, so the number stays):** every `results/` value below is from this build unless marked otherwise; registry rows 5,000,002 (2 duplication rows), age/sex shares within 0.041 pp of FCDS's, 46% of registry records last seen in 2040 and 27% each in 2020 and 2030, structural SSN missingness 5.68% against the 5% target. The run-twice checksum identity test has not yet been repeated for this design. **Earlier: v0.3 built and verified 2026-08-12:** `pipeline/build_cohorts.py` ran twice on the cluster; every design target hit exactly, and the two runs produced byte-identical files (run-twice checksum identity). The values below are v0.3 measurements; v0.2 history is noted where it differs.

| `{python}` variable | Known value | `results/` file | Sentence |
|---|---|---|---|
| `fl_pool` | 50,518,675 — **measured 2026-09-24** (`fl_census_age_sex.csv`; the build writes it as `fl_pool_last_seen`) | `population_summary.json` | "…the `{python} fl_pool` simulants ever recorded as Florida residents in the 2020, 2030 or 2040 census, each at their last appearance." |
| `fl_finder_pool`, `finder_year` | 22,959,862; 2040 — **measured 2026-09-24** (`fl_residents_finder_year`) | `population_summary.json` | "…finder files drawn from the `{python} fl_finder_pool` residents of `{python} finder_year`." |
| `fl_simulants` | 21,123,234 — **measured** (2020 census residents; kept only for the official-count check) | `population_summary.json` (exists) | "The simulated 2020 census records `{python} fl_simulants` Florida residents, `{python} fl_share_census` of the official count…" |
| `registry_rows_by_year`, `age_sex_max_dev` | 2020: 1,329,059; 2030: 1,376,079; 2040: 2,294,864; largest deviation 0.041 pp (men 45–49) — **measured at the 2026-09-24 build** | `age_sex_qa.json` (exists) | "…`{python} age_sex_max_dev` percentage points from the FCDS shares; `{python} registry_share_pre2040` of registry records are people last seen in 2020 or 2030." |
| `fl_share_census` | 0.98073 | `population_summary.json` (exists; denominator 21,538,187 is a cited literal) | "The extract is `{python} fl_share_census` of Florida's official 2020 Census count of 21,538,187 residents." |
| `pop_ssn_never` | 0.04183 over the last-seen pool (**measured 2026-09-24**; 0.04992 in the 2020 census alone) | `population_summary.json` (exists) | "…because `{python} pop_ssn_never` of the registry pool never held an SSN in the source population." |
| `registry_rows` | 5,000,002 — **measured 2026-09-24** (2026-08-12 build: 5,000,012; v0.2: 5,000,019) | `release_manifest.json` (exists) | "The simulated registry holds `{python} registry_rows` rows…" |
| `registry_simulants` | 5,000,000 — exact by construction, **verified at build** | `linkage_baseline.json` (exists) | "…for `{python} registry_simulants` distinct simulants." |
| `registry_dupe_rows` | 0 by construction since v0.4 (2026-10-01, duplicate-with-guardian off; v0.3: 2; 2026-08-12 build: 12; v0.2: 19); asserted in the build and in the paper's load chunk | `release_manifest.json` (exists) | not quoted; Table 1's caption says each data file has exactly one row per person. |
| `registry_ssn_missing` | 0.05685 — **measured 2026-09-24** (2026-08-12 build: 0.05775; v0.2: 0.057723) | `linkage_baseline.json`, `error_rates.json` (exist) | "Registry SSN missingness reached `{python} registry_ssn_missing`, above its target." |
| `finder_500k_rows` | 500,000 | `linkage_baseline.json` (exists) | "…two finder files of `{python} finder_500k_rows` and `{python} finder_100k_rows` records." |
| `finder_100k_rows` | 100,000 — one row per person since v0.4 (v0.3: 100,001) | `release_manifest.json` (exists) | Table 1 |
| `finder_ssn_missing` | 0.200 | `linkage_baseline.json` (exists) | "SSN is blank in `{python} finder_ssn_missing` of finder records." |
| `overlap_500k_simulants` | 100,000 — **verified at every build, latest 2026-09-24** (v0.2 measured 129,356) | `release_manifest.json` (exists) | "Realised overlap is `{python} overlap_500k_simulants` simulants against a target of `{python} overlap_500k_target` — exact by construction." |
| `overlap_100k_simulants` | 20,000 — **verified at build** (v0.2 measured 25,797) | `release_manifest.json` (exists) | as above, 100k file |
| `overlap_finder_finder` | 0 — **verified at build** (v0.2 measured 2,508, undesigned) | `release_manifest.json` (exists) | "The two finder files share no simulants, so the 100k file is a clean held-out replicate." |
| `match_prevalence_500k`, `match_prevalence_100k` | 0.200000 both — **verified at build** (v0.2: 0.258712, 0.257970) | `release_manifest.json` (exists) | "Match prevalence is `{python} match_prevalence_500k` of finder rows, as designed." |
| `overlap_500k_pairs` | 100,000 — **measured** (no overlap member sits on a duplicated registry row in v0.3; v0.2: 129,357) | `linkage_baseline.json` (exists) | "Recall is computed over `{python} overlap_500k_pairs` true record pairs." |
| `agree_<field>_500k`, `blank_<field>_500k` (first_name, last_name, dob, street_name, ssn, …) | 0.940/0.021, 0.959/0.020, 0.936/0.020, 0.970/0.059, 0.991/0.214 — **measured 2026-09-24** | `pair_agreement.json` (exists) | Table 4; "…first names agree exactly in `{python} agree_first_name_500k` of true pairs with both present…" |
| `name_dob_all_agree_500k`, `ssn_usable_500k` | 0.793, 0.779 — **measured 2026-09-24** | `pair_agreement.json` (exists) | "…`{python} name_dob_all_agree_500k` of true pairs agree exactly on name and date of birth together, and `{python} ssn_usable_500k` have a usable, agreeing SSN." |
| `overlap_100k_pairs` | 20,000 — **measured** (v0.2: 25,797) | `linkage_baseline.json` (exists) | as above |
| `overlap_500k_target` / `overlap_100k_target` | 100,000 / 20,000 | `config.yaml` (exists) | "…against targets of `{python} overlap_500k_target` and `{python} overlap_100k_target`." |
| `cfg_registry_target`, `cfg_finder_500k_target`, `cfg_finder_100k_target` | 5,000,000 / 500,000 / 100,000 | `config.yaml` (exists) | "The registry cohort targets `{python} cfg_registry_target` records…" |
| `cfg_oversample` | 1.15 (was 1.5; pseudopeople drops ~1.5% of rows) | `config.yaml` (exists) | "Cohorts are drawn at `{python} cfg_oversample`× target…" |
| `cfg_seed_sample`, `cfg_seed_registry`, `cfg_seed_finder`, `cfg_seed_postprocess` | 42, 42, 1, 999 | `config.yaml` (exists) | "All stochastic steps take their seeds from `config.yaml`…" |
| `cfg_finder_ssn_missing` / `_ssn_transposed` / `_address_missing` | 0.20 / 0.01 / 0.05 | `config.yaml` (exists) | "Finder files receive `{python} cfg_finder_ssn_missing` missing SSN, `{python} cfg_finder_ssn_transposed` transposition…" |
| `cfg_registry_ssn_missing` / `_ssn_transposed` / `_address_missing` | 0.05 / 0.00 / 0.01 | `config.yaml` (exists) | "…against the registry's `{python} cfg_registry_ssn_missing` target." |
| `err_street_500k`, `err_street_100k`, `err_street_reg` | 0.049846, 0.049590, 0.010028 — **measured 2026-09-24** | `error_rates.json` (exists) | Table 1 columns |
| `err_ssn_transposed` | 4,001 swaps applied to the 500k finder's present SSNs (1.0%); 671 remain visible among true pairs with both SSNs present, because a swap of two equal digits changes nothing — **measured 2026-09-24** | `error_rates.json`, acceptance notebook | "…`{python} err_ssn_transposed` SSNs carry an adjacent-digit swap." |
| `size_registry_mb`, `size_finder500k_mb`, `size_finder100k_mb`, `size_zip_mb` | 564.8, 49.9, 10.0, 234.5 — **measured 2026-09-24** (the registry grew with `diagnosis_date`) | `release_manifest.json` (exists) | Table 1 |
| `md5_registry`, `md5_finder500k`, `md5_finder100k`, `md5_zip` | `0dd8e15b…`, `6025e406…`, `ffbc3a53…`, `f05136aa…` — **2026-09-24 build**; the run-twice identity test has not been repeated for this design | `release_manifest.json` (exists) | Table 1 |
| `fcds_rate_min`, `fcds_rate_max` | 12.09 (females 5–9), 2,753.68 (males 75–79) — **per 100,000; verified against the file 2026-09-24** | `reference/fcds_incidence_by_age_sex.csv` (exists; the registry weights since 2026-09-24) | "…from `{python} fcds_rate_min` (females 5–9) to `{python} fcds_rate_max` (males 75–79) per 100,000." |
| `fcds_rate_female_max` | 1,838.96 at ages 80–84 (**verified against the file**) | `reference/fcds_incidence_by_age_sex.csv` (exists) | Figure 1 caption; "the female rate peaks at `{python} fcds_rate_female_max` per 100,000." |
| `gbd_prev_min`, `gbd_prev_max` | 0.59, 32.36 (**percent units**) — comparator panel only since 2026-09-24, not the weights | `reference/gbd_neoplasm_prevalence_florida.csv` (exists) | Figure 1 comparator; "…GBD prevalence runs from `{python} gbd_prev_min`% (males under 1) to `{python} gbd_prev_max`% (males 95+)." |
| `gbd_prev_female_max` | 21.84 at ages 85–90 (**verified against the file**) — comparator only | `reference/gbd_neoplasm_prevalence_florida.csv` (exists) | Figure 1 caption, comparator panel. |
| `r500_name_dob_precision` / `_recall` / `_missed` | 0.99810 / 0.79311 / 0.20689 — **measured 2026-09-24** (2026-08-12 build: 0.99775 / 0.79448 / 0.20552) | `linkage_baseline.json` (exists) | Table 3 narration |
| `r500_ssn_only_precision` / `_missed` | 0.99974 / 0.22077 — **measured 2026-09-24** | `linkage_baseline.json` (exists) | Table 3 narration |
| `r500_fcds_min_ssn_recall` | 0.64665 (FP = 0) — **measured 2026-09-24** | `linkage_baseline.json` (exists) | Table 3 narration |
| `r500_fcds_min_monthyear_fp` / `_precision` | 4,435 / 0.94522 — **measured 2026-09-24** | `linkage_baseline.json` (exists) | Table 3 narration |
| `r500_fcds_either_recall` / `_precision` | 0.81540 / 0.94842 — **measured 2026-09-24** | `linkage_baseline.json` (exists) | Table 3 narration |
| `r500_fcds_current_recall` | 0.59318 (FP = 0) — **measured 2026-09-24** | `linkage_baseline.json` (exists) | Table 3 narration |
| `r500_best_recall` / `r500_best_precision` / `r500_best_missed` | 0.95410 / 0.99821 / 0.04590 — **measured 2026-09-24** (2026-08-12 build: 0.95550 / 0.99795) | `linkage_baseline.json` (exists) | Table 3 narration; §3.4 comparator |
| `r500_lastname_dob_precision` | 0.71006 — **measured 2026-09-24** (2026-08-12 build: 0.65208; v0.2: 0.70006) | `linkage_baseline.json` (exists) | Table 3 narration | 
| `r500_current_either_recall`, `r500_current_address_recall` | 0.71690, 0.56138 (FP = 0 for both) — **measured 2026-09-24** (new rules) | `linkage_baseline.json` (exists) | Table 3 and §3.4 ¶2 |
| `strat_*` (Figure 3) | name+DOB missed 20.5–20.9%; SSN missed 19% White, 21% Black, 29% Latino, 34% Asian; union 3.9–7.2% — **measured 2026-09-24** | `linkage_baseline_stratified.json` (exists) | §3.4 ¶4 |
| `baseline_seconds_500k`, `baseline_threads` | 3.8 s, 8 threads on an 8-CPU long.q allocation (`long-slurm-sarchive-p0112`) — **measured 2026-09-24**; node recorded in the JSON | `linkage_baseline.json` (exists) | §3.4 ¶5 |
| `duckdb_version` | 1.5.4 | `linkage_baseline.json` (exists) | "Extraction, sampling and scoring run in DuckDB `{python} duckdb_version`." |
| `psp_version` | 1.2.8 — **recorded at v0.3 generation time** | `environment.json` (exists) | "…generated with pseudopeople `{python} psp_version`." |
| `dataset_version` | 0.4 (2026-10-01; v0.3 was never released) | `config.yaml` / `release_manifest.json` (exists) | "This profile describes dataset version `{python} dataset_version`." |
| `build_wall_seconds`, `build_node_spec` | 584 s wall, 23.0 GB peak RSS, `long-slurm-sarchive-p0115` (8 CPUs allocated) — **measured 2026-09-24**; the three-way load benchmark is still to measure | `environment.json` (exists) | §4.1 scale claim |
| `uniq_name_dob`, `uniq_lastname_dob`, `uniq_zip_dob_sex`, `shared_fullname` | 97.0%, 88.8%, 81.6%; 47% — **measured 2026-09-24** | `forensics.json` (exists) | §3.4 ¶1 |
| common-name counts | *TO COMPUTE (v0.3)* | `forensics.json` — **TO WRITE** | Table 2 cells only. |
| `pct_dob_blank`, `pct_dob_unparseable`, `n_doe_names`, `n_ssn_repeated`, `n_ssn_noncompliant` | registry: 1.0%, 1.4%, 11, 0, 0 — **measured 2026-09-24** | `forensics.json` (exists; per file under `sentinels`) | §3.3 sentinel sentence, not yet in the draft |
| stratified ladder metrics | *TO COMPUTE (v0.3)* | `linkage_baseline_stratified.json` — **TO WRITE** | Figure 3 cells; prose quotes at most one contrast, via a named variable. |
| race/ethnicity composition | *TO COMPUTE (v0.3)* | `registry_age_sex.csv` (extended) — **TO WRITE** | Figure 1 race/ethnicity panel; §3.2's descriptive fractions. |
| `n_pairs_naive`, `pairs_block_dob`, `completeness_block_dob`, `pairs_block_ln_yob`, `completeness_block_ln_yob` | 2.5 trillion; 58 million, 91.7%; 1.23 billion, 90.7% — **measured 2026-09-24** | `forensics.json` (exists) | §3.4 ¶3 |
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
5. **The FCDS table in `reference/fcds_incidence_by_age_sex.csv` — RESOLVED 2026-09-24** (decision #7): General Incidence 1995–2023, all malignant sites, counts and crude age-specific rates, posted by the second author in the data-access thread. The header now says so.
6. **Faker / commercial generators.** The author's 2026-08-08 Introduction outline names faker explicitly, so it is now cited as software (`faker_software`, trim tier) — package metadata plus an access date is the right form for a tool cited only to say what it does not do, and the "no error model, no cross-file identity" claim is verifiable against faker's own documentation. Commercial generators remain unnamed: the equivalent claim about them is still an unverified negative.
7. **The §2.1 simulation brief.** The author's summary (ACS + 2020 Decennial Census initialisation; twenty years of mortality/fertility/mobility from those sources and GBD) is authoritative but must be reconciled with the published description in Haddock et al. before print.
8. **The household partial-move behaviour** ("always a single person who moves to a new household or joins an existing one as an 'other nonrelative'") — the author's own [[double check]]; verify against the simulation code before §4.2 states it.
9. **The installs-vs-requests ratio** (pseudopeople PyPI installs ≈ 100× the access requests for the gated state/national files — the author's recollection, marked "check this"). **Demoted 2026-09-24:** the uptake-barrier framing left the abstract, Key Features, §1.3, §4.3 and §6, so nothing in the paper now needs this figure; it closes unless the author restores a monitoring clause in §6.
10. **The Census Bureau cooperative agreement** (number CB21RMD0160001, and whether it is the right instrument for the §7 acknowledgment). 
11. **Enamorado, Fifield and Imai (2019), "Using a probabilistic model to assist merging of large-scale administrative records", *American Political Science Review* 113(2): 353–371, DOI 10.1017/S0003055418000783** — the "small overlap" case the second author invokes for the 20% design (§2.2). Verify the reference before use.

---

## Work still to be done before rendering

Ordered by dependency. Items 1–3 must complete before any other number in the paper can be trusted.

1. **Commit what already exists — DONE (`ddd88c5`).** `config.yaml`, `pipeline/`, `results/` and `reference/` are tracked.
2. **Folded into `pipeline/build_cohorts.py` (2026-08-12).** The Florida-extract summary is written by the build script as `results/population_summary.json`: `fl_simulants`; `fl_share_census`; `pop_ssn_never` (the *population-level* never-had-an-SSN rate, distinct from the registry-measured rate). The registry duplicate-row count lands in `release_manifest.json`.
3. **`pipeline/build_cohorts.py` — DONE 2026-08-12: ported, then run twice on the cluster and verified.** Both acceptance tests passed — every design target exact, and the two runs produced byte-identical files (run-twice checksum identity). Built via `sbatch --wrap` (note: `srun` from inside an interactive session's allocation tries to create a job *step* in it and fails — use sbatch). `config.yaml` now points at v0.3. Original scope, for the record: The script covers items 2–4 end to end: weighted sampling with the five salted hash streams (salt strings identical to v0.2 so the draws are comparable), staged Parquet `ORDER BY simulant_id`, `stratified_trim` from `src/` in place of the notebook's buggy downsampling cell, the ordered SSA join with targeted SSN noise (now importable and unit-tested in `src/simulated_data_for_fcds_scale_rl/ssn_noise.py`), `race_ethnicity` carried into the released schema, GBD weights read from `reference/` instead of hard-coded, deterministic zip via fixed-metadata `zipfile` (no external `zip` binary), and the four `results/` JSONs. **Acceptance tests are asserted in-script: every design target hit exactly — overlaps 100,000 and 20,000, finder files disjoint — with hard failure otherwise; run twice and compare checksums for the identity test.** Run `srun --mem=120G -c 8 uv run python pipeline/build_cohorts.py` — never on a login node. On success, bump `dataset.version` to 0.3 and point `paths.release_dir` at the new release directory in `config.yaml` (both left at 0.2 for now so `pipeline/linkage_baseline.py` keeps running against the existing files).
4. **Folded into `pipeline/build_cohorts.py` (2026-08-12).** The build writes `results/release_manifest.json` (per-file rows, distinct simulants, overlap by both definitions — simulants and true pairs — byte sizes, MD5 **and** SHA-256, finder–finder overlap = 0, match prevalence 0.200 by design) and `results/error_rates.json` (realised missingness per targeted column per file, the structural-SSN floor, and the SSN-transposition count — measured at build time from the noise step itself, resolving the never-measured `err_ssn_transposed`), plus `results/environment.json` (versions, node, wall time, peak RSS; the three-way load benchmark still to be added there per item 9).
5. **Age/sex/race composition and top names — folded into `pipeline/build_cohorts.py` (2026-09-24).** The build writes `results/registry_age_sex.csv`, `results/registry_top_names.csv` and `results/age_sex_qa.json` for all three files from the source's true ages (the released files carry no age or year column, and with mixed record vintages a date-of-birth-derived age would be wrong), so the standalone `qa_age_sex.py` was removed. `pipeline/qa_source_age_sex.py` → `results/fl_census_age_sex.csv` (DONE 2026-09-24) gives the Florida pools by sex and FCDS age bin for the 2020, 2030 and 2040 censuses and the last-seen pool: the Florida-population panel of Figure 1 and the basis of the registry-size and pool decision.
6. **`pipeline/example_pair.py` → `results/example_pair.csv` — DONE, re-specified 2026-09-25:** profile-driven selection, richest pair per profile with at most five differing fields: 2284_912718 (Nettie/Jeanette, an OCR error in the city, a wrong state, a ZIP digit, a blank SSN), 2448_211514 (an OCR error in the street name, a ZIP digit, a wrong race/ethnicity category, a blank SSN; **re-chosen 2026-09-27** after the reviewer pass, because the previous address pair, 3793_114288, carried a fake last name "N" that distracted from the address noise — the `address` profile now excludes name and date-of-birth changes), 1299_239472 (month/day swap, blank ZIP, adjacent SSN digits swapped). Pin with `--ids` if the figure must not move. Original scope: search the overlap for exemplars showing a nickname or typo, a transposed SSN, a blanked address field, and a swapped month/day; pin the chosen `simulant_id`s so Figure 2 is stable across reruns. Verify such exemplars actually exist before promising all four.
7. **`pipeline/data_forensics.py` → `results/forensics.json` — DONE 2026-09-24.** Quasi-identifier uniqueness (97.0% / 88.8% / 81.6%; 47% share a full name), blocking on full DOB (58M candidates, 91.7% completeness) and on last-name initial + birth year (1.23B, 90.7%), sentinel checks (11 Doe-pattern names; 0 repeated-digit and 0 non-issuable SSNs; 1.0% blank and 1.4% unparseable dates of birth), and the top-10 first and last names. `src/ssn_rules.py` holds the SSA issuance rules, tested.
8. **Extend `pipeline/linkage_baseline.py` — DONE 2026-09-24.** The current layout's address set (name + sex + DOB + ZIP + street number + street name) and its "either" join the ladder (eleven rules); a race-stratified pass writes `results/linkage_baseline_stratified.json` (five groups by the finder record's race/ethnicity, true-pair counts per group) for Figure 3; the node (hostname, CPUs, threads) is recorded. Re-run 2026-09-24 on an 8-CPU allocation, 3.8 s for the 500k file.
9. **`results/environment.json`.** Pseudopeople version used at generation time (the venv has 1.2.8, but dataset v0.2 predates it), Python version, DuckDB version, node spec, and the construction run's wall time and peak RAM — the numbers §4.1 needs to make any scale claim at all. Include the three-way load benchmark (full USA via pseudopeople; Florida via `state=`; Florida from the staged extract), wall time and peak RAM each — §2.1's friction narrative and §3.1's benchmark bullet both depend on it.
10. **Deposit and mint DOIs.** Build the deterministic zip, deposit on Zenodo, mint a dataset DOI and a code-archive DOI, and obtain the private reviewer access URL IJPDS requires at submission. The Data Availability Statement, the Data Access section, the abstract and Key Features cannot be finalised without these.
11. **Fix `paper.qmd` front matter and structure — partly DONE 2026-09-24.** Done: two authors with the full IHME address, ORCID and corresponding email; a docx-only chunk that rebuilds the affiliation block from the front matter (Quarto's docx template prints names only); the `Data Resource Profile:` title prefix; Key Features as an unnumbered six-bullet section backed by a load chunk over `results/` and `config.yaml`; the body headings in DRP order. Still to do: the abstract — it carries `{python}` placeholders, which Quarto does not evaluate inside YAML metadata, so either generate it in the body from a chunk with `output: asis` (as the author block is) or accept typed numbers there, against the convention; the second author's street address and ORCID; the back-matter statements per §7 (Acknowledgments, Ethics, COI, Publication Consent, Funding, Data Availability, Abbreviations, plus an AI Disclosure since this manuscript is AI-assisted); and verify `ijpds.csl` renders bracketed Vancouver numerals.
12. **Render once and commit `_freeze/` with `results/`.** Per `CLAUDE.md`, freeze hashes `paper.qmd` only and does not watch `src/`, `config.yaml` or data, so a render is required after every `src/` change and the two directories must be committed together.
13. **`pipeline/pair_agreement.py` → `results/pair_agreement.json` — DONE 2026-09-24.** Per-field agreement between the two records of each true pair for both finder files (Table 4), plus the two ladder summaries.
14. **`notebooks/v03_acceptance_checks.ipynb` — DONE 2026-09-24.** The receiver's-eye checks, executed against the v0.3 files: 37 pass, 0 fail, 12 notes — checksums against the manifest, layout and sizes, overlaps and the key, the second author's noise rates (including the ~1% visible SSN swaps and the 5.7% registry SSN floor), age/sex against his FCDS table from true ages, FCDS's minimum field sets (96.9% of finder records satisfy a Procedure Guide set, 92.5% a current-layout set, which follows from the 20% blank SSNs he specified), formats, names and race/ethnicity, the worked pair, deterministic sanity against Li et al., and provenance. Re-run after every rebuild; it is also the template for the deposit's QA section.
15. **`pipeline/qa_observer_pool.py` → `results/observer_pool_acs.json`, `results/observer_pool_1040.json` — DONE 2026-09-24.** Sizes the ACS and 1040 observers as registry pools (decision #19).
16. **Data dictionary for the deposit (2026-09-25 review).** One row per released field: name, type, format (`MM/DD/YYYY`, `ddd-dd-dddd`), blank convention (empty field), which noise mechanisms touch it and at what set rate, and whether it is registry-only (`diagnosis_date`). Generate it from `config.yaml`, pseudopeople's default noise config and the manifest so it cannot drift; ship it with the README in the zip and cite it from §3.1 and §5. **Prototype DONE 2026-10-01:** `reference/data_dictionary.csv` (15 fields; columns field, files, type, format, example, blanks, source, noise, notes), reviewed by the author, who asked for the blank rates spelled out per file; the build copies it verbatim into the release directory and the zip and lists it in the manifest with its digest, and §3.1 cites it. Hand-written rather than generated, so re-check it against `config.yaml` and pseudopeople's defaults whenever either changes. The README for the zip is still to write.
17. **Subsection cross-references from Results (reviewer pass 2026-09-26, item 23).** Results points to `@sec-methods`, `@sec-discussion` and `@sec-access` at section level; once Methods and Discussion have labelled subsections, retarget each pointer to its subsection (age/sex quota → §2.2, noise and blanking → §2.3, same-year pairs and heaping → §4.2, source population on request → §5).

---

## Open decisions for the author

1. **Manuscript type — RESOLVED (2026-08-08): Data Resource Profile**, per the author; the journal's DRP guidelines are recorded in this outline and the structure above follows them. One residual check: the DRP word limit in the journal's Fee Structure table.
2. **Title:** adopt the recommended title above, or one of the three runners-up? **Which one?**
3. **Overlap definition:** report the overlap as distinct simulants in both files (recommended, with pairs footnoted), or as record pairs? **Simulants or pairs?**
4. **FCDS rule vintage:** foreground the 2007/2016 Procedure Guide rule, the current Data Linkage Record Layout rule, or both with the ambiguity stated (recommended)? **Which?**
5. **"Jo Lam's proposed quality metrics":** did you mean the missed-match / false-match framing of Lam et al. 2024, or the unpublished ITALO reporting work? If ITALO, there is no citable artifact yet. **Lam et al. 2024, or ITALO?**
6. **Noise-rate provenance — RESOLVED in substance 2026-09-24:** the rates are the second author's specification, quoted in the working notebook of 2026-02-02 ("I propose the same customization as in the FCDS 2024 monograph: Finder file: 20% missing SSN, 1% transposition error SSN, 5% missing Address; FCDS file: 5% missing SSN, 0% transposition, 1% missing Address"), so the paper attributes them to him and to FCDS's monograph work. Still needed: the monograph's exact reference (needs-verification #4), and his confirmation that the paper may quote the specification as his and that Table 4 looks like FCDS's real finder submissions. **Confirmed?**
7. **FCDS age/sex table — RESOLVED in substance 2026-09-24.** Its provenance is in the public data-access thread [@pseudopeople_issue205]: on 2026-01-28 and 2026-01-30 the second author posted the table as *Florida Cancer Registry, General Incidence, diagnosis years 1995–2023, all malignant sites, sex detail, 5-year age groups (18 groups, 85+ open), counts and crude age-specific rates per 100,000 per year, extracted and authorized for this project*, with the 1,605 unknown-sex cases excluded. The simulated registry is drawn to the count shares (`config.yaml`, `paths.age_sex_target`); the rate column is no longer used and can stay for the record. Residual: cite it as the thread or as an FCDS extract, and update the CSV header (done 2026-09-24). **Which citation form?** **Reviewer's angle (2026-09-25):** the data-access thread is the paper's first citation; cite the table itself in a form reviewers recognise — an FCDS data extract or a personal communication from the second author, dated 2026-01-28 — and the thread for provenance.
8. **Objection/redress mechanism:** do you commit to implementing a working one (targeted suppression plus a tombstoned version bump) on the deposit, or present it explicitly as an untested proposal? A salt change does not work — it re-draws which simulants are selected, not the names attached to them. **Commit, or present as proposal?**
9. **Licence:** CC0 (recommended — attribution stacking is impractical for benchmark data embedded in test suites) or CC-BY? **CC0 or CC-BY?**
10. **Conflict of interests:** disclose that you built pseudopeople, co-authored the source population, help govern access to it, and are named personally in the monograph recommendation that motivates this paper, and that the second author wrote that recommendation — or declare "None"? Recommended: disclose both. **Disclose or not?**
11. **`person_linkage_case_study` attribution:** have you confirmed with Zeb Burke-Conte that he is the author and is content to be cited? **Yes or no?**
12. **Attachment 9 conversion demo:** keep `lst-fcds-fixed-width` (requires writing the converter in `src/`) or cut it as the first casualty of the word limit? **Keep or cut?**
13. **Funding:** what grant supports *this* work, as distinct from the underlying population's Gates INV-060835 and Census CB21RMD0160001 — or is it "no specific funding"? **Which?**
14. **Acknowledgment by name — RESOLVED (2026-09-24): Anders Alexandersson is a co-author**, so no acknowledgment is needed. Residual: his affiliation wording, full street address and ORCID for the author block (Title, authors), and whether the second-author disclosure in §7 is worded to his satisfaction.
15. **Stratified equity results (Figure 3) — RESOLVED by the data 2026-09-24: report both the null and the non-null.** Name+DOB shows no differential across race/ethnicity groups (missed 20.5–20.9%); the SSN rule does (missed 34% Asian, 29% Latino, 19% White) because SSN coverage in the source population differs by group, and the best simple rule inherits it (7.2% against 3.9%). Results §3.4 states it; §4.2 explains it.
16. **Registry scope — RESOLVED 2026-09-24: expand.** The simulated registry is drawn from the last-seen pool (every simulant ever recorded in Florida in the 2020, 2030 or 2040 census, once, at their last appearance) and the finder files from 2040 residents, so the registry includes people who have since died or moved away, as FCDS's caseload does; this is what makes FCDS's age/sex shares attainable at 5M (§2.2; `results/fl_census_age_sex.csv`: 37% of the tightest stratum against 101% from the 2020 census alone). Residual: state the vintage mix in §3.2 and the drawback in §4.2.
17. **Common-names table (Table 2) stratifier:** by race/ethnicity (recommended — it makes Figure 3's mechanism visible) or by birth cohort? **Race/ethnicity, or birth cohort?**
18. **A record-year column in the registry? — RESOLVED 2026-09-24: added, as `diagnosis_date`.** Each registry record carries a diagnosis date, a day within its census year (§2.3), so age at diagnosis is computable from the released fields (the acceptance notebook, §5c, checks it against Anders's table). The shortcut it hands a linker — every finder member's registry record is dated 2040, so filtering the registry to that year discards 54% of candidates — is named in §4.2 beside the heaping of dates on three years. A yearly observer (the 1040 observer, sized 2026-09-24) would remove both.
19. **Pivot the registry pool from the census to a yearly observer? — RESOLVED 2026-09-24: no, keep the census pool.** The measurements stand (`results/observer_pool_*.json`): the ACS cannot supply the registry (0.94M Florida people ever surveyed, a 0.25M ceiling, no repeat observations); the 1040 observer could (69M filers, 15.7M ceiling, 4.8M repeat filers with an address change) and remains the address-change extension of §4.3, not the design. The heaping of diagnosis dates on three census years is named in §4.2.
20. **Finder files assembled across census years, for address changes?** The author's idea (2026-09-24): draw each finder member's record from an earlier census than 2040 so a true pair spans years. The census pool supports it (both files can be drawn from records of any year the person was a Florida resident, the registry keeping its last-seen record); the ACS cannot supply a 500k finder file (0.94M Florida people ever surveyed). The measured ceiling is the simulation's own mobility, above: about 10% of people change address per simulated decade and no one changes surname, against real-world moving rates several times higher, so the gain is a different address on a tenth to a quarter of true pairs. Alternatives: inject address change as noise (replace the address of a chosen share of finder records with another simulated Florida address — a knob, like the SSN swaps, rather than a dynamic), or both. Either is a new version, with the finder files described as cohorts enrolled 2020–2040 and linked in 2040. **Multi-year draw, injected moves, both, or neither?**
21. **Version number for the duplication-off build — RESOLVED 2026-10-01: v0.4** (the author's call). v0.3 was never released either, but the new build is a different noise realisation of the same design, with row duplication off and a data dictionary in the archive, so it gets its own number; `config.yaml`, the build's `--version` default, the acceptance notebook's name (`v04_acceptance_checks.ipynb`) and the README moved with it. The v0.3 directory and zip stay on disk until the author removes them.