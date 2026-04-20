UV = uv
DOCS_OUTPUT_DIR = docs/
DOCS_FORMAT = google
.PHONY: docs
docs:
	$(UV) run pdoc --mermaid --math banners -o $(DOCS_OUTPUT_DIR) --docformat $(DOCS_FORMAT)
