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

Verified on 2026-11-24: `uv run pytest -m manim` on César's Fedora machine → 3 passed, 1 xfailed
(`example/showcase.py`, the error recorded in the Backlog). The LaTeX error in
`example/ondas_electromagneticas.py` was missing system packages, fixed with
`sudo dnf install texlive-standalone texlive-dvisvgm`.

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

## [x] M6 — One rendering model: Template = Palette + Theme + layouts

banners exists to present. Today it has two rendering modes that look and size
text differently: the fluid editorial style (sizes in `rem`, so text stays at
16–19 px even on a full-screen projector, which has drawn criticism) and
`Template` (a fixed 16:9 canvas sized in `cqw`). `Template` also ignores any
`palette`, so palettes and templates cannot be combined. This milestone keeps a
single model: every slide is drawn on the 16:9 canvas, and a template is
composed of a palette and a theme that can each be declared on their own.
It is a breaking release: **0.5.0**.

**Concepts**

- `Palette`: colors only, named by role. Fields: `primary`, `secondary`, `dark`,
  `closing_bg`, `light`, `text`, `muted`, `on_dark`, `panel`, `icon_color`
  (optional) and the optional sequences `section_colors` and `bar_colors`.
  These are exactly the color fields `Template` has today, moved out of it.
- `Theme`: the visual style that is not color. Fields: `font`, `heading_font`,
  `title_weight`, `icon_stroke` (stroke width of the line icons) and `scale`.
- `Template`: layouts, logos, photos, icons, bar on/off and split, and
  `auto_contrast`, plus one `palette` and one `theme` (its own defaults).
  Switching the template of an existing deck changes layouts, palette and theme
  together without touching the slides.

**Precedence** (resolved in one function, not per layout):
palette: slide `palette=` > `configure(palette=...)` > `template.palette`;
theme: `configure(theme=...)` > `template.theme`. A palette or theme declared by
the user replaces the template's one as a whole (no field-by-field merge).

**Changes**

- Every slide renders through the active template. Without
  `configure(template=...)`, a default `Template()` is used, whose palette is
  `ORANGE`. `ORANGE` takes the current `Template` default colors; `BLUE`,
  `GREEN`, `PURPLE` and `GRAY` are redefined by role from their current colors.
- `background=` (per slide or in `configure`) paints the canvas background of
  that slide instead of the layout color; when `Background.text_color()` returns
  a color, the text of that slide uses it.
- Removed, with no deprecation period (code that uses them fails with
  `TypeError`/`ImportError`): the editorial rendering in `banners/slides/` and
  `Slide` (`_render_banner`, `_render_content`, `_css_grid`, the `rem` sizes),
  `content_kind`, `icon=` on slides and in `configure`, `Palette.start/mid/end`,
  `Palette.text_*`, `Palette.gradient`, `SectionPalette` and `to_section_palette`.
- The six presets (`BECH`, `EXECUTIVE`, `INSTITUTIONAL`, `COSMOS`, `VIBRANT`,
  `TERRA`) are rewritten as `Template(palette=Palette(...), theme=Theme(...), ...)`
  with the same look as today. Their palettes and themes are reachable as
  `TERRA.palette` / `TERRA.theme`; no extra named constants.
- Content elements (`Text`, `Image`, `Graph`, `AnimatedGraph`, `Table`, `Plot`,
  `Manim`, `FlowAnimation`) stay independent of slides and configuration and
  keep working in a plain marimo cell.
- `Palette`, `Theme` and the presets are exported in `banners.__all__`; README
  and docstrings describe the new model (the full README rewrite is a later
  milestone). Notebooks in `test/` and `example/` are updated to the new API.

**Non-goals**: per-slide `theme=`; new icon sets (filled icons); new layouts or a
new visual identity; manim animations and the README rewrite (later milestones).

**Anti-goals**: a field-by-field merge between user and template palettes; any
slide text sized in `rem`/`px`; content elements importing `banners.config`.

**Acceptance criteria**
- `make check` → green.
- Tests in `tests/` cover: the precedence rules above (slide > configure >
  template for palette, configure > template for theme); `Palette` and `Theme`
  are usable without a `Template`; every preset renders `Cover`, `Intro`,
  `Section` (divider and with content) and `Closing` with its own palette and
  with `palette=BLUE`; `background=` changes the canvas background; every removed
  parameter raises `TypeError`; each content element renders without `configure()`.
