# M11 — Bilingual documentation site: Implementation Plan

> **For agentic workers:** execute with superpowers:executing-plans (inline, as
> `CLAUDE.md` requires). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A Quarto website in English and Spanish that teaches banners from
zero, published on GitHub Pages, plus the equation GIF in the README.

**Architecture:** A Quarto website project in `site/` with mirrored page trees
`site/en/` and `site/es/` (same file names), one sidebar per language and a
navbar EN/ES link rewritten by `site/lang-switch.js` to the same page in the
other language. Code blocks are plain (not executed by Quarto); a pytest file
runs them. Pictures come from `scripts/docs_images.py`, which builds a
temporary marimo notebook from named slide snippets, exports it and
screenshots each slide (the pattern of `scripts/readme_images.py`). pdoc
writes the API reference into the rendered site under `api/`. A GitHub
Action renders and publishes the site to the `gh-pages` branch.

**Tech Stack:** Quarto 1.9, pdoc, Playwright, ffmpeg, pytest, GitHub Actions.

**Spec:** `MILESTONES.md` → "M11 — Bilingual documentation site".

## Global Constraints

- Page list, identical under `site/en/` and `site/es/`: `index.qmd`, `get-started.qmd`, `look/{templates,palettes,themes,layouts,backgrounds}.qmd`, `slides/{cover,intro,section,closing}.qmd`, `content/{text,image,table,plot,graph,animated-graph,flow-animation,manim}.qmd`, `howto/{present,organization-template,manim-scene,cache}.qmd`, `examples.qmd`, `whats-new.qmd`.
- Every page opens with one sentence saying what it covers, shows code next to its result (image or GIF), and ends with a "Next" link following the reading order above.
- Every ```` ```python ```` block is self-contained (its own imports) and runs; a block whose first line is `# fragment` is not run. Blocks that import manim run only under the `manim` marker.
- Links between pages are relative; no link starts with `/`.
- Images live in `site/images/`; README media stays in `media/`.
- Writing rules from the maintainer: full sentences, explicit subject and object, explain the why by its practical effect, no slogans, no bold for drama. Spanish pages pass `hunspell -d es_CL -l` (proper nouns and code excepted) and are checked by eye for missing accents.
- No branded presets or brand assets (M10); the organization-template page uses a placeholder logo URL from Wikimedia Commons in the public domain.
- Commits per task on `milestone/m11-docs`, Conventional Commits, no `Co-Authored-By`. Verification for every task: `make check`; from Task 2 on also `quarto render site`.

## Review Focus

1. A page present in one language only: the EN/ES link would 404. `test_languages_have_the_same_pages` (Task 2).
2. A code block that depends on a previous block's variables fails when copied alone. Each block runs in a fresh namespace in `test_site_code_runs` (Task 2).
3. An image referenced by a page but never generated. `test_site_images_exist` (Task 2).
4. The site is served under `/banners/` on GitHub Pages, so absolute links break. `test_site_links_are_relative` (Task 2).
5. The EN/ES link on the API reference or the home page, where there is no mirror. `lang-switch.js` falls back to the other language's `index.html`; checked on the live site (Task 8).

---

### Task 1: Equation GIF in the README

**Files:**
- Modify: `scripts/readme_images.py` (new `record_player_gif`, called from `main()`), `README.md`, `tests/test_readme_images.py`
- Create: `media/equations.gif`

**Interfaces:**
- Produces: `gif_command(video: Path, out: Path, box: tuple[int, int, int, int], fps: int = 12, width: int = 800) -> list[str]` — the ffmpeg command that crops `box` (x, y, w, h) from the recording and writes a palette-optimized GIF.
- Produces: `record_player_gif(page, html: Path, out: Path, clicks: int = 5, step_ms: int = 1800) -> None` — opens the exported `example/ondas_electromagneticas.py`, finds the slide that holds the `MaxwellDerivationScene` player, records it while clicking `clicks` times.

