UV = uv
DOCS_OUTPUT_DIR = docs/
DOCS_FORMAT = google
.PHONY: docs
docs:
	$(UV) run pdoc --mermaid --math banners -o $(DOCS_OUTPUT_DIR) --docformat $(DOCS_FORMAT)

uv-dev:
	$(UV) pip install -e ".[dev]"

# Respaldo manual: la publicación normal la hace .github/workflows/release.yml al subir
# un tag vX.Y.Z. Este target sube desde el equipo local y necesita un token de PyPI.
.PHONY: publish
publish:
	rm -rf dist/
	$(UV) build
	$(UV) publish
