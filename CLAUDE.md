# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install (always use uv, never pip)
uv pip install -e "."            # core only
uv pip install -e ".[dev]"       # includes manim, pandas, pdoc

# Run the visual demo / reference guide
uv run marimo edit test.py

# Generate docs
uv run pdoc banners -o docs/
```

No test suite exists yet. Visual validation is done via `test.py` in marimo.

---

## Architecture

`banners` is a **marimo presentation library**. Every slide calls `.render()` which returns a `mo.vstack` of marimo components, displayed directly in a notebook cell.

### Layers

```
banners/
  config.py          # Global mutable state: team, date, palette, section counter
  palette.py         # Palette / SectionPalette dataclasses + 5 presets
  slide.py           # Slide base class — layout engine lives here
  slides/            # Cover, Intro, Section, Closing — each overrides _render_banner()
  content/           # Leaf content elements — each has a .render() method
  scenes/            # Reusable Manim Scene factories (e.g. PipelineScene)
```

### `Slide` base class (`slide.py`)

`_render_content()` drives all layout logic:
- **1 item** → rendered at full width.
- **N items** → `_css_grid()` wraps them in an equal `1fr`-per-column grid via inline HTML.
- `content_kind` wraps `Text` items in `mo.callout(kind=...)` when the list is text-only.

`_render_item()` dispatches by type: `Text`/`str` → `mo.md()`; anything with `.render()` → call it; otherwise pass through as-is.

All four slide types inherit `Slide` and only implement `_render_banner()` to return a `mo.Html` banner block.

### Global config (`config.py`)

`configure()` writes to a module-level `_state` dict and resets the `Section` auto-counter to 0. `Section.__init__` calls `_cfg._next_section_number()` to get its auto-number, so **cell order matters** — sections number themselves at construction time.

### Palette system (`palette.py`)

`Palette` is for full-banner slides (Cover/Intro/Closing). It has `start/mid/end` colors and a `gradient` property. `Palette.to_section_palette()` derives a `SectionPalette` (border + dark bg) by darkening `start`. Predefined constants: `ORANGE`, `BLUE`, `GREEN`, `PURPLE`, `GRAY`.

---

## Content elements

All content elements live in `banners/content/`. Each class must expose a `.render()` method that returns a marimo component. The `Slide._render_item()` method calls it automatically.

| Class | Notes |
|-------|-------|
| `Text(body)` | Wraps a markdown string. |
| `Image(src, width)` | Accepts path, bytes, or URL. `_icon_src()` in `slide.py` handles conversion. |
| `Graph(diagram)` | Static Mermaid via `mo.mermaid()`. |
| `AnimatedGraph(diagram)` | Interactive: Python Mermaid parser → SVG → anywidget. Click toggles node highlight. |
| `Table(df)` | Wraps a pandas DataFrame. |
| `Plot(fig)` | Auto-detects matplotlib vs plotly. |
| `Manim(scene, format, quality, interactive)` | Renders a Manim `Scene` subclass. Results cached after first render. |
| `FlowAnimation(nodes, quality)` | Delegates entirely to `Manim(interactive=True)`. Builds a `_FlowScene` dynamically. |

### `AnimatedGraph` internals

Uses a custom pipeline instead of mermaid.js to avoid marimo's shadow DOM (which blocks `<script>` execution from `mo.Html`):
1. `_parse()` — regex-based Mermaid `graph LR/TD` parser → `{nodes, edges, direction}`
2. `_layout()` — BFS level assignment with `max_level = len(nodes)` cycle guard → `{node: (x,y)}`
3. `_build_svg()` — generates SVG with `.ag-node` class on each node group
4. `_GraphWidget(anywidget.AnyWidget)` — `_esm` JS attaches click listeners that toggle fill color

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

## Adding a new scene

Add a factory function to `banners/scenes/` that lazily imports manim and returns a `Scene` subclass. Export from `banners/scenes/__init__.py`. Use `self.next_section("name")` for click-advance steps.
