# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo>=0.23.2",
# ]
# ///
"""
01_intro.py — Introduction to banners: slides, configuration and palettes.
Run with: uv run marimo edit test/01_intro.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text
    from banners.palette import Palette, ORANGE, BLUE, GREEN, PURPLE, GRAY
    return Closing, Cover, BLUE, GREEN, GRAY, Intro, ORANGE, Palette, PURPLE, Section, Text, configure, mo


@app.cell
def _(mo):
    mo.md(r"""
    # banners — Introduction

    **banners** is a marimo presentation library. Each slide calls `.render()`
    which returns a marimo component displayed directly in the notebook cell.

    ---

    ## Install

    ```bash
    uv pip install -e "."          # core
    uv pip install -e ".[dev]"     # includes manim, pandas, pdoc
    ```

    ---

    ## Slide types

    | Class | Purpose | Position |
    |-------|---------|----------|
    | `Cover` | Large centered banner | First slide |
    | `Intro` | Compact gradient banner | Context / problem statement |
    | `Section` | Dark panel with left border | Middle slides |
    | `Closing` | Large centered banner + metrics | Last slide |

    All slides inherit `team`, `date`, and `palette` from `configure()`.

    ---

    ## `configure()` — global setup

    Call once at the top of the notebook. Resets the `Section` auto-counter to 0.

    ```python
    configure(
        team="Analytics Team",
        date="April 2026",
        palette=BLUE,
        icon={"src": "img/logo.png"},  # optional
    )
    ```

    | Parameter | Used by | Description |
    |-----------|---------|-------------|
    | `team`    | Cover, Intro, Closing | Label in the banner |
    | `date`    | Cover | Date line at the bottom |
    | `palette` | All slides | Color palette |
    | `icon`    | All slides | Logo placed on the banner |
    """)
    return


@app.cell
def _(BLUE, configure):
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return


@app.cell
def _(mo):
    mo.md("## Cover")
    return


@app.cell
def _(Cover, Text):
    Cover(
        title="My Project",
        subtitle="Short phrase framing the context.",
        content=[
            Text("**Key point 1** — Something relevant to the audience."),
            Text("**Key point 2** — The concrete result achieved."),
            Text("**Key point 3** — The impact for the team."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Cover parameters

    | Parameter | Type | Description |
    |-----------|------|-------------|
    | `title` | `str` | Large centered title |
    | `subtitle` | `str` | Smaller line below the title |
    | `content` | list of `Text` | Bullet points in a grid below the banner |
    | `content_kind` | `str` | Box style: `"neutral"`, `"info"`, `"warn"`, `"danger"`, `"success"` |
    | `palette` | `Palette` | Override the global palette |
    | `icon` | `dict` | `{"src": path}` logo on the banner |
    | `footer` | `str` | Quote rendered as a blockquote below content |
    """)
    return


@app.cell
def _(mo):
    mo.md("## Intro")
    return


@app.cell
def _(Intro, Text):
    Intro(
        title="The context: why we're here",
        subtitle="What motivated this work and what was at stake.",
        tag="Context",
        summary="Models were running on servers with a confirmed shutdown date.",
        content=[
            Text("**Operational risk** — Models would stop producing predictions."),
            Text("**No traceability** — No record of which version was active."),
            Text("**People dependency** — Manual and undocumented process."),
        ],
        content_kind="warn",
        footer="The question wasn't whether to migrate — but how to do it sustainably.",
    ).render()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Intro exclusive parameters

    | Parameter | Description |
    |-----------|-------------|
    | `tag` | Small-caps label above the title (e.g. `"Context"`) |
    | `summary` | Full-width highlighted block between banner and content |
    | `footer` | Blockquote at the bottom |
    """)
    return


@app.cell
def _(mo):
    mo.md("## Section")
    return


@app.cell
def _(Section, Text):
    Section(
        title="What was built",
        subtitle="Three decisions that define the result.",
        content=[
            Text("**Decision 1** — Parameterized infrastructure for any model."),
            Text("**Decision 2** — Deploy with a single command."),
            Text("**Decision 3** — Automatically generated technical documentation."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Section exclusive parameters

    | Parameter | Description |
    |-----------|-------------|
    | `number` | Large number on the left. Auto-assigned if omitted. Override with `number="05"` or suppress with `number=" "` |
    | `footer` | Blockquote at the bottom |

    Sections **auto-number** starting from `01`. The counter resets each time
    `configure()` is called. Cell order matters — sections number themselves at
    construction time.
    """)
    return


