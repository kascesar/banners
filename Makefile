UV = uv
DOCS_OUTPUT_DIR = docs/
DOCS_FORMAT = google
.PHONY: docs
docs:
	$(UV) run pdoc --mermaid --math banners -o $(DOCS_OUTPUT_DIR) --docformat $(DOCS_FORMAT)

# Checks required by the milestone workflow before any work is reported as done.
.PHONY: lint test check
lint:
	$(UV) run ruff check banners tests scripts

# Tests marked manim are skipped by default (see pyproject.toml).
test:
	$(UV) run pytest

check: lint test

# README images (template gallery PNGs and showcase GIFs) in media/.
# Needs the dev extra; downloads Chromium the first time.
.PHONY: readme-images
readme-images:
	$(UV) run playwright install chromium
	$(UV) run python scripts/readme_images.py

# Development environment exactly as pinned in uv.lock.
uv-dev:
	$(UV) sync --extra dev

# Manual fallback: releases normally go through .github/workflows/release.yml when a
# vX.Y.Z tag is pushed. This target uploads from the local machine and needs a PyPI token.
.PHONY: publish
publish:
	rm -rf dist/
	$(UV) build
	$(UV) publish