- `grep -rnE "font-size:[0-9.]+(rem|px)" banners/` → no matches.
- `uv run pytest tests/test_notebooks.py` → the same notebooks pass as before
  (known xfails stay xfail).
- `pyproject.toml` version is `0.5.0`; `uv build` and `uvx twine check dist/*` pass.
- César reviews a private artifact gallery that renders every preset × layout,
  with and without a user palette, and presents one existing deck full screen in
  marimo slide mode to confirm text size.

Verified on 2026-11-24: César reviewed the gallery (electromagnetic-waves demo,
eight layouts per template) and presented `example/ondas_electromagneticas.py`
full screen; the text reads well. The Python release itself (tag `v0.5.0`) is
left to César.

---

## [x] M7 — Security and broken notebooks

Short fix milestone before the manim work: one security issue and the four
visual notebooks that do not run. M9 regenerates the README GIFs from these
notebooks, so they have to run first.

- **TLS verification.** `Slide._icon_src` downloads images by URL with
  `check_hostname = False` and `verify_mode = ssl.CERT_NONE`, so it accepts
  invalid or spoofed certificates. It is used by templates (logos, marks,
  photos given as paths or bytes) and by `Background.image(url)`. Remove both
  lines so the default context verifies the certificate and the host name. An
  image whose certificate fails is then omitted by templates (as any failing
  image already is) and raises when `Background.image(url)` is created.
- **`test/04_graph.py` and `test/05_animated_graph.py`** do not compile: the
  documentation cell uses `mo.md(r"""...""")` and the code example inside it
  contains another triple quote. Use `r'''...'''` for the outer string.
- **`test/07_plot.py`** raises `MultipleDefinitionError` because several cells
  import `matplotlib.pyplot as plt`. Import it in one cell and pass `plt` to the
  others.
- **`example/showcase.py`** raises `NameError: name 'MathTex' is not defined`:
  add `MathTex`, `FadeOut` and `WHITE as MW` to its manim imports cell.

**Non-goals**: the other Backlog bugs (`AnimatedGraph` destination labels,
mixed-format gradients, `Closing` stats weight).

**Acceptance criteria**
- `make check` → green, including a unit test that captures the SSL context used
  by `Slide._icon_src` for a URL (no network) and asserts
  `verify_mode == ssl.CERT_REQUIRED` and `check_hostname is True`.
- `tests/test_notebooks.py` has no `KNOWN_FAILURES` entries left; `uv run pytest
  tests/test_notebooks.py` passes `test/04`, `05` and `07`.
- `uv run pytest -m manim` → `example/showcase.py` passes (no xfail).
- The four items are removed from the Backlog.

---

## [x] M8 — Professional manim animations, player, and palette-aware plots

Today the manim animations look like a foreign piece on the slide: a fixed navy
background (`#0f172a`), fixed node colors, a black video stage and gray buttons,
while M6 made most slides light and palette-driven. Each step also takes 0.5 s
plus a 0.2 s wait, which feels slow. César wants the animations to belong to the
deck's palette, be faster and more direct, and render faster, without losing
their visual appeal. He gave freedom on the motion details, grounded in the
research below.

