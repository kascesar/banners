UV = uv
DOCS_OUTPUT_DIR = docs/
DOCS_FORMAT = google
.PHONY: docs
docs:
	$(UV) run pdoc --mermaid --math banners -o $(DOCS_OUTPUT_DIR) --docformat $(DOCS_FORMAT)

uv-dev:
	$(UV) pip install -e ".[dev]"

.PHONY: publish
publish:
	rm -rf dist/
	$(UV) build
	$(UV) publish
