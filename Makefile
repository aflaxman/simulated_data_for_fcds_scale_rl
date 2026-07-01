.PHONY: paper test lint
paper:                   ## render docx + html from frozen results
	uv run quarto render --to docx
test:
	uv run pytest
lint:
	uv run ruff check .