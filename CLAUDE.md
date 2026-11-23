# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Working by milestones

Work is planned in `MILESTONES.md`. When asked to "take the next milestone":

1. Read `MILESTONES.md` and pick the **first** milestone whose status is `[ ]`.
2. Work on a branch named `milestone/<id>-<slug>` (e.g. `milestone/m2-unit-tests`).
3. Implement only that milestone. If you find unrelated issues, add them to the
   **Backlog** section of `MILESTONES.md` instead of fixing them.
4. A milestone is done only when **every** acceptance criterion passes. Run the
   verification commands listed in it and paste their result in the commit message body.
5. Mark it `[x]`, add a one-line entry to the **Log** section (date, branch, summary),
   commit, and stop. Do not start the next milestone in the same session.
6. If a criterion cannot be met, mark the milestone `[!]`, write why under it, and stop.

## Commands

```bash
# Install (always use uv, never pip)
uv pip install -e "."            # core only
uv pip install -e ".[manim]"     # + manim (needs system libs, see README)
uv pip install -e ".[dev]"       # dev tools: hatch, pdoc, pandas, manim

# Visual reference notebooks (one per feature)
uv run marimo edit test/01_intro.py        # ... through test/10_background.py
uv run marimo edit example/showcase.py     # full demo deck

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
Every slide calls `.render()` which returns a `mo.vstack` of marimo components,
displayed directly in a notebook cell (slides also implement `_display_()`).

### Layers

```
banners/
  config.py          # Global mutable state: team, date, icon, palette, background, section counter
  palette.py         # Palette / SectionPalette dataclasses + 5 presets
  background.py      # Background: color / gradient / image + automatic text contrast
  slide.py           # Slide base class — layout engine lives here
  template.py        # Template: fixed 16:9 canvas renderer (corporate PowerPoint style)
  slides/            # Cover, Intro, Section, Closing — each overrides _render_banner()
  content/           # Leaf content elements — each has a .render() method
  scenes/            # Reusable Manim Scene factories (e.g. PipelineScene)
  static/            # Vendored mermaid.min.js
test/                # Visual reference notebooks (marimo), one per feature
example/             # Demo decks (showcase, ondas_electromagneticas)
example/layouts/     # marimo slide-layout files (*.slides.json)
```

### `Slide` base class (`slide.py`)

`_render_content()` drives all layout logic:
- **1 item** → rendered at full width.
- **N items** → `_css_grid()` wraps them in an equal `1fr`-per-column grid via inline HTML.
- `content_kind` wraps `Text` items in `mo.callout(kind=...)` when the list is text-only.

`_render_item()` dispatches by type: `Text`/`str` → `mo.md()`; anything with `.render()` → call it; otherwise pass through as-is.

All four slide types inherit `Slide` and only implement `_render_banner()` to return a `mo.Html` banner block.

### Templates (`template.py`)

When `configure(template=Template(...))` is set, every slide's `render()` returns
`template.render(self)` instead of the editorial layout. The template draws a
16:9 canvas (`container-type:inline-size` + `aspect-ratio:16/9`) with absolutely
positioned boxes in % of the slide and font sizes in `cqw` (`SIZES`, taken from
PowerPoint point sizes). Layout is chosen by slide type and content (see the
module docstring). `Cover.image` and `Section.image` are only used by templates.
Never commit organization brand assets (logos, photos) to this public repo.

### Global config (`config.py`)

`configure()` writes only the arguments passed (uses an `_UNSET` sentinel) to a
module-level `_state` dict and always resets the `Section` auto-counter to 0.
`Section.__init__` calls `_cfg._next_section_number()` (returns `"01"`, `"02"`, …),
so **cell order matters** — sections number themselves at construction time.

Because `_state` is module-global, tests must reset it between cases
(call `configure()` with explicit values or restore a snapshot of `_state` in a fixture).

### Palette system (`palette.py`)

`Palette` is for full-banner slides (Cover/Intro/Closing). It has `start/mid/end` colors and a `gradient` property. `Palette.to_section_palette()` derives a `SectionPalette` (border + dark bg) by darkening `start`. Predefined constants: `ORANGE`, `BLUE`, `GREEN`, `PURPLE`, `GRAY`.

### Backgrounds (`background.py`)

`Background.color()`, `Background.gradient()`, `Background.image(src, overlay=...)`
produce a `Background(css=...)`. Set globally via `configure(background=...)` or per slide.
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

- Python ≥ 3.10. Use `uv` for everything (`uv run`, `uv pip`, `uv build`).
- Public API changes must update `banners/__init__.py` `__all__`, the README, and docstrings (pdoc builds docs from them, Google style).
- Do not commit rendered media (`*.mp4` is gitignored) or `__marimo__/` folders.
