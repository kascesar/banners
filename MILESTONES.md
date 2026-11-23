# Milestones

Status: `[ ]` pending · `[x]` done · `[!]` blocked (reason written below it)

Rules for Claude Code are in `CLAUDE.md` → "Working by milestones".
One milestone per session, one branch per milestone.

---

## [x] M1 — Repo hygiene

Fix small inconsistencies so later milestones start from a clean base.

- `test/08_manim.py` references `layouts/08_manim.slides.json`, which does not exist.
  Either create `test/layouts/08_manim.slides.json` (same shape as
  `example/layouts/showcase.slides.json`) or remove the `layout_file` argument.
- Decide what to do with `layouts/test.slides.json` at the repo root (empty
  `{"type":"slides","data":{}}`, not referenced anywhere): delete it or document it.
- `README.org` and `README.md` coexist: confirm which one is canonical
  (`pyproject.toml` uses `README.md`) and remove or sync the other.
- Add `ruff` to the `dev` extra and a `[tool.ruff]` section in `pyproject.toml`
  (line-length 100, target py310). Fix what `ruff check` reports, without behavior changes.

**Acceptance criteria**
- `grep -rn "layout_file" test example` → every referenced file exists (relative to the notebook).
- `uv run ruff check banners` → exit 0.
- `uv run python -c "import banners; print(banners.__all__)"` → works.

---

## [x] M2 — Unit tests for pure logic

Create a pytest suite in `tests/` (not `test/`, which holds marimo notebooks).

- Add `pytest` and `pytest-cov` to the `dev` extra and `[tool.pytest.ini_options]` in `pyproject.toml`
  with `testpaths = ["tests"]` and a `manim` marker skipped by default.
- `tests/conftest.py`: fixture that snapshots and restores `banners.config._state`.
- Cover at least:
  - `config`: `configure()` only overrides passed args; resets section counter;
    `_next_section_number()` returns `"01"`, `"02"`, …
  - `Section` auto-numbering across consecutive instances and after `configure()`.
  - `palette`: `Palette.gradient`, `to_section_palette()` darkens `start`, the 5 presets exist.
  - `background`: `_parse_first_color` for named colors, `#rgb`/`#rgba`/`#rrggbb`/`#rrggbbaa`,
    `rgb()`/`rgba()` (0–255 and 0–1 ranges),
    gradients (first color wins), and unparseable input → `None`;
    `text_color()` returns white on dark, `#1f2937` on light.
  - `AnimatedGraph`: `_parse` for `graph LR` and `graph TD`, labels with `[...]`,
    edge labels; `_layout` on a chain, a fork, and a cycle (must terminate);
    `_build_svg` returns SVG with one `.ag-node` per node.
  - `Slide`: `_render_item` dispatch (`str`, `Text`, object with `.render()`, passthrough)
    and `_render_content` with 1 vs N items.

**Acceptance criteria**
- `uv run pytest` → all green, ≥ 30 tests, runs without manim installed.
- `uv run pytest --cov=banners --cov-report=term` → ≥ 60% on
  `config.py`, `palette.py`, `background.py`, `content/animated_graph.py`.
- No changes to library behavior (only tests and config). If a test reveals a bug,
  mark it `@pytest.mark.xfail(reason=...)` and add the bug to the Backlog.

---

## [x] M3 — CI on GitHub Actions

- `.github/workflows/ci.yml`: on push and pull_request, matrix Python 3.10 / 3.12,
  install with `uv` (`astral-sh/setup-uv`), run `ruff check` and `pytest`.
- Manim tests are not run in CI (marker skipped by default).
- Add a CI badge to `README.md`.

**Acceptance criteria**
- Workflow file passes `uvx actionlint` (or is valid YAML if actionlint is unavailable).
- Locally, the exact commands used by the workflow succeed.
- After push, the workflow run is green (César verifies on GitHub).

Pendiente de verificación de César: que el workflow corra verde tras el push.

---

## [x] M4 — Smoke test for the visual notebooks

Make sure every notebook in `test/` and `example/` at least executes without errors.

- `tests/test_notebooks.py`: parametrize over `test/*.py` and `example/*.py`,
  run each with `uv run python <file>` (they all call `app.run()`) in a subprocess
  with a timeout, and assert exit code 0.
- Notebooks that need manim (`08_manim.py`, `09_flow_animation.py`, any example using it)
  are marked `manim`.
- Add it to CI (non-manim subset).

**Acceptance criteria**
- `uv run pytest tests/test_notebooks.py` → green for all non-manim notebooks.
- `uv run pytest -m manim` → green locally on César's Fedora (with system libs installed).

Pendiente de verificación de César: uv run pytest -m manim en su Fedora con las libs del sistema
(`example/ondas_electromagneticas.py` falla con `ValueError: latex error converting to dvi`
porque falta la clase LaTeX `standalone.cls`, que usa la plantilla por defecto de `MathTex`;
`kpsewhich standalone.cls` no encuentra nada y `dvisvgm` tampoco está en el PATH.
`test/08_manim.py` y `test/09_flow_animation.py` pasan; `example/showcase.py` queda xfail
por el error anotado en el Backlog).

La prueba `tests/test_notebooks.py` entra al CI de M3 sin cambios en el workflow: el CI
ejecuta `uv run pytest` y `addopts = "-m 'not manim'"` deja fuera los notebooks con manim.

---

