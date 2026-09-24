"""Render the three master-graphic candidates to figures/ (PNG at 300 dpi and PDF).

Paper-tier work: it reads only results/ and reference/. Run after
pipeline/qa_age_sex.py and pipeline/example_pair.py have written their summaries.

    uv run python pipeline/draw_candidate_figures.py
"""

from __future__ import annotations

from pathlib import Path

from simulated_data_for_fcds_scale_rl import figures as F

OUT = Path(__file__).resolve().parent.parent / "figures"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, make in [("candidate_1_pyramid", F.candidate_pyramid),
                       ("candidate_2_record_pairs", F.candidate_record_pairs),
                       ("candidate_3_composite", F.candidate_composite)]:
        fig = make()
        for ext in ("png", "pdf"):
            fig.savefig(OUT / f"{name}.{ext}", dpi=300)
        print("wrote", OUT / f"{name}.png")


if __name__ == "__main__":
    main()
