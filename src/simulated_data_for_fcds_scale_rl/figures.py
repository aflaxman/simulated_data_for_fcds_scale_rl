"""Drawing functions for the paper's figures (paper tier: reads ``results/`` and ``reference/`` only).

Three master-graphic candidates were drawn on 2026-09-24; the author chose 1 and 2 as
separate figures (the paper's Figure 1 and Figure 2) and 3 is kept for reference:

1. ``candidate_pyramid``      — age/sex pyramid of the registry stand-in, stacked by
                                race/ethnicity, FCDS reported-case shares as dots, top-3
                                first names per age group in the margins.
2. ``candidate_record_pairs`` — the same simulant in the registry and a finder file,
                                discrepancies washed and named.
3. ``candidate_composite``    — the two side by side with a small "what is in the
                                deposit" inset.

Colours follow the dataviz reference palette (light mode), validated 2026-09-24
against a white surface: five categorical slots for race/ethnicity in a fixed
order, text in ink tokens, a hairline grid. Only relative shares are drawn.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
CFG = yaml.safe_load((ROOT / "config.yaml").read_text())
RESULTS = ROOT / CFG["paths"]["results"]

# --- palette (dataviz reference instance, light) ---------------------------------
SURFACE = "#ffffff"
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, BASE = "#e1e0d9", "#c3c2b7"
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"]  # fixed order, never cycled
RACE_ORDER = ["White", "Latino", "Black", "Asian", "Other"]
RACE_FOLD = {"Multiracial or Other": "Other", "AIAN": "Other", "NHOPI": "Other", "Unknown": "Other"}
WASH = "#cde2fb"  # sequential blue step 100: the "these cells differ" highlight

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 7,
    "axes.edgecolor": BASE,
    "axes.linewidth": 0.6,
    "xtick.color": INK2,
    "ytick.color": INK2,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
})

MM = 1 / 25.4


# --- data ---------------------------------------------------------------------------
def _fold_race(r: str) -> str:
    return RACE_FOLD.get(r, r if r in RACE_ORDER else "Other")


def load_age_sex(file: str = "registry.csv") -> pd.DataFrame:
    df = pd.read_csv(RESULTS / "registry_age_sex.csv")
    df = df[df["file"] == file].copy()
    df["race"] = df["race_ethnicity"].map(_fold_race)
    return df


def load_top_names(file: str = "registry.csv") -> pd.DataFrame:
    df = pd.read_csv(RESULTS / "registry_top_names.csv")
    return df[df["file"] == file].copy()


def load_fcds_shares() -> pd.DataFrame:
    """FCDS reported cases by age group and sex, as shares of all reported cases."""
    f = pd.read_csv(ROOT / CFG["paths"]["age_sex_target"], comment="#")
    f["sex"] = f["sex"].str.capitalize()
    f["share"] = f["count"] / f["count"].sum() * 100
    return f[["sex", "age_start", "share"]]


def load_manifest() -> dict:
    return json.load(open(RESULTS / "release_manifest.json"))


def load_example_pairs() -> pd.DataFrame:
    return pd.read_csv(RESULTS / "example_pair.csv", dtype=str, keep_default_na=False)


# --- pyramid ------------------------------------------------------------------------
def pyramid(ax, file: str = "registry.csv", show_names: bool = True, show_fcds: bool = True,
            name_size: float = 6.0, label_size: float = 6.4, gap: float = 1.2, legend: bool = True):
    """Age/sex pyramid of one released file. Returns the legend handles (for a figure-level legend)."""
    df = load_age_sex(file)
    bins = df[["age_group", "age_start"]].drop_duplicates().sort_values("age_start").reset_index(drop=True)
    groups = bins["age_group"].tolist()
    n = len(groups)
    total = df["count"].sum()
    shares = (df.pivot_table(index=["sex", "age_group"], columns="race", values="count", aggfunc="sum", fill_value=0)
              / total * 100)
    fcds = load_fcds_shares() if show_fcds else None
    names = load_top_names(file) if show_names else None

    xmax = 0.0
    for sex, sign in (("Male", -1), ("Female", 1)):
        for yi, g in enumerate(groups):
            left = gap
            row = shares.loc[(sex, g)] if (sex, g) in shares.index else None
            for race, color in zip(RACE_ORDER, SLOTS):
                w = float(row.get(race, 0.0)) if row is not None else 0.0
                if w <= 0:
                    continue
                ax.barh(yi, sign * w, left=sign * left, height=0.72, color=color,
                        edgecolor=SURFACE, linewidth=0.7, zorder=2)
                left += w
            xmax = max(xmax, left)
        if fcds is not None:
            f = fcds[fcds["sex"] == sex].set_index("age_start").reindex(bins["age_start"])
            xs = sign * (gap + f["share"].to_numpy())
            ax.plot(xs, range(n), color=INK2, lw=1.3, zorder=3, marker="o", ms=4.2,
                    mfc=INK2, mec=SURFACE, mew=0.9)
            xmax = max(xmax, gap + float(f["share"].max()))

    # axis: symmetric, ticks in absolute percent, a central gutter for the age labels
    half = xmax * (1.75 if show_names else 1.12)
    ax.set_xlim(-half, half)
    ax.set_ylim(-0.7, n + 0.45)
    step = 5 if xmax - gap > 8 else 2
    vals = list(range(step, int(math.ceil(xmax - gap)) + step, step))
    ticks = [-(gap + v) for v in vals[::-1]] + [(gap + v) for v in vals]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{v}%" for v in vals[::-1]] + [f"{v}%" for v in vals], fontsize=6.5)
    for t in ticks:
        ax.axvline(t, color=GRID, lw=0.6, zorder=0)
    ax.set_yticks([])
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.tick_params(axis="x", length=0, pad=2)
    for yi, g in enumerate(groups):
        ax.text(0, yi, g, ha="center", va="center", fontsize=label_size, color=INK2, zorder=4)
    for sex, sign in (("Male", -1), ("Female", 1)):
        ax.text(sign * (gap + (xmax - gap) / 2), n - 0.2, sex, ha="center", va="bottom", fontsize=7.5,
                color=INK, weight="bold")
    ax.set_xlabel(f"Share of records in {file.replace('.csv', '')}, by age group", fontsize=6.8, color=INK2, labelpad=3)

    if names is not None:
        for sex, x, ha in (("Male", 0.004, "left"), ("Female", 0.996, "right")):
            sub = names[names["sex"] == sex].sort_values(["age_start", "rank"])
            for yi, g in enumerate(groups):
                lst = sub[sub["age_group"] == g]["first_name"].tolist()
                if lst:
                    ax.text(x, yi, ", ".join(lst), transform=ax.get_yaxis_transform(),
                            ha=ha, va="center", fontsize=name_size, color=INK2, zorder=4)

    handles = [Patch(facecolor=c, edgecolor="none", label=r) for r, c in zip(RACE_ORDER, SLOTS)]
    if show_fcds:
        handles.append(Line2D([0], [0], color=INK2, lw=1.3, marker="o", ms=4.2, mfc=INK2, mec=SURFACE, mew=0.9,
                              label="Cases reported by FCDS, share by age and sex"))
    if legend:
        ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=6, frameon=False,
                  fontsize=6.4, handlelength=1.2, handletextpad=0.5, columnspacing=1.2)
    return handles


# --- record pair --------------------------------------------------------------------
DISPLAY_ROWS = [
    ("First name", ["first_name"]),
    ("Middle initial", ["middle_initial"]),
    ("Last name", ["last_name"]),
    ("Date of birth", ["date_of_birth"]),
    ("Sex", ["sex"]),
    ("Race/ethnicity", ["race_ethnicity"]),
    ("Street address", ["street_number", "street_name", "unit_number"]),
    ("City, state, ZIP", ["city", "state", "zipcode"]),
    ("SSN", ["ssn"]),
    ("Diagnosis date", ["diagnosis_date"]),  # registry only
]


def _fmt(rec: pd.Series, fields: list[str]) -> str:
    vals = [str(rec.get(f, "") or "") for f in fields]
    if fields[0] == "street_number":
        s = " ".join(v for v in vals[:2] if v)
        if vals[2]:
            s += f", unit {vals[2]}"
        return s or "(blank)"
    if fields[0] == "city":
        city, state, zipc = vals
        s = ", ".join(v for v in (city, state) if v)
        if zipc:
            s = f"{s} {zipc}".strip()
        return s or "(blank)"
    return vals[0] or "(blank)"


COMPACT_LABELS = ["First name", "Middle init.", "Last name", "Birth date", "Sex", "Race/eth.",
                  "Street", "City, ST ZIP", "SSN", "Dx date"]
SHORT_NOTES = {"nickname or different name": "nickname/other name", "adjacent digits swapped": "digits swapped",
               "month and day swapped": "month/day swapped"}


def record_card(ax, pair: pd.DataFrame, size: float = 6.4, show_header: bool = True, compact: bool = False) -> None:
    """One simulant's registry row beside its finder-file row; differing cells washed and named."""
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    reg = pair[pair["source"] == "registry"].iloc[0]
    fin = pair[pair["source"] == "finder_500k"].iloc[0]
    notes = {}
    if reg["discrepancies"]:
        for item in reg["discrepancies"].split("; "):
            f, lab = item.split(": ", 1)
            notes[f] = SHORT_NOTES.get(lab, lab) if compact else lab
    xs = ({"label": 0.0, "reg": 0.14, "fin": 0.44, "note": 0.745} if compact
          else {"label": 0.0, "reg": 0.175, "fin": 0.475, "note": 0.775})
    labels = COMPACT_LABELS if compact else [lab for lab, _ in DISPLAY_ROWS]
    value_size = size - 0.2 if compact else size
    n = len(DISPLAY_ROWS)
    top = 0.78 if show_header else 0.98
    row_h = top / n
    if show_header:
        x0, x1 = xs["reg"] + 0.11, xs["fin"] + 0.11
        ax.text((x0 + x1) / 2, 0.995, f"simulant_id {reg['simulant_id']}: the same simulated person",
                ha="center", va="top", fontsize=size - 0.3, color=INK2)
        ax.plot([x0, x0, x1, x1], [0.885, 0.91, 0.91, 0.885], color=BASE, lw=0.8, solid_capstyle="round")
        for key, title in (("reg", "Registry record"), ("fin", "Finder-file record")):
            ax.text(xs[key], 0.84, title, fontsize=size + 0.4, color=INK, weight="bold", va="center")
    for i, ((_, fields), label) in enumerate(zip(DISPLAY_ROWS, labels)):
        y = top - (i + 0.5) * row_h
        a, b = _fmt(reg, fields), _fmt(fin, fields)
        hit = [f for f in fields if f in notes]
        if fields == ["diagnosis_date"]:
            if not reg.get("diagnosis_date"):
                continue  # files built before the column existed
            b, hit = "(registry only)", []
        if hit:
            ax.add_patch(Rectangle((xs["reg"] - 0.012, y - row_h * 0.46), (xs["note"] - 0.02) - (xs["reg"] - 0.012),
                                   row_h * 0.92, facecolor=WASH, edgecolor="none", zorder=0))
            ax.text(xs["note"], y, "; ".join(dict.fromkeys(notes[f] for f in hit)), fontsize=size - 0.5,
                    color=INK2, style="italic", va="center")
        if i:
            ax.plot([0, 1], [y + row_h / 2] * 2, color=GRID, lw=0.5, zorder=0)
        ax.text(xs["label"], y, label, fontsize=size - 0.4, color=MUTED, va="center")
        for key, v in (("reg", a), ("fin", b)):
            ax.text(xs[key], y, v, fontsize=value_size, family="DejaVu Sans Mono", va="center",
                    color=MUTED if v == "(blank)" else INK)


