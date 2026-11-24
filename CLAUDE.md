# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working by milestones

Work is planned in `MILESTONES.md` and follows the `superpowers` plugin flow
(spec → plan → TDD → verification). Where a superpowers skill disagrees with
this file, this file wins.

When asked to "take the next milestone":

1. **Pick.** Read `MILESTONES.md` and take the **first** milestone whose status
   is `[ ]`. Its description is the spec and its acceptance criteria are the
   definition of done. If the description is ambiguous, ask before planning.
2. **Branch.** Create `milestone/<id>-<slug>` (e.g. `milestone/m6-font`) in the
   main checkout. Do not create worktrees (`using-git-worktrees`) unless asked.
3. **Plan.** Use `writing-plans` and save the plan to `plans/<id>-<slug>.md`
   (e.g. `plans/m6-font.md`). Every acceptance criterion must map to at least one
   task, and each task names the test or command that proves it. Wait for the
   maintainer to approve the plan before writing code.
4. **Execute.** Use `executing-plans` (inline). Do not use
   `subagent-driven-development` or `dispatching-parallel-agents` unless asked.
   - Logic in `banners/` follows `test-driven-development`: write a failing
     pytest test in `tests/` first, then the code.
   - Visual changes are checked with the notebooks in `test/` (marimo); TDD does
     not apply to those notebooks.
   - Any failing test or wrong render goes through `systematic-debugging`
     before a fix is proposed.
   - Stay inside the milestone. Unrelated issues go to the **Backlog** section
     of `MILESTONES.md`, not into the code.
5. **Commit.** Commit after each task on the milestone branch only. Commit
   messages follow Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`,
   `chore:`) and carry no `Co-Authored-By` line. Never commit on `main`.
6. **Verify.** Before claiming the milestone is done, apply
   `verification-before-completion`: run `make check` and every verification
   command listed in the milestone, and paste their output in the body of the
   last commit.
7. **Close.** Mark the milestone `[x]`, add a one-line entry to the **Log**
   section (date, branch, summary) and commit. `finishing-a-development-branch`
   stops here: never merge, push, open a PR or delete branches; the maintainer
   reviews, squashes if needed and merges. Do not start the next milestone in
   the same session.
8. **Blocked.** If a criterion cannot be met, mark the milestone `[!]`, write
   why under it, commit, and stop.

New ideas that are not a milestone yet go through `brainstorming`; the outcome
is written as a new `[ ]` milestone in `MILESTONES.md` (description plus
acceptance criteria), not as a separate design document. Before asking the
maintainer for a review of finished work, `requesting-code-review` may be used.

## Commands

```bash
# Install (always use uv, never pip)
uv sync                          # core only, exactly as pinned in uv.lock
uv sync --extra manim            # + manim (needs system libs, see README)
uv sync --extra dev              # dev tools: hatch, pdoc, pandas, plotly, manim, ruff, pytest
# Do not mix in `uv pip install`: `uv run` re-syncs to uv.lock and can leave
# packages from another resolution next to it (incompatible versions).

# Visual reference notebooks (one per feature)
uv run marimo edit test/01_intro.py        # ... through test/10_background.py
uv run marimo edit example/showcase.py     # full demo deck

# Checks (run before claiming any work is done)
make lint                        # ruff check banners tests
make test                        # pytest (manim tests skipped)
make check                       # lint + test

# Docs
make docs                        # pdoc → docs/

# Release: .github/workflows/release.yml publishes to PyPI on a `v*` tag.
# 1. Bump `version` in pyproject.toml (e.g. 0.2.3) and commit it.
# 2. Tag that commit with the same version and push the tag:
git tag v0.2.3
git push origin v0.2.3
# The workflow fails if the tag (without `v`) differs from pyproject's version.
# Tags containing `rc` (e.g. v0.2.3rc1) go to TestPyPI instead of PyPI.
# `make publish` remains as a manual fallback (needs a local PyPI token).
```

### Tests

- `test/` holds **marimo notebooks** for visual validation, not pytest tests.
  Every notebook ends with `if __name__ == "__main__": app.run()`.
- Automated tests (pytest) live in `tests/`. Run them with `uv run pytest`;
  `tests/conftest.py` restores `banners.config._state` after every test.
- Anything that requires manim or system libraries (cairo, pango, ffmpeg) must be
  marked `@pytest.mark.manim` and is skipped by default.

---

## Architecture

`banners` is a **marimo presentation library** published on PyPI as `marimo-banners`.
Every slide calls `.render()`, which returns a `mo.Html` 16:9 canvas drawn by the
active `Template`, displayed directly in a notebook cell (slides also implement
`_display_()`). Content elements (`banners/content/`) render on their own too.

### Layers

```
banners/
  config.py          # Global mutable state: team, date, template, palette, theme, background, section counter
  palette.py         # Palette: colors by role + 5 presets (ORANGE, BLUE, GREEN, PURPLE, GRAY)
  theme.py           # Theme: fonts, title weight, icon stroke, scale
  background.py      # Background: color / gradient / image + automatic text contrast
  slide.py           # Slide base class: stores the slide data, render() delegates to the template
  template.py        # Template: 16:9 canvas renderer (layouts) + presets (BECH, EXECUTIVE, …)
  icons.py           # Original line icons as SVG data URIs (used by templates)
  slides/            # Cover, Intro, Section, Closing — only their own fields, no rendering
  content/           # Leaf content elements — each has a .render() method
  scenes/            # Reusable Manim Scene factories (e.g. PipelineScene)
  static/            # Vendored mermaid.min.js
