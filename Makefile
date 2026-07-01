.PHONY: paper test lint
paper:                   ## render docx + html from frozen results
	quarto render
test:
	uv run pytest
lint:
	uv run ruff check .