- [ ] **Step 1: Write the failing test** `test_gif_command`: `gif_command(Path("v.webm"), Path("o.gif"), (10, 20, 300, 200))` contains `"crop=300:200:10:20"`, `"fps=12"`, `"scale=800:-1"`, `"palettegen"` and ends with `"o.gif"`.
- [ ] **Step 2: Run** `uv run pytest tests/test_readme_images.py -v` → FAIL.
- [ ] **Step 3: Implement** both functions. Recording uses a Playwright context with `record_video_dir`; the box is the slide canvas bounding box times the device scale factor; clicks go to the player iframe's stage.
- [ ] **Step 4: Run** `make readme-images`; look at `media/equations.gif` frame by frame (each derivation step readable, under 3 MB). Add it to the README under Showcase with the caption "Animations — a Manim derivation advancing one step per click, inside a marimo slide." `make check` → green.
- [ ] **Step 5: Commit** `feat(readme): equation derivation GIF recorded in marimo`.

### Task 2: Site skeleton, tests, build and CI check

**Files:**
- Create: `site/_quarto.yml`, `site/index.qmd` (redirects to `en/`), `site/lang-switch.js`, `site/styles.css`, every page of the Global Constraints list in `en/` and `es/` (title, one-line summary and "Next" link; `en/index.qmd`, `es/index.qmd`, `en/get-started.qmd` and `es/get-started.qmd` written in full)
- Create: `tests/test_site.py`
- Modify: `Makefile` (`docs`: `quarto render site` then `pdoc … -o site/_site/api`; `docs-preview`), `.gitignore` (`site/_site/`, `site/.quarto/`), `.github/workflows/ci.yml` (job `site`: `quarto-dev/quarto-actions/setup@v2`, `quarto render site`), `CLAUDE.md` (Commands and Architecture: the site), `pyproject.toml` if needed
- Delete: `docs/` (committed pdoc output)

