"""Size a pseudopeople observer as a registry pool for Florida.

Pipeline tier (a full scan of one observer: the ACS is 1 GB and takes a minute on
two threads; the 1040 observer is 324 GB and wants a cluster job). For the given
observer: Florida person-years by year, distinct people, the last-seen pool by sex
and FCDS age bin, how large a registry with FCDS's exact age/sex shares it could
supply, how many 2040 census residents appear in it (overlap supply), and how many
people with two or more observations changed address between their first and last.
Written 2026-09-24 to answer whether a yearly observer could replace the census pool
(decision #19); results in ``results/observer_pool_<name>.json``.

    uv run python pipeline/qa_observer_pool.py american_community_survey survey_date results/observer_pool_acs.json 2 40GB
    sbatch -c 8 --mem=120G --wrap "uv run python pipeline/qa_observer_pool.py taxes_1040 tax_year results/observer_pool_1040.json 8 100GB"
"""
import sys, json, time, duckdb, pandas as pd, yaml
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
from simulated_data_for_fcds_scale_rl.age_sex_weights import load_age_sex_weights
obs, datecol, out = sys.argv[1], sys.argv[2], sys.argv[3]
threads = int(sys.argv[4]) if len(sys.argv) > 4 else 2
mem = sys.argv[5] if len(sys.argv) > 5 else "40GB"
cfg = yaml.safe_load(open(ROOT / "config.yaml"))
src = cfg["paths"]["psp_source"]
yearexpr = f"year({datecol})" if datecol == "survey_date" else datecol
w = load_age_sex_weights(ROOT / cfg["paths"]["age_sex_target"])
bins = w[w.sex == "Female"][["age_start", "age_end"]].reset_index(drop=True)
fc = pd.read_csv(ROOT / cfg["paths"]["age_sex_target"], comment="#"); fc["sex"] = fc.sex.str.capitalize()
share = fc.set_index(["age_start", "sex"])["count"] / fc["count"].sum()
con = duckdb.connect(); con.execute(f"SET memory_limit='{mem}'; SET threads={threads}; SET preserve_insertion_order=false;")
con.register("bins", bins)
t0 = time.time()
con.execute(f"""
    CREATE TABLE fl AS
    SELECT simulant_id, {yearexpr} AS year, any_value(sex) AS sex, min(age) AS age, any_value(address_id) AS address_id
    FROM read_parquet('{src}{obs}/*.parquet')
    WHERE state = 'FL' GROUP BY simulant_id, {yearexpr}
""")
res = {"observer": obs, "scan_seconds": round(time.time() - t0)}
res["person_years"] = con.execute("SELECT count(*) FROM fl").fetchone()[0]
res["rows_by_year"] = dict(con.execute("SELECT year, count(*) FROM fl GROUP BY year ORDER BY year").fetchall())
res["distinct_people"] = con.execute("SELECT count(DISTINCT simulant_id) FROM fl").fetchone()[0]
last = con.execute("""
    SELECT f.sex, b.age_start, count(*) AS n
    FROM (SELECT * FROM fl QUALIFY row_number() OVER (PARTITION BY simulant_id ORDER BY year DESC) = 1) f
    JOIN bins b ON f.age >= b.age_start AND f.age < b.age_end
    WHERE f.sex IN ('Male', 'Female') GROUP BY ALL
""").df().set_index(["age_start", "sex"])["n"].reindex(share.index).fillna(0)
res["men_65_plus_last_seen"] = int(last.xs("Male", level="sex").loc[65:].sum())
res["max_registry_exact_fcds_shares"] = float((last / share).min())
res["max_registry_at_50pct_of_tightest"] = float((last / share).min() * 0.5)
res["tightest_stratum"] = " ".join(str(x) for x in (last / share).idxmin())
res["last_seen_by_stratum"] = {f"{s} {a}": int(n) for (a, s), n in last.items()}
# overlap supply: 2040 census Florida residents that appear in this observer at any year
con.execute(f"""
    CREATE TABLE c2040 AS SELECT DISTINCT simulant_id FROM read_parquet('{src}decennial_census/*.parquet')
    WHERE state = 'FL' AND year = 2040
""")
res["census_2040_residents"] = con.execute("SELECT count(*) FROM c2040").fetchone()[0]
res["census_2040_residents_in_observer"] = con.execute("SELECT count(*) FROM c2040 WHERE simulant_id IN (SELECT simulant_id FROM fl)").fetchone()[0]
# address change: people with 2+ observations whose address differs between first and last
mv = con.execute("""
    WITH o AS (SELECT simulant_id, first(address_id ORDER BY year) AS a0, last(address_id ORDER BY year) AS a1, count(*) AS k, max(year) - min(year) AS span
               FROM fl GROUP BY simulant_id)
    SELECT count(*) FILTER (WHERE k >= 2) AS multi, count(*) FILTER (WHERE k >= 2 AND a0 <> a1) AS moved, avg(span) FILTER (WHERE k >= 2) AS mean_span
    FROM o
""").fetchone()
res["people_with_2plus_obs"], res["of_which_address_changed"], res["mean_span_years_2plus"] = int(mv[0]), int(mv[1]), float(mv[2] or 0)
json.dump(res, open(out, "w"), indent=2)
print(json.dumps({k: v for k, v in res.items() if k != "last_seen_by_stratum"}, indent=1))
