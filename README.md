# marimo-banners

[![CI](https://github.com/kascesar/banners/actions/workflows/ci.yml/badge.svg)](https://github.com/kascesar/banners/actions/workflows/ci.yml)

Composable slide presentations inside [marimo](https://marimo.io) notebooks.

Each slide is a Python object drawn on a fixed 16:9 canvas, like a PowerPoint
slide. Positions and font sizes are relative to the slide width, so a deck keeps
its proportions and stays legible from a notebook cell to a full-screen projector.
How the slides look comes from a `Template`, made of layouts, a `Palette`
(colors) and a `Theme` (fonts, title weight, icon stroke, scale).

> **Personal note:** This project is a personal initiative to explore the capabilities of generative AI for developing complete, production-quality software projects — from architecture decisions to implementation, testing, and documentation — using [Claude Code](https://claude.ai/code) as the primary development partner.

---

## 01 · Slide types & palettes

![Slide types and palettes demo](demo-1-slide-types.gif)

Four slide types (`Cover`, `Intro`, `Section`, `Closing`) with five built-in palettes (`ORANGE`, `BLUE`, `GREEN`, `PURPLE`, `GRAY`) and full custom palette support.

---

## 02 · Content types

![Content types demo](demo-2-content-types.gif)

> The animations on this page were recorded with version 0.2 and still show the previous style.

`Text` (markdown + LaTeX), `Image`, `Graph` (Mermaid), `AnimatedGraph` (interactive), `Table`, `Plot` (matplotlib / plotly), `FlowAnimation`, and `Manim` — all composable inside any slide.

---

## 03 · Slide backgrounds

![Slide backgrounds demo](demo-3-backgrounds.gif)

`Background.color()`, `Background.gradient()`, and `Background.image()` — apply to any slide. Dark overlays and text contrast are handled automatically.

---

# Upgrading to 0.6

Version 0.6 requires Python 3.11 or newer, so it can use manim 0.21 or newer
(faster rendering). Projects that stay on Python 3.10 keep version 0.5.1.

# Upgrading to 0.5

Version 0.5 has a single rendering model: every slide is drawn on the 16:9
canvas of a `Template`, and the fluid editorial style of 0.3 and 0.4 is gone.
Decks that only use titles, content and the predefined palettes run unchanged
and look different. These parameters were removed and now raise an error:

| Removed | Replacement |
|---------|-------------|
| `content_kind=` on slides | None: text renders as body text. |
| `icon=` on slides and in `configure()` | `Template(mark=...)` for the small corner mark, `logo_on_light`/`logo_on_dark` for logos. |
| `Palette(start=..., mid=..., end=...)`, `Palette.gradient`, `text_*` | `Palette(primary=..., dark=..., closing_bg=...)`: the old `end`, `start` and `mid`. |
| `SectionPalette`, `Palette.to_section_palette()` | `Palette`, for every slide type. |
| `Template(primary=..., font=..., ...)` color and font fields | `Template(palette=Palette(...), theme=Theme(...))`. |
| `configure(template=None)` for the editorial style | `configure(template=None)` now uses the default `Template()`. |

---

# Installation

banners needs Python 3.11 or newer.

```bash
uv pip install marimo-banners
```

For animated diagrams (`FlowAnimation`, `Manim`):

```bash
uv pip install "marimo-banners[manim]"
```

`FlowAnimation` and `Manim` depend on system libraries for rendering. Install the appropriate set for your OS:

**Ubuntu / Debian**
```bash
sudo apt install python3-dev libpango1.0-dev pkg-config libcairo2-dev libx11-dev libgl1-mesa-dev ffmpeg
```

**Fedora / RHEL**
```bash
sudo dnf install gcc-c++ python3-devel pkgconf-pkg-config cairo-devel pango-devel libX11-devel mesa-libGL-devel ffmpeg
```

# Quick start

```python
from banners import BLUE, TERRA, Closing, Cover, Intro, Section, Text, configure

# Set shared values once; every slide picks them up.
configure(template=TERRA, palette=BLUE, team="Analytics Team", date="April 2026")

Cover(title="Churn Prediction v2", subtitle="Model migration and deployment.")
Intro(title="Why", content=[Text("**Risk** — No fallback."), Text("**Cost** — Manual steps.")])
Section(title="Results", content=[Text("**Accuracy** — 91% AUC."), Text("**Latency** — p99 under 30 ms.")])
Closing(title="One framework for all models.")
```

# Global configuration

`configure()` sets values shared across all slides. Call it once at the top of
the notebook; it only changes the arguments it receives.

| Parameter | Description |
|-----------|-------------|
| `template` | `Template` that draws every slide. `None` uses the default `Template()`. |
| `palette` | `Palette` for every slide; replaces the template's palette. |
| `theme` | `Theme` for every slide; replaces the template's theme. |
| `background` | `Background` painted on every slide's canvas. |
| `team` | Team line on `Cover`, `Intro` and `Closing`. |
| `date` | Date on `Cover`. |

Calling `configure()` also resets the `Section` auto-number counter to zero.

# Slides

| Class | Purpose | Typical position |
|-------|---------|-----------------|
| `Cover` | Dark cover with logo, or photo cover (`image=`) | First slide |
| `Intro` | Large title on the left, content on the right | Slides 2–3 |
| `Section` | Divider without content; content slide otherwise | Middle slides |
| `Closing` | Closing message with an optional metrics row (`stats=`) | Last slide |

All slides share these parameters:

| Parameter | Description |
|-----------|-------------|
| `title` | Main heading |
| `subtitle` | Support phrase shown under the title |
| `content` | Content element(s) of the slide |
| `palette` | Colors for this slide only; replaces the configured and the template palette |
| `footer` | Short note (source, closing remark) at the bottom right |
| `background` | Background of this slide's canvas (see [Slide backgrounds](#slide-backgrounds)) |

## Section — auto-numbering

`Section` slides assign their number automatically, starting from `01` and incrementing with each new instance. The counter resets when `configure()` is called.

```python
configure(team="My Team")    # counter resets to 0

Section(title="Context")     # number = "01"
Section(title="Results")     # number = "02"
Section(title="Conclusions") # number = "03"

# Override:
Section(title="Appendix", number="A1")

# Suppress:
Section(title="No number", number="")
```

# Content elements

| Class | Renders |
|-------|---------|
| `Text(body)` | Markdown — paragraphs, lists, tables, LaTeX |
| `Image(src)` | Image from file path, bytes, or URL |
| `Graph(code)` | Static Mermaid diagram |
| `AnimatedGraph(code)` | Interactive Mermaid diagram — click to highlight nodes |
| `Table(df)` | pandas DataFrame |
| `Plot(fig)` | matplotlib or plotly figure (auto-detected) |
| `FlowAnimation(...)` | Click-to-advance animated pipeline diagram |
| `Manim(scene)` | Custom Manim `Scene` subclass (static or interactive) |

Content is passed to the `content` parameter of any slide. Layout is resolved automatically:

- **Single item** → full width.
- **Several items** → equal columns, one per item.
- **A visual first, then text** (`Section(content=[Plot(fig), Text(...)])`) → visual on the left, title and text on the right.

Content elements also work on their own in any marimo cell, without slides or `configure()`.

## AnimatedGraph

Accepts `graph LR` / `graph TD` Mermaid syntax. Clicking a node toggles a highlight color.

```python
from banners.content import AnimatedGraph

AnimatedGraph("""
graph LR
    A[Ingest] --> B[Validate]
    B --> C[Transform]
    C --> D[Load]
""", highlight_color="#3b82f6")
```

## FlowAnimation

Step-by-step pipeline animation. Each node appears on click with a short
0.25 s fade-in, and the diagram stays on screen between clicks. On a slide the
animation takes the slide palette: the background is `palette.panel`, nodes use
`section_colors` (or `primary` and `secondary`), and names and arrows use `text`
and `muted`. Standalone, it uses the default `Palette()`, or pass `palette=`.
Requires the `manim` dependency.

```python
from banners.content import FlowAnimation

# Flat list — linear chain
FlowAnimation(["S3", "Glue", "Athena"])

# Nested list — layered topology
FlowAnimation([
    ["Ingest"],
    [{"name": "Transform A", "detail": "features"},
     {"name": "Transform B", "detail": "filters"}],
    ["Load"],
])

# Explicit graph — arbitrary connections
FlowAnimation(
    nodes=["Ingest A", "Ingest B", "Validate", "Train"],
    edges=[
        ("Ingest A", "Validate"),
        ("Ingest B", "Validate"),
        ("Validate", "Train"),
    ],
)
```

| Parameter | Default | Description |
|-----------|---------|-------------|
| `direction` | `"LR"` / `"TD"` | Flow direction — left-right or top-down |
| `quality` | `"low"` | Render quality: `"low"`, `"medium"`, `"high"` |
| `width` | `"100%"` | Player width — any CSS value |

Default direction: `"LR"` for flat lists and graphs, `"TD"` for nested lists.

## Manim

Embed any Manim `Scene` subclass — static GIF/PNG/MP4 or click-to-advance interactive mode.

```python
from manim import Scene, MathTex, Write
from banners.content import Manim

class MyScene(Scene):
    def construct(self):
        self.next_section("eq1")
        self.play(Write(MathTex(r"E = mc^2", font_size=72)))
        self.wait(1)
        self.next_section("eq2")
        self.play(Write(MathTex(r"\nabla^2 E = \frac{1}{c^2}\ddot{E}", font_size=52)))
        self.wait(1)

Section(
    title="Derivation",
    content=[Manim(MyScene, interactive=True, quality="medium")],
).render()
```

On a slide, banners paints the scene background with `palette.panel` and the
player controls with the palette, so the animation blends into the slide; a
scene that sets `self.camera.background_color` keeps its own color. Every
render runs at 30 frames per second.

`banners.scenes.PipelineScene` is a ready-made data-pipeline scene that follows
the palette: `Manim(PipelineScene, interactive=True)`.

Renders are cached on disk (`~/.cache/banners/manim/`) keyed by scene source code
and palette — no re-rendering across notebook restarts.

# Palettes and themes

A `Palette` holds the colors of a deck, named by the role they play:

| Field | Role |
|-------|------|
| `primary` | Titles and main segment of the bottom bar |
| `secondary` | End segment of the bottom bar |
| `dark` | Background of the dark cover |
| `closing_bg` | Background of the closing slide |
| `light` | Background of dividers and content slides |
| `text`, `muted` | Body text and labels on light backgrounds |
| `on_dark` | Text on dark backgrounds |
| `panel` | Box behind charts and visuals |
| `icon_color`, `section_colors`, `bar_colors` | Optional: icon color, one color per section, multi-color bar |

| Constant | `primary` | `dark` | `closing_bg` |
|----------|-----------|--------|--------------|
| `ORANGE` (default) | `#e4572e` | `#404040` | `#363e45` |
| `BLUE` | `#2f6fd0` | `#0f2340` | `#16325c` |
| `GREEN` | `#2e8b57` | `#0f2a1f` | `#173d2d` |
| `PURPLE` | `#6e56cf` | `#221a3a` | `#2e2450` |
| `GRAY` | `#5b6470` | `#1a1d21` | `#2a2e34` |

A `Theme` holds the rest of the style: `font`, `heading_font` (titles; `None`
uses `font`), `title_weight`, `icon_stroke` (line icons) and `scale` (multiplies
every font size).

Each template has its own palette and theme (`TERRA.palette`, `TERRA.theme`).
A palette or theme you declare replaces the template's one as a whole:

```python
from banners import BLUE, TERRA, Palette, Section, Theme, configure

configure(template=TERRA)                                  # TERRA colors and fonts
configure(template=TERRA, palette=BLUE)                    # TERRA layouts and fonts, BLUE colors
configure(theme=Theme(font="Inter, sans-serif", scale=1.1))
Section(title="Risks", palette=Palette(primary="#b42318"))  # this slide only
```

Precedence: palette — slide `palette=` > `configure(palette=...)` > template;
theme — `configure(theme=...)` > template.

# Slide backgrounds

The `background` parameter paints the canvas of a slide instead of the layout
color. When the text color that reads well on the background can be computed,
the slide text uses it.

```python
from banners import Background

# Solid color
Cover(title="Dark slide", background=Background.color("#0f172a"))

# Custom gradient
Section(title="Gradient", background=Background.gradient("#0d1b2a", "#4a1a6e"))
Section(title="3-stop",   background=Background.gradient("#0d1b2a", "#4a1a6e",
                                                        mid="#1a2a5e", angle=45))

# Image — dark overlay applied automatically for legibility
Cover(title="Photo", background=Background.image("assets/photo.jpg"))
Cover(title="URL",   background=Background.image("https://...", overlay="rgba(0,0,0,0.7)"))
Cover(title="Raw",   background=Background.image(raw_bytes, overlay=None))
```

# Templates (fixed 16:9 slides)

A `Template` draws every slide on the 16:9 canvas, like a corporate PowerPoint
master: positions and font sizes are relative to the slide width (`cqw` units).
Without `configure(template=...)` a default `Template()` is used. Define your
own to reproduce your organization's template while keeping every banners
feature (Mermaid, plots, tables, Manim).

```python
from banners import Palette, Template, Theme, configure
from banners.content import Plot, Text
from banners.slides import Closing, Cover, Intro, Section

corp = Template(
    palette=Palette(primary="#ff6600", secondary="#054af6"),  # titles + bottom bar
    theme=Theme(font="'Century Gothic', 'URW Gothic', sans-serif"),
    logo_on_dark="assets/logo_white.png",
    logo_on_light="assets/logo_color.png",
    mark="assets/isotype.png",           # small mark on content slides
    closing_image="assets/mascot.png",   # picture next to the closing title
)
configure(template=corp, team="Analytics", date="November 2026")

Cover(title="Churn v2", subtitle="Model migration")                  # dark cover
Cover(title="Churn v2", image="assets/photo.jpg")                    # photo cover
Section(title="Context", image="assets/photo2.jpg")                  # divider with photo
Intro(title="Problem", content=[Text("..."), Text("...")])            # big title + columns
Section(title="Results", content=[Plot(fig), Text("- ...")])          # visual + text
Section(title="Impact", image="assets/photo3.jpg", content=Text(".."))  # photo + text
Closing(title="Thanks")                                               # closing
```

| Slide | Layout |
|-------|--------|
| `Cover()` / `Cover(image=...)` | Dark cover with logo, or photo cover with the title over the picture. |
| `Section()` without content | Divider; with `image=`, the photo fills the right half. |
| `Section(content=[visual, Text])` | Visual on the left, title and text on the right. |
| `Section(content=..., image=...)` | Photo on the left half, title and content on the right. |
| `Section(content=...)` | Title on top, content in columns. |
| `Intro()` | Large title in the left column, content in columns on the right. |
| `Closing()` | Closing slide; `title=""` shows the centered logo. |

Image fields accept a URL (loaded by the browser, nothing is embedded), a
path, or bytes. When `logo_on_dark` is not set, dark slides show
`logo_on_light` in white with the `mark` kept in color.

A preset inspired by BancoEstado's decks is included. It is not an official
BancoEstado template; its logos are linked from Wikimedia Commons and it ships
no photos:

```python
from banners import BECH
configure(template=BECH, team="Advanced Analytics", date="November 2026")
```

## Built-in templates

```python
from banners import EXECUTIVE, INSTITUTIONAL, COSMOS, VIBRANT, TERRA, PRESETS
configure(template=COSMOS)
```

| Template | Style | Photos |
|----------|-------|--------|
| `EXECUTIVE` | Sober, graphite on white, serif titles, monochrome line icons, no bar | — |
| `INSTITUTIONAL` | Formal navy + steel blue, serif titles, monochrome icons | — |
| `COSMOS` | Dark, cyan/violet/pink, section colors | NASA, public domain: Hubble *Pillars of Creation* (cover), Apollo 17 *Earth* (dividers) |
| `VIBRANT` | White, four-color bar, colored icons, one color per section | — |
| `TERRA` | Earthy greens and terracotta, serif titles | U.S. National Park Service, public domain: Grand Canyon (cover) |
| `BECH` | BancoEstado deck | — (logos from Wikimedia Commons) |

Photos are linked from Wikimedia Commons and loaded by the browser; none are
stored in the repository. They contain no people. NPS photos must not be used
to imply endorsement by the National Park Service.

Icons come from `banners.icons` (original line icons, inline SVG, no network):
`Template(mark="chart", divider_icon="layers")`. Customize any preset with
`dataclasses.replace(COSMOS, cover_image="my_photo.jpg")`. A single slide
drops the preset photo with `image=False`, for example `Section(title="Agenda", image=False)`.

Other template options: `cover_image`, `divider_image`, `divider_icon`, `bar`,
`bar_split`, and `auto_contrast` (titles below a 3:1 contrast ratio fall back to
a readable color; off in `BECH` to keep the brand orange).

Keep brand assets (logos, photos) out of public repositories: define your
`Template` in a private module next to your notebooks.
`Template(theme=Theme(scale=1.1))` enlarges every font.

# Documentation

```bash
make docs
```

Generated HTML is written to `docs/`.

# Examples

| Notebook | Content |
|----------|---------|
| `example/showcase.py` | Walkthrough of slide types, content elements, and backgrounds |
| `example/ondas_electromagneticas.py` | Complete presentation: Maxwell's equations → animated derivation → wave solution |

Run any example with:

```bash
uv run marimo edit example/showcase.py
```
