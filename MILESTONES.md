# Milestones

Status: `[ ]` pending · `[x]` done · `[!]` blocked (reason written below it)

Rules for Claude Code are in `CLAUDE.md` → "Working by milestones".
One milestone per session, one branch per milestone.
The implementation plan of each milestone is saved in `plans/<id>-<slug>.md`.

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

Verified: the CI workflow runs green on GitHub (Python 3.10 and 3.12).

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

Pending verification by César: `uv run pytest -m manim` on César's Fedora machine with the system libraries
(`example/ondas_electromagneticas.py` fails with `ValueError: latex error converting to dvi`
because the LaTeX class `standalone.cls`, used by the default `MathTex` template, is missing;
`kpsewhich standalone.cls` finds nothing and `dvisvgm` is not on the PATH either.
`test/08_manim.py` and `test/09_flow_animation.py` pass; `example/showcase.py` stays xfail
because of the error recorded in the Backlog).

`tests/test_notebooks.py` joins the M3 CI without workflow changes: the CI runs
`uv run pytest` and `addopts = "-m 'not manim'"` leaves the manim notebooks out.

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

Verified on 2026-11-23: the Trusted Publisher is registered on PyPI and the `v0.4.0` tag published 0.4.0. TestPyPI (`rc` tags) has not been tried yet.

---

## Backlog

Unplanned items found while working. Promote to a milestone when relevant.

- `banners/scenes/pipeline.py` and other `ImportError` messages suggest `uv pip install 'banners[manim]'`,
  but the package on PyPI is called `marimo-banners`.
- `AnimatedGraph._parse` loses the label of an edge destination node: `A --> B[Validate]`
  leaves `B` labeled `"B"`. `_edge_re` is not anchored to the end of the line and the lazy
  label group accepts an empty match. It shows in `test/05_animated_graph.py` (`D[Load]`
  appears as "D"). Test: `tests/test_animated_graph.py::test_parse_destination_label` (xfail).
- `background._parse_first_color` searches each format over the whole string in a fixed order
  (`#rrggbbaa`, `#rrggbb`, `#rgba`, `#rgb`, `rgb()`), so in a gradient with mixed formats the
  first color does not win: `linear-gradient(#fff, #000000)` yields black and the automatic
  text turns white over a white start. Test:
  `tests/test_background.py::test_parse_first_color_gradient_mixed_formats_first_wins` (xfail).
- `test/04_graph.py` and `test/05_animated_graph.py` do not compile (`SyntaxError`): the
  documentation cell uses `mo.md(r"""...""")` and the code example inside it contains another
  triple quote (`Graph("""...`), which closes the string too early. Test:
  `tests/test_notebooks.py` (xfail).
- `test/07_plot.py` does not run: several cells import `matplotlib.pyplot as plt` and marimo
  raises `MultipleDefinitionError`. Test: `tests/test_notebooks.py` (xfail).
- `example/showcase.py` fails with `NameError: name 'MathTex' is not defined`: the
  `BasicScene` cell takes `MathTex`, `FadeOut` and `MW` as parameters, but no cell defines
  them (the imports cell only brings `Scene`, `Text as MT`, `Write`, `FadeIn`, `Create`,
  `Line`, `LEFT`, `RIGHT` and `UP`). Test: `tests/test_notebooks.py` (xfail, `manim` marker).
- `Slide._icon_src` disables TLS verification (`check_hostname = False`,
  `verify_mode = ssl.CERT_NONE`) when downloading icons and images by URL, so it accepts
  invalid or spoofed certificates. It affects `icon=` and `Background.image(url)`.
- Regenerate the README GIFs (`demo-1-slide-types.gif`, `demo-2-content-types.gif`,
  `demo-3-backgrounds.gif`) with the 0.3 editorial design; today they show the 0.2 style
  (the README warns about it in a note).
- The texts of the `test/` notebooks describe the previous design (for example,
  `test/01_intro.py` says "Compact gradient banner" and "Dark panel with left border").
- A local `make publish` would put `.claude/settings.local.json` in the sdist: hatch only
  reads the project `.gitignore`, not the user's global git ignore file. The CI release
  builds from a clean checkout and is not affected. Fix: an `exclude` rule in `pyproject.toml`.
- (Optional) `configure(font=...)` to set a corporate typeface on every slide.

---

## Log

| Date | Milestone | Branch | Summary |
|------|-----------|--------|---------|
| 2026-11-23 | M1 | `milestone/m1-repo-hygiene` | Removes the broken `layout_file` from `test/08_manim.py`, deletes `layouts/test.slides.json` and `README.org`; adds ruff and fixes its findings. |
| 2026-11-23 | M2 | `milestone/m2-unit-tests` | pytest suite in `tests/` (64 tests + 2 xfail for errors recorded in the Backlog), `_state` fixture, `manim` marker. |
| 2026-11-23 | M3 | `milestone/m3-ci` | Workflow `.github/workflows/ci.yml` (Python 3.10 and 3.12, `uv sync --locked` without extras, `ruff check` and `pytest`) and CI badge in the README. |
| 2026-11-23 | M4 | `milestone/m4-notebook-smoke` | Smoke test `tests/test_notebooks.py` that runs the 12 notebooks (4 with the `manim` marker, 4 xfail for errors recorded in the Backlog). |
| 2026-11-23 | M5 | `milestone/m5-release` | Workflow `release.yml` that publishes to PyPI with Trusted Publishing when a `v*` tag is pushed (TestPyPI if the tag contains `rc`) and fails if the tag does not match the version; release steps in `CLAUDE.md`. |
| 2026-11-23 | — | `design/editorial` | Editorial redesign of the slides (César's patch) plus visual fixes: icons without overlap, contrast on dark backgrounds, `Intro` summary size; docstrings, README with "Upgrading from 0.2" and version 0.3.0. |