**Research (2026-11-24)** that sets the motion rules:
- Duration: most UI animations should last 100–400 ms; at 500 ms they start to
  feel slow; 200–300 ms for elements entering
  ([NN/g](https://www.nngroup.com/articles/animation-duration/),
  [Material Design 3](https://m3.material.io/styles/motion/easing-and-duration/applying-easing-and-duration)).
- Easing: ease-out for entrances, smooth for moves; no bounce or overshoot
  ([NN/g](https://www.nngroup.com/articles/animation-duration/),
  [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/motion)).
- One focal change per click; no decorative motion; no trailing waits, because
  the click is the pause; hard cut from the last frame between steps
  ([manim-slides example](https://raw.githubusercontent.com/jeertmans/manim-slides/main/example.py),
  [Manim output docs](https://docs.manim.community/en/stable/tutorials/output_and_config.html)).
- Match the slide by painting the scene background with the slide color; use
  transparency only when something other than a flat color must show through.

**Decisions**
- **Palette hand-off (approach A, chosen by César).** Content elements that can
  follow the palette implement `_with_palette(palette) -> same type`, which
  returns a styled copy. `Template._content` calls it before rendering the item.
  A content element still never reads `banners.config`; a standalone element
  renders with `Palette()` (the `ORANGE` defaults) for animations, and exactly as
  today for `Plot`. The palette is part of the manim cache key.
- **Background (chosen by César):** opaque MP4 painted with `palette.panel`, the
  color of the box that holds visuals. No transparent video.
- **FlowAnimation colors:** background `panel`; node colors cycle through
  `section_colors`, else `(primary, secondary)`; node names in `text`, details
  and arrows in `muted`.
- **Motion:** each step plays one `self.play` of **0.25 s**: the node fades in
  with a short shift and its incoming arrows draw, with `rate_func=ease_out_cubic`.
  No `Write`, no scale-in, no `self.wait()` at the end of a step.
- **Frame rate:** 30 fps for every quality (manim's "low" preset is 15 fps,
  which leaves a 0.25 s step with about 4 frames). Resolutions stay 480p/720p/1080p.
- **`Manim(scene)` with a custom scene:** banners sets `background_color` to
  `palette.panel` as a default; the scene keeps any color it sets itself.
- **`PipelineScene`:** becomes `PipelineScene(palette=None)` with the same motion
  rules and palette colors. `Manim` accepts a scene factory and calls it with the
  palette, which also fixes the documented `Manim(PipelineScene, interactive=True)`,
  broken today with `TypeError: Scene.render() missing 1 required positional argument`.
- **Player (`_manim_widget.js`):** no black stage; controls take colors from the
  palette passed by Python (`muted` for idle controls, `primary` for the active
  autoplay toggle), on a transparent bar, sized relative to the surrounding text.
- **Python and manim (approved by César):** the minimum Python becomes 3.11 so
  the `manim` extra can require `manim>=0.21`, which reports a 2.2× faster Cairo
  renderer and faster scene hashing
  ([v0.21 notes](https://gle-graphics.org/blog/manim-v021-typst-cairo-speedup/),
  secondary source; verified by measuring). Users on Python 3.10 stay on 0.5.1,
  so the next release is 0.6.0. `requires-python`, ruff `target-version`, the CI
  matrix (3.11 and 3.12) and `CLAUDE.md` change accordingly.
- **Plots** (decided with César earlier): the template restyles a matplotlib
  figure placed on a slide: axes, ticks, labels and legend take a color readable
  on `panel`; only lines and patches with matplotlib's automatic cycle colors
  (`C0`, `C1`, …) take the palette colors (`primary`, `secondary`, then
  `section_colors`). Colors set by hand are kept.

**Non-goals**: transparent video; plotly restyling; new scene types; Typst math.

**Acceptance criteria**
- `make check` → green, with unit tests (no manim) for: `_with_palette` on
  `FlowAnimation`, `Manim` and `Plot` returns a copy with the palette colors and
  leaves the original unchanged; the palette changes the manim cache key; the
  template calls `_with_palette` for items that have it; a figure on a slide gets
  panel-readable axes and palette colors on automatic lines, a hand-set line
  color is unchanged, and the same `Plot` outside a slide is unchanged; content
  modules still do not import `banners.config`.
- `uv run pytest -m manim` → green, including `Manim(PipelineScene, interactive=True)`
  rendering one video per section, and a 4-node `FlowAnimation` whose sections
  each last at most 0.3 s.
- A cold render of `FlowAnimation(["Ingest", "Validate", "Transform", "Load"], quality="low")`
  is measured before and after on César's machine (baseline 2.0 s with manim
  0.19.1 on Python 3.10) and the result is written in the closing commit; it
  must not be slower than the baseline.
- `requires-python = ">=3.11"`, the `manim` extra requires `manim>=0.21`, CI runs
  on 3.11 and 3.12, and `pyproject.toml` version is `0.6.0`.
- César reviews `test/08_manim.py`, `test/09_flow_animation.py` and
  `example/showcase.py` in marimo slide mode, with at least two different palettes.

---

## [x] M9 — Short, striking README

The README is the first thing people see on GitHub and PyPI. Its job is to make
them want to try banners, not to document it: the how-to guide moves to a
GitHub Pages site (M11). The current README (445 lines, three GIFs in the 0.2
style) reads as a reference manual.

Design (approved by César, 2026-11-24):
- **Short.** A one-line pitch, install, a quick start of a few lines, the two
  galleries below, and links to the docs. No API reference, no upgrade notes
  beyond one line pointing to the changelog section of the docs.
- **Template gallery, 2×3.** The same slide (a `Section` with a title, three
  bullets and a small matplotlib chart) rendered with the six public templates:
  default `Template()`, `EXECUTIVE`, `INSTITUTIONAL`, `COSMOS`, `VIBRANT`,
  `TERRA`. `BECH` is never shown (it imitates a real bank).
- **Showcase GIFs, one per row (1×3).** One GIF per part of
  `example/showcase.py` (01 slide types, 02 content types, 03 backgrounds).
  Hard cuts between slides, no transitions, about 1.5 s per slide, looping.
- **Generated, not hand-made.** A script renders the slides in headless
  Chromium (Playwright) and writes PNGs and GIFs to `media/`; `make
  readme-images` runs it. The old root GIFs are deleted.
- **Absolute image URLs** (`raw.githubusercontent.com/.../main/media/...`),
  because PyPI does not resolve relative paths.
- No organization brand assets in the README or the images.

Out of scope: the texts of the `test/` notebooks and the detailed usage guide
(both go to M11).

**Acceptance criteria**
- `README.md` is at most 120 lines.
- Every Python code block in the README runs against the current API, checked
  by a test that extracts and executes them.
- `make readme-images` regenerates the 6 template PNGs and the 3 GIFs; every
  GIF has hard cuts (no frame blends two slides).
- César approves the README rendered on GitHub.

---

## [ ] M10 — Templates for open-source projects

Presets themed after open-source projects (Debian first; candidates: Fedora,
Ubuntu, marimo, NumPy, pandas, matplotlib, Hydra), with the project name and
its logo linked from an official or Wikimedia Commons URL, never stored in the
repo. **Needs research before planning**: each project's trademark or logo
policy decides whether a preset may use its name, colors and logo. Debian's
"Open Use Logo" has a free license; Fedora (Red Hat), Ubuntu (Canonical) and
Hydra (Meta) are trademarks with restrictive policies; the others are
unverified. Only projects whose policy allows it get a preset.

---

## [ ] M11 — Usage guide on GitHub Pages

A GitHub Pages site with the detailed guide that leaves the README in M9:
installation, slides, content elements, palettes, themes, templates,
backgrounds, animations, and the API reference (pdoc). Includes rewriting the
texts of the `test/` notebooks, which describe the old design. Needs a
brainstorming pass before planning.

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
- `Cover` and `Closing` accept `content=` and `footer=`, but the template layouts do not draw
  them, so the values are silently ignored. Either draw them or remove the parameters.
- `Closing` stats values use a fixed `font-weight:700` instead of `Theme.title_weight`.
- `test/01_intro.py` and `example/showcase.py` prose still describes the removed `icon`
  parameter and the `start`/`mid`/`end` palette (M11 rewrites the notebook texts).
- A local `make publish` would put `.claude/settings.local.json` in the sdist: hatch only
  reads the project `.gitignore`, not the user's global git ignore file. The CI release
  builds from a clean checkout and is not affected. Fix: an `exclude` rule in `pyproject.toml`.

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
| 2026-11-24 | M6 | `milestone/m6-palette-theme-template` | One rendering model on the 16:9 canvas: `Template` = `Palette` (colors by role) + `Theme` (fonts, title weight, icon stroke, scale) + layouts; palette precedence slide > configure > template; editorial style, `content_kind`, `icon=` and `SectionPalette` removed; version 0.5.0. |
| 2026-11-24 | M7 | `milestone/m7-security-notebooks` | TLS verification restored in `Slide._icon_src`; `test/04`, `05`, `07` and `example/showcase.py` run (no known notebook failures left); plotly added to the dev extra and CI for `test/07_plot.py`. |
| 2026-11-24 | M8 | `milestone/m8-manim-palette` | Python ≥ 3.11 and manim ≥ 0.21; plots and animations follow the slide palette (`_with_palette`); manim renders on `palette.panel` at 30 fps with 0.25 s ease-out steps (4-node flow cold render 2.0 s → 1.62 s); player controls above the video; `PipelineScene` fixed; version 0.6.0. |
| 2026-11-24 | M9 | `milestone/m9-readme` | README of 95 lines with a 2×3 template gallery and three showcase GIFs, generated by `make readme-images` (Playwright) into `media/`; README code tested; Cover subtitle no longer overlaps a wrapped title; marimo-defined manim scenes invalidate the cache; showcase titles as MP4. |
