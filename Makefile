.PHONY: paper test lint figures checks
paper:                   ## render docx + html from frozen results
	uv run quarto render --to docx
test:
	uv run pytest
lint:
	uv run ruff check .
figures:                 ## redraw the paper's figures into figures/ from results/
	uv run python pipeline/draw_candidate_figures.py
checks:                  ## regenerate and execute the acceptance-check notebook against the release
	uv run python notebooks/make_acceptance_checks.py