## [x] M5 — Automated release to PyPI

- `.github/workflows/release.yml`: on tag `v*`, build with `uv build` and publish
  using PyPI Trusted Publishing (no API token in secrets).
- Check that the tag matches `project.version` in `pyproject.toml`; fail otherwise.
- Document the release steps in `CLAUDE.md` → Commands (replace `make publish`).

**Acceptance criteria**
- Workflow valid (actionlint).
- `uv build` locally produces sdist + wheel, and `uvx twine check dist/*` passes.
- César configures the Trusted Publisher on PyPI and a test tag publishes
  (can be tested first against TestPyPI).

Pendiente de verificación de César: configurar el Trusted Publisher en PyPI (y TestPyPI si aplica) y publicar con un tag de prueba.

---

## Backlog

Unplanned items found while working. Promote to a milestone when relevant.

- `banners/scenes/pipeline.py` y otros mensajes de `ImportError` sugieren `uv pip install 'banners[manim]'`,
  pero el paquete en PyPI se llama `marimo-banners`.
- `AnimatedGraph._parse` pierde la etiqueta del nodo destino de una arista: `A --> B[Validar]`
  deja `B` con etiqueta `"B"`. `_edge_re` no está anclado al final de la línea y el grupo
  perezoso de la etiqueta acepta vacío. Se nota en `test/05_animated_graph.py` (`D[Load]`
  aparece como "D"). Prueba: `tests/test_animated_graph.py::test_parse_destination_label` (xfail).
- `background._parse_first_color` busca cada formato en todo el string en orden fijo
  (`#rrggbbaa`, `#rrggbb`, `#rgba`, `#rgb`, `rgb()`), así que en un gradiente con formatos
  mezclados no gana el primer color: `linear-gradient(#fff, #000000)` da negro y el texto
  automático queda blanco sobre un inicio blanco. Prueba:
  `tests/test_background.py::test_parse_first_color_gradient_mixed_formats_first_wins` (xfail).
- `test/04_graph.py` y `test/05_animated_graph.py` no compilan (`SyntaxError`): la celda de
  documentación usa `mo.md(r"""...""")` y el ejemplo de código de adentro contiene otra
  triple comilla (`Graph("""...`), que cierra el string antes de tiempo. Prueba:
  `tests/test_notebooks.py` (xfail).
- `test/07_plot.py` no se ejecuta: varias celdas importan `matplotlib.pyplot as plt` y marimo
  lanza `MultipleDefinitionError`. Prueba: `tests/test_notebooks.py` (xfail).
- `example/showcase.py` falla con `NameError: name 'MathTex' is not defined`: la celda de
  `BasicScene` recibe `MathTex`, `FadeOut` y `MW` como parámetros, pero ninguna celda los
  define (la celda de imports solo trae `Scene`, `Text as MT`, `Write`, `FadeIn`, `Create`,
  `Line`, `LEFT`, `RIGHT` y `UP`). Prueba: `tests/test_notebooks.py` (xfail, marca `manim`).
- `Slide._icon_src` desactiva la verificación TLS (`check_hostname = False`,
  `verify_mode = ssl.CERT_NONE`) al descargar íconos e imágenes por URL, así que acepta
  certificados inválidos o suplantados. Afecta a `icon=` y a `Background.image(url)`.
- Regenerar los GIFs del README (`demo-1-slide-types.gif`, `demo-2-content-types.gif`,
  `demo-3-backgrounds.gif`) con el diseño editorial de la 0.3; hoy muestran el estilo 0.2
  (el README lo advierte en una nota).
- Los textos de los notebooks de `test/` describen el diseño anterior (por ejemplo,
  `test/01_intro.py` dice "Compact gradient banner" y "Dark panel with left border").
- (Opcional) `configure(font=...)` para definir una tipografía corporativa en todas las slides.

---

## Log

| Date | Milestone | Branch | Summary |
|------|-----------|--------|---------|
| 2026-11-23 | M1 | `milestone/m1-repo-hygiene` | Quita `layout_file` roto de `test/08_manim.py`, borra `layouts/test.slides.json` y `README.org`; agrega ruff y corrige sus hallazgos. |
| 2026-11-23 | M2 | `milestone/m2-unit-tests` | Suite pytest en `tests/` (64 pruebas + 2 xfail por errores anotados en el Backlog), fixture de `_state`, marca `manim`. |
| 2026-11-23 | M3 | `milestone/m3-ci` | Workflow `.github/workflows/ci.yml` (Python 3.10 y 3.12, `uv sync --locked` sin extras, `ruff check` y `pytest`) y badge de CI en el README. |
| 2026-11-23 | M4 | `milestone/m4-notebook-smoke` | Prueba de humo `tests/test_notebooks.py` que ejecuta los 12 notebooks (4 con marca `manim`, 4 xfail por errores anotados en el Backlog). |
| 2026-11-23 | M5 | `milestone/m5-release` | Workflow `release.yml` que publica en PyPI con Trusted Publishing al subir un tag `v*` (TestPyPI si el tag contiene `rc`) y falla si el tag no coincide con la versión; pasos de release en `CLAUDE.md`. |
| 2026-11-23 | — | `design/editorial` | Rediseño editorial de las slides (patch de César) más correcciones visuales: íconos sin superposición, contraste en fondos oscuros, tamaño del resumen de `Intro`; docstrings, README con "Upgrading from 0.2" y versión 0.3.0. |