test/                # Visual reference notebooks (marimo), one per feature
example/             # Demo decks (showcase, ondas_electromagneticas)
example/layouts/     # marimo slide-layout files (*.slides.json)
```

### `Slide` base class (`slide.py`)

A slide only stores data (`title`, `subtitle`, `content`, `palette`, `footer`,
`background` plus each subclass's fields). `Slide.render()` returns
`(configure template or Template()).render(self)`; there is no other rendering
path. `Slide._icon_src()` converts paths, URLs and bytes to data URIs for the
template and for `Background.image`.

### Templates (`template.py`)

`Template` = layouts + logos/photos/icons/bar options + one `Palette` + one
`Theme`. `Template.render(slide)` calls `_resolve_style()` to pick the palette
(slide `palette=` > `configure(palette=)` > `template.palette`) and the theme
(`configure(theme=)` > `template.theme`); a user palette or theme replaces the
template's one as a whole, fields are never merged. It then draws the layout on
`replace(self, palette=..., theme=...)`, so layouts read only `self.palette.*`
and `self.theme.*`. A slide `background` paints the canvas and, when
`Background.text_color()` returns a color, sets `text`/`muted`/`on_dark` to it.

The canvas is `container-type:inline-size` + `aspect-ratio:16/9`, with absolutely
positioned boxes in % of the slide and font sizes in `cqw` (`SIZES`, taken from
PowerPoint point sizes, times `Theme.scale`). Layout is chosen by slide type and
content (see the module docstring). Never size slide text in `rem` or `px`.
Never commit organization brand assets (logos, photos) to this public repo.
Preset photos must be public domain, contain no people, and be linked
(Wikimedia Commons `Special:FilePath` URLs), never stored in the repo.

### Global config (`config.py`)

`configure()` writes only the arguments passed (uses an `_UNSET` sentinel) to a
module-level `_state` dict and always resets the `Section` auto-counter to 0.
`Section.__init__` calls `_cfg._next_section_number()` (returns `"01"`, `"02"`, …),
so **cell order matters** — sections number themselves at construction time.

Because `_state` is module-global, tests must reset it between cases
(call `configure()` with explicit values or restore a snapshot of `_state` in a fixture).

### Palette and Theme (`palette.py`, `theme.py`)

`Palette` holds only colors, by role (`primary`, `secondary`, `dark`,
`closing_bg`, `light`, `text`, `muted`, `on_dark`, `panel`, optional
`icon_color`, `section_colors`, `bar_colors`). `ORANGE = Palette()` is the
default. `Theme` holds `font`, `heading_font`, `title_weight`, `icon_stroke` and
`scale`. Both are plain dataclasses with no dependency on templates or slides.

### Backgrounds (`background.py`)

`Background.color()`, `Background.gradient()`, `Background.image(src, overlay=...)`
produce a `Background(css=...)`. Set globally via `configure(background=...)` or per slide;
the template paints it on the slide canvas.
`text_color()` parses the first color in the CSS (`_parse_first_color`: named colors,
`#rrggbbaa`, `#rrggbb`, `#rgba`, …), computes WCAG relative luminance and returns
`"#ffffff"` (dark bg, luminance < 0.2) or `"#1f2937"` (light bg), or `None` if unparseable.

---

## Content elements

All content elements live in `banners/content/`. Each class must expose a `.render()` method that returns a marimo component. The `Slide._render_item()` method calls it automatically.