def deposit_inset(ax, size: float = 6.0) -> None:
    """A few lines on what is in the deposit, from the release manifest."""
    m = load_manifest()
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ov = m["overlaps"]
    ax.text(0, 0.97, f"What is in the deposit (v{m['version']})", fontsize=size + 0.6, color=INK, weight="bold", va="top")
    y = 0.74
    for name in ("registry.csv", "finder_500k.csv", "finder_100k.csv"):
        ax.text(0.0, y, name, fontsize=size, family="DejaVu Sans Mono", color=INK, va="center")
        ax.text(0.62, y, f"{m['files'][name]['distinct_simulants']:>9,} people", fontsize=size,
                family="DejaVu Sans Mono", color=INK, va="center", ha="right")
        y -= 0.17
    text = (f"{ov['finder_500k']['overlap_simulants']:,} people of the 500k finder file and "
            f"{ov['finder_100k']['overlap_simulants']:,} of the 100k file\nare also in the registry; none are in both "
            "finder files. Every row carries\nits simulant_id, so any linkage can be scored exactly.")
    ax.text(0, y + 0.05, text, fontsize=size - 0.4, color=INK2, va="top", linespacing=1.35)


# --- candidates -----------------------------------------------------------------------
def candidate_pyramid():
    fig, ax = plt.subplots(figsize=(180 * MM, 112 * MM))
    fig.subplots_adjust(left=0.01, right=0.99, top=0.84, bottom=0.17)
    pyramid(ax)
    fig.text(0.01, 0.975, "Who is in the simulated registry", fontsize=9.5, color=INK, weight="bold", va="top")
    fig.text(0.01, 0.93, "Share of the registry stand-in's records by age group and sex, stacked by race/ethnicity.\n"
                         "Dots: the age and sex distribution of cases reported by the Florida Cancer Data System, "
                         "which the registry was drawn to match.\n"
                         "At the ends: the three most common first names in each group, as they appear in the file.",
             fontsize=6.6, color=INK2, va="top", linespacing=1.4)
    return fig