**Interfaces:**
- Produces: `site/_quarto.yml` with sidebars `en` and `es` (contents = the page list in reading order, grouped as Get started / Look and feel / Slides / Content / How-to guides / Examples / What's new / API), navbar with `href: ../api/index.html`-style relative API link and an item with id `lang-switch`.
- Produces: `lang-switch.js`: swaps `/en/` ↔ `/es/` in `location.pathname`; on a page outside both, links to `en/index.html` or `es/index.html`.

- [ ] **Step 1: Write the failing tests** in `tests/test_site.py`:
  - `test_languages_have_the_same_pages`: sets of `*.qmd` paths relative to `site/en` and `site/es` are equal and equal the Global Constraints list.
  - `test_site_code_runs`: every non-fragment ```` ```python ```` block without `manim` runs with `exec` in a fresh namespace.
  - `test_site_manim_code_runs` (`@pytest.mark.manim`): same for blocks that import manim.
  - `test_site_images_exist`: every `](../images/…)`/`](../../images/…)` target exists.
  - `test_site_links_are_relative`: no markdown link target starts with `/`.
- [ ] **Step 2: Run** `uv run pytest tests/test_site.py -v` → FAIL (no `site/`).
- [ ] **Step 3: Build** the skeleton and the four full pages. Get started: install (pip/uv tabset), the 3-slide deck (configure + Cover + Section + Closing, one cell each), open in slide mode, full screen, next steps.
- [ ] **Step 4: Run** `make check`, `quarto render site`, `make docs` and open `site/_site/en/index.html`: sidebar, EN/ES switch and API link work locally.
- [ ] **Step 5: Commit** `feat(site): bilingual Quarto skeleton, Get started, tests and CI render check`.

### Task 3: Documentation images

**Files:**
- Create: `scripts/docs_images.py`, `site/images/*.png|gif`
- Modify: `Makefile` (`docs-images`), `tests/test_readme_images.py` (or new `tests/test_docs_images.py`)

**Interfaces:**
- Consumes: `export`, `shoot`, `make_gif` from `scripts/readme_images.py` (imported by path).
- Produces: `SHOTS: dict[str, str]` — image name → a Python snippet whose last expression is a slide; `notebook_source(shots: dict[str, str]) -> str` — a marimo notebook with one cell per shot, in order; `main()` writes `site/images/<name>.png`. GIFs (FlowAnimation, Manim) are recorded with `record_player_gif` from Task 1.

- [ ] **Step 1: Write the failing test** `test_notebook_source_has_one_cell_per_shot`: for `{"a": "Section(title='A')", "b": "Section(title='B')"}` the source has exactly two cells whose bodies end with those expressions, in that order, and parses with `ast.parse`.
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement**, then fill `SHOTS` for every picture the pages of Tasks 2 and 4–7 reference (named after the page: `get-started-deck`, `templates-gallery-*`, `palette-roles`, `cover-basic`, `content-plot`, …).
- [ ] **Step 4: Run** `make docs-images`; look at the images; `make check` (including `test_site_images_exist`) → green.
- [ ] **Step 5: Commit** `feat(scripts): generate documentation images`.

### Task 4: Look and feel (Templates, Palettes, Themes, Layouts, Backgrounds)

**Files:** `site/{en,es}/look/*.qmd`

- [ ] **Step 1:** Write the five EN pages. Templates: one line changes the deck, the six presets, what a template is made of. Palettes: colors by role (diagram of which role paints what), presets, a custom palette, a palette per slide, precedence slide > configure > template. Themes: font, heading font, title weight, icon stroke, scale. Layouts: how the template picks a layout from the slide type and its content. Backgrounds: color, gradient, image, automatic text contrast.
- [ ] **Step 2:** Write the five ES pages from the EN ones; run hunspell on them and fix accents.
- [ ] **Step 3: Run** `make check` and `quarto render site`.
- [ ] **Step 4: Commit** `docs(site): look and feel`.

### Task 5: Slides (Cover, Intro, Section, Closing)

**Files:** `site/{en,es}/slides/*.qmd`

- [ ] **Step 1:** EN pages: what the slide is for, a minimal example with its picture, a parameter table taken from the docstring, variants (Cover with photo, Section numbering and cell order, Closing with stats).
- [ ] **Step 2:** ES pages; hunspell.
- [ ] **Step 3: Run** `make check`, `quarto render site`.
- [ ] **Step 4: Commit** `docs(site): slides`.

### Task 6: Content elements

**Files:** `site/{en,es}/content/*.qmd`

- [ ] **Step 1:** EN pages, one per element: what it is, minimal example and result, options, how it follows the palette, limits (e.g. AnimatedGraph needs the marimo kernel; Manim needs the extra and system libraries; results are cached).
- [ ] **Step 2:** ES pages; hunspell.
- [ ] **Step 3: Run** `make check`, `uv run pytest -m manim tests/test_site.py`, `quarto render site`.
- [ ] **Step 4: Commit** `docs(site): content elements`.

### Task 7: How-to guides, Examples, What's new

**Files:** `site/{en,es}/howto/*.qmd`, `site/{en,es}/examples.qmd`, `site/{en,es}/whats-new.qmd`

- [ ] **Step 1:** EN pages. Present: slide mode, full screen, layout files. Organization template: logo URLs, palette, theme, photos (public-domain placeholder), and a note that the organization's own trademark rules apply. Manim scene: `next_section`, short steps, palette colors. Cache: where it lives, what invalidates it, how to clear it. Examples: the two notebooks with their GIFs and run commands. What's new: 0.6 and 0.5 notes with upgrade steps.
- [ ] **Step 2:** ES pages; hunspell.
- [ ] **Step 3: Run** `make check`, `quarto render site`.
- [ ] **Step 4: Commit** `docs(site): how-to guides, examples and release notes`.

### Task 8: Publish on GitHub Pages

**Files:**
- Create: `.github/workflows/site.yml` (on push to `main` and manual dispatch; permissions `contents: write`; uv sync dev, quarto setup, `make docs`, `quarto publish gh-pages site --no-render --no-prompt`)
- Modify: `README.md` (link to the site), `site/_quarto.yml` (`site-url`)

- [ ] **Step 1:** Write the workflow; `actionlint` if available, else review by eye.
- [ ] **Step 2:** Ask César before enabling GitHub Pages on the `gh-pages` branch (outward-facing setting).
- [ ] **Step 3:** After merge, check the live site: home, a page in each section, the EN/ES switch on a guide page (same page) and on the API page (other language's home), images load.
- [ ] **Step 4: Commit** `ci(site): publish the documentation to GitHub Pages`.

### Task 9: Close

- [ ] **Step 1:** César reviews the site (locally with `make docs-preview`, then live).
- [ ] **Step 2:** Close per `CLAUDE.md`: `make check`, `uv run pytest -m manim`, `quarto render site` output in the body, M11 `[x]`, Log line.