| Class | Notes |
|-------|-------|
| `Text(body)` | Wraps a markdown string (LaTeX supported). |
| `Image(src, width)` | Accepts path, bytes, or URL. `_icon_src()` in `slide.py` handles conversion. |
| `Graph(diagram)` | Static Mermaid via `mo.mermaid()`. |
| `AnimatedGraph(diagram)` | Interactive: Python Mermaid parser → SVG → anywidget. Click toggles node highlight. |
| `Table(df)` | Wraps a pandas DataFrame. |
| `Plot(fig)` | Auto-detects matplotlib vs plotly. |
| `Manim(scene, format, quality, interactive)` | Renders a Manim `Scene` subclass. Results cached after first render. |
| `FlowAnimation(nodes, quality)` | Delegates entirely to `Manim(interactive=True)`. Builds a `_FlowScene` dynamically. |

### `AnimatedGraph` internals

Uses a custom pipeline instead of mermaid.js to avoid marimo's shadow DOM (which blocks `<script>` execution from `mo.Html`):
1. `_parse()` — regex-based Mermaid `graph LR/TD` parser → tuple `(nodes, edges, direction)`:
   `nodes` is `{id: label}`, `edges` is `[(src, dst, edge_label)]`
2. `_layout()` — BFS level assignment with `max_level = len(nodes)` cycle guard → tuple `(pos, node_w, node_h)`,
   where `pos` is `{id: (x, y)}`
3. `_build_svg()` — generates SVG with `.ag-node` class on each node group
4. `_GraphWidget(anywidget.AnyWidget)` — `_esm` JS attaches click listeners that toggle fill color

These pure functions (`_parse`, `_layout`, `_build_svg`) are the main target for unit tests.

### `Manim` + `FlowAnimation` internals

**Static mode** (`interactive=False`): renders in a `tempfile.TemporaryDirectory` with `manim.tempconfig`, returns `mo.image` or `mo.video`.

**Interactive mode** (`interactive=True`): renders with `save_sections=True`. Each `self.next_section("name")` in the scene produces a separate `.mp4`. All sections are base64-encoded and passed to `_ManimInteractiveWidget` (anywidget) as a `srcs` list.

`_ManimInteractiveWidget._esm` implements a **double-buffer video player**:
- `buf[0]` = front (z=1, visible), `buf[1]` = back (z=0, preloading)
- `whenReady(video, cb)` — race-free helper: registers `canplay` listener first, then checks `readyState >= 3`. Uses a `done` flag to prevent double-firing.
- On click: loads next src into `buf[1]`, waits for `whenReady`, swaps z-indices, calls `buf.reverse()` to rotate roles.
- At the last frame, clicking restarts from `srcs[0]`.

`FlowAnimation._build_scene()` constructs a `_FlowScene(Scene)` class dynamically inside the method, using closures to capture `nodes`/`colors`/sizing. It uses `self.next_section(f"step_{i}")` per node and passes the class to `Manim`.

**Critical constraint**: `mo.Html()` uses `innerHTML` — `<script>` tags do NOT execute. All interactive widgets must use `anywidget.AnyWidget` with `_esm`.

### `PipelineScene` (`banners/scenes/pipeline.py`)

A factory function (not a class) that imports manim lazily and returns a `_PipelineScene` class. Called as `Manim(PipelineScene, interactive=True)`. Defines 6 sections: raw → validate → branches → join → load → status.

**Manim name conflicts in marimo**: when defining a Manim scene inside a marimo cell, import manim symbols with aliases to avoid conflicts with banners exports: `from manim import Text as MText, WHITE as MW, GRAY as MG`, etc.

---

## Adding a new content element

1. Create `banners/content/<name>.py` with a class that has a `.render()` method.
2. Export it from `banners/content/__init__.py`.
3. Export it from `banners/__init__.py` (`__all__`).
4. If it needs interactive JS, use `anywidget.AnyWidget` with `_esm` — never `mo.Html()` with `<script>`.
5. Add a visual notebook `test/NN_<name>.py` and unit tests in `tests/`.

## Adding a new scene

Add a factory function to `banners/scenes/` that lazily imports manim and returns a `Scene` subclass. Export from `banners/scenes/__init__.py`. Use `self.next_section("name")` for click-advance steps.

## Conventions

- Python ≥ 3.11. Use `uv` for everything (`uv run`, `uv pip`, `uv build`).
- Everything in the repository is written in English: code, docstrings, comments,
  tests, notebooks, README, `MILESTONES.md`, plans in `plans/`, workflow and config
  comments, commit messages and PR comments. This overrides any personal rule that
  asks for another language.
- Public API changes must update `banners/__init__.py` `__all__`, the README, and docstrings (pdoc builds docs from them, Google style).
- Do not commit rendered media (`*.mp4` is gitignored) or `__marimo__/` folders.