@app.cell
def _(mo):
    mo.md("## Closing")
    return


@app.cell
def _(Closing):
    Closing(
        title="One framework for all models.",
        subtitle="Infrastructure is solved. The team focuses only on data science.",
        stats=[
            ("Low",   "Effort per new model",  "Just configure data"),
            ("↑ ROI", "Cumulative return",      "Each migration amortizes more"),
            ("100%",  "Traceability",           "Automatic end-to-end tracking"),
            ("1",     "Shared codebase",        "Everyone contributes to the same repo"),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Closing exclusive parameter

    | Parameter | Type | Description |
    |-----------|------|-------------|
    | `stats` | list of `(value, label, caption)` | Metric cards rendered in a row |

    ---

    ## `footer` — available on all slides

    Every slide type accepts a `footer` parameter.
    It renders as a blockquote below the content area.
    """)
    return


@app.cell
def _(Section, Text):
    Section(
        title="Key findings",
        content=Text("The migration reduced deployment time from days to minutes."),
        footer="All environments validated end-to-end before going live.",
    ).render()
    return


@app.cell
def _(mo):
    mo.md(r"""
    ---

    ## Palette system

    `Palette` defines a three-stop gradient used by Cover, Intro, and Closing.
    `Section` automatically derives its border and dark background from the same palette.

    ### Predefined palettes

    | Constant | Gradient |
    |----------|----------|
    | `ORANGE` (default) | `#7c2d12 → #c2410c → #ea580c` |
    | `BLUE`   | `#1e3a5f → #1d4ed8 → #3b82f6` |
    | `GREEN`  | `#14532d → #15803d → #22c55e` |
    | `PURPLE` | `#3b0764 → #7e22ce → #a855f7` |
    | `GRAY`   | `#111827 → #374151 → #6b7280` |

    ### Custom palette

    ```python
    teal = Palette(start="#042f2e", mid="#0f766e", end="#2dd4bf")
    configure(palette=teal)
    ```

    `Section` derives:
    - **border** → `end` color
    - **background** → darkened `start`
    """)
    return


@app.cell
def _(Cover, GRAY, Text, configure):
    configure(palette=GRAY, team="Analytics Team", date="April 2026")
    Cover(
        title="Gray palette",
        subtitle="Set via configure(palette=GRAY).",
        content=[
            Text("**Cover** — inherits palette globally."),
            Text("**Section** — border and background derived automatically."),
            Text("**Closing** — same gradient, no extra work."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(Cover, Palette, Section, Text, configure):
    teal = Palette(start="#042f2e", mid="#0f766e", end="#2dd4bf")
    configure(palette=teal, team="Analytics Team", date="April 2026")
    Cover(
        title="Custom teal palette",
        subtitle="Palette(start, mid, end) passed to configure().",
        content=[
            Text("**start** — darkest stop (left side of gradient)."),
            Text("**mid** — center stop."),
            Text("**end** — brightest stop, used as Section border accent."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="Section with teal palette",
        subtitle="Border and background derived automatically from the custom palette.",
        content=Text("""
The border takes the `end` color and the background is a darkened
version of `start` — consistent with the overall scheme without any
extra configuration.
"""),
    ).render()
    return


if __name__ == "__main__":
    app.run()