def candidate_record_pairs():
    pairs = load_example_pairs()
    ids = pairs["pair"].unique().tolist()
    fig, axes = plt.subplots(len(ids), 1, figsize=(180 * MM, (24 + 40 * len(ids)) * MM))
    fig.subplots_adjust(left=0.02, right=0.99, top=0.86, bottom=0.03, hspace=0.18)
    for ax, k in zip(axes if len(ids) > 1 else [axes], ids):
        record_card(ax, pairs[pairs["pair"] == k])
    fig.text(0.02, 0.975, "The same person, twice: what the records look like and how they disagree", fontsize=9.5,
             color=INK, weight="bold", va="top")
    fig.text(0.02, 0.935, "Each pair is one simulant as it appears in the registry stand-in and in the 500,000-record "
                          "finder file. Highlighted rows differ; the note names\nwhat the discrepancy looks like. "
                          "Simulated data: no real person is described.", fontsize=6.6, color=INK2, va="top",
             linespacing=1.4)
    return fig


def candidate_composite():
    fig = plt.figure(figsize=(180 * MM, 112 * MM))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1.0], left=0.005, right=0.995, top=0.875, bottom=0.145, wspace=0.08)
    ax_p = fig.add_subplot(gs[0])
    handles = pyramid(ax_p, name_size=5.4, label_size=5.6, gap=1.8, legend=False)
    right = gs[1].subgridspec(3, 1, height_ratios=[1.0, 1.0, 0.7], hspace=0.28)
    pairs = load_example_pairs()
    ids = pairs["pair"].unique().tolist()[:2]
    for i, k in enumerate(ids):
        record_card(fig.add_subplot(right[i]), pairs[pairs["pair"] == k], size=5.4, compact=True)
    deposit_inset(fig.add_subplot(right[2]), size=5.4)
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.0), ncol=6, frameon=False,
               fontsize=6.2, handlelength=1.2, handletextpad=0.5, columnspacing=1.1)
    fig.text(0.005, 0.985, "A Florida-scale simulated registry and finder files for testing record linkage", fontsize=9.5,
             color=INK, weight="bold", va="top")
    fig.text(0.005, 0.945, "Left: who is in the registry stand-in, by age, sex and race/ethnicity, against the cases FCDS "
                           "reports, with the commonest first names per group.\nRight: the same simulant in two files, "
                           "and what the deposit contains.", fontsize=6.4, color=INK2, va="top", linespacing=1.4)
    return fig