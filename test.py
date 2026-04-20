"""
test.py — Guía de referencia y demo visual del sistema de slides.
Correr con: uv run marimo edit test.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text, Image, Graph
    from banners.palette import Palette, BLUE, GREEN, PURPLE, GRAY

    return BLUE, Closing, Cover, Graph, Image, Intro, Section, Text, mo


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Banners — Reference Guide

    ---

    ## Import

    ```python
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text, Image, Graph
    from banners.palette import Palette, BLUE, GREEN, PURPLE, GRAY
    ```

    ## Slides

    | Class | Purpose | Typical position |
    |-------|---------|-----------------|
    | `Cover` | Large centered banner | First slide |
    | `Intro` | Context or problem statement | Slides 2–3 |
    | `Section` | Intermediate section slide | Middle slides |
    | `Closing` | Closing slide with optional metrics | Last slide |

    ## Content types

    | Class | Renders |
    |-------|---------|
    | `Text(body)` | Markdown — paragraphs, lists, tables |
    | `Image(src, width)` | Image from path, bytes or URL |
    | `Graph(diagram)` | Mermaid diagram |

    ## Automatic layouts

    | Content | Layout |
    |---------|--------|
    | Single item | Full width |
    | List of `Text` only + `content_kind` | Columns with box (`mo.callout`) |
    | List with any `Image` or `Graph` | Automatic CSS grid `1fr` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Cover

    Large centered banner. Use as the **first slide**.

    ```python
    Cover(
        title="My Project",
        subtitle="Short phrase framing the context.",
        date="April 2026",
        content=[
            Text("**Key point 1** — Something relevant to the audience."),
            Text("**Key point 2** — The concrete result achieved."),
            Text("**Key point 3** — The impact for the team."),
        ],
        content_kind="neutral",
    ).render()
    ```
    """)
    return


@app.cell
def _(Cover, Text):
    Cover(
        title="My Project",
        subtitle="Short phrase framing the context.",
        date="April 2026",
        content=[
            Text("**Key point 1** — Something relevant to the audience."),
            Text("**Key point 2** — The concrete result achieved."),
            Text("**Key point 3** — The impact for the team."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Intro

    Compact banner with gradient. For slides that open a thematic block.

    Exclusive parameters:
    - `tag` — Label in small caps above the title (e.g. `"Context"`).
    - `summary` — Full-width highlighted block between the banner and content.
    - `footer` — Quote at the bottom as a blockquote.

    ```python
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
    ```
    """)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section

    Dark background with left color border. For **all middle slides**.

    Exclusive parameters:
    - `number` — Large number on the left (`"01"`, `"02"`, ...).
    - `footer` — Quote at the bottom as a blockquote.

    ### Text columns
    """)
    return


@app.cell
def _(Section, Text):
    Section(
        title="What was built",
        subtitle="Three decisions that define the result.",
        number="03",
        content=[
            Text("**Decision 1** — Parameterized infrastructure for any model."),
            Text("**Decision 2** — Deploy with a single command."),
            Text("**Decision 3** — Automatically generated technical documentation."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Graph (automatic CSS grid)
    """)
    return


@app.cell
def _(Graph, Section):
    Section(
        title="Pipeline flow",
        content=Graph("""
    graph LR
    A[Glue Job] --> B[Athena Table]
    B --> C[SageMaker Pipeline]
    C --> D[Predictions]
    """),
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Image (automatic CSS grid)

    `Image` accepts a file path, bytes, or URL.
    The `width` parameter accepts any CSS value (`"80%"`, `"400px"`, `"100%"`).
    """)
    return


@app.cell
def _(Image, Section):
    Section(
        title="Sample image",
        content=Image("img/test.jpeg", width="60%"),
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Mixing Text and Image (automatic CSS grid)
    """)
    return


@app.cell
def _(Image, Section, Text):
    Section(
        title="Architecture overview",
        content=[
            Text("""
    **System description**

    Each stage runs independently
    with automatic end-to-end traceability.
    """),
            Image("img/test.jpeg", width="50%"),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Two images side by side (automatic CSS grid)
    """)
    return


@app.cell
def _(Image, Section):
    Section(
        title="Before and after",
        content=[
            Image("img/test.jpeg", width="100%"),
            Image("img/test.jpeg", width="100%"),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Mixing Text and Graph (automatic CSS grid)
    """)
    return


@app.cell
def _(Graph, Image, Section, Text):
    Section(
        title="Pipeline evidence",
        content=[
            Text("""
    ## Flow description

    Each stage runs independently
    with automatic end-to-end traceability.
    """),
            Graph("""
    graph TD
    A[Glue Job] --> B[Athena Table]
    B --> C[SageMaker Pipeline]
    C --> D[Predictions S3]
    """),
            Image("img/test.jpeg", width="100%"),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Markdown table in Text
    """)
    return


@app.cell
def _(Image, Section, Text):
    Section(
        title="Before vs after",
        content=[Text("""
    | Before | After |
    |--------|-------|
    | Hardcoded per model  | Parameterized for any model |
    | n models = n projects | n models = 1 framework     |
    """),
        Image("img/test.jpeg", width="100%"),]
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Closing

    Large centered banner, same visual weight as `Cover`.

    Exclusive parameter:
    - `stats` — List of tuples `(value, label, caption)` rendered as metrics.
    """)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Color palettes

    All classes accept `palette`. Default is orange.

    | Constant | Gradient |
    |----------|----------|
    | `ORANGE` (default) | `#7c2d12 → #c2410c → #ea580c` |
    | `BLUE` | `#1e3a5f → #1d4ed8 → #3b82f6` |
    | `GREEN` | `#14532d → #15803d → #22c55e` |
    | `PURPLE` | `#3b0764 → #7e22ce → #a855f7` |
    | `GRAY` | `#111827 → #374151 → #6b7280` |

    Custom palette: `Palette(start, mid, end)`.
    """)
    return


@app.cell
def _(BLUE, Cover, Text):
    Cover(
        title="Project with blue theme",
        subtitle="Same system, different colors.",
        date="April 2026",
        palette=BLUE,
        content=[
            Text("**Key point 1** — Color doesn't change the structure."),
            Text("**Key point 2** — Just pass `palette=BLUE`."),
            Text("**Key point 3** — Everything else works the same."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="Pipeline evidence",
        content=[
            Text("""
            ## Ultimos periodos disponibles por tabla

            Aquí se van a mostrar los ultimos periodos disponibles por tabla en ambas Bases de Datos
            """),
            Text(
                """
                |bd_in_modelos | aa_modelos|
                |--------------|-----------|
                |              |           |
                """
            ),
        ]
    ).render()
    return


if __name__ == "__main__":
    app.run()
