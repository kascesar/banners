"""
test.py — Reference guide and visual demo for the banners slide system.
Run with: uv run marimo edit test.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", layout_file="layouts/test.slides.json")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text, Image, Graph, AnimatedGraph, Table, Plot, Manim, FlowAnimation
    from banners.palette import Palette, BLUE, GREEN, PURPLE, GRAY

    return (
        AnimatedGraph,
        BLUE,
        Closing,
        Cover,
        FlowAnimation,
        GRAY,
        Graph,
        Image,
        Intro,
        Manim,
        Palette,
        Section,
        Text,
        configure,
        mo,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Banners — Reference Guide

    ---

    ## Import

    ```python
    from banners import configure
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import Text, Image, Graph, Table, Plot
    from banners.palette import Palette, BLUE, GREEN, PURPLE, GRAY
    ```

    ---

    ## Global configuration

    Call `configure()` once at the top of the notebook.
    All slides inherit these values automatically — no need to repeat them slide by slide.

    ```python
    configure(
        team="Analytics Team",
        date="April 2026",
        palette=BLUE,
        icon={"src": "img/logo.png"},
    )
    ```

    | Parameter | Used by | Description |
    |-----------|---------|-------------|
    | `team`    | `Cover`, `Intro`, `Closing` | Label shown in the banner |
    | `date`    | `Cover` | Date line at the bottom of the banner |
    | `palette` | `Cover`, `Intro`, `Closing` | Color palette (`BLUE`, `GREEN`, etc.) |
    | `icon`    | All slides | Logo/icon placed on the banner |

    Calling `configure()` also **resets the `Section` auto-number counter** to `0`.

    Any parameter passed explicitly to a slide overrides the global value.

    ---

    ## Slides

    | Class | Purpose | Typical position |
    |-------|---------|-----------------|
    | `Cover` | Large centered banner | First slide |
    | `Intro` | Context or problem statement | Slides 2–3 |
    | `Section` | Intermediate section slide | Middle slides |
    | `Closing` | Closing slide with optional metrics | Last slide |

    All slides accept a `footer` parameter that renders a blockquote at the bottom.

    ---

    ## Content types

    | Class | Renders |
    |-------|---------|
    | `Text(body)` | Markdown — paragraphs, lists, tables |
    | `Image(src, width)` | Image from path, bytes, or URL |
    | `Graph(diagram)` | Mermaid diagram (static) |
    | `AnimatedGraph(diagram)` | Mermaid diagram — click nodes to highlight |
    | `Table(df)` | pandas DataFrame |
    | `Plot(fig)` | matplotlib or plotly figure (auto-detected) |
    | `Manim(scene)` | Manim animation — GIF, PNG, or MP4 |

    ## Automatic layouts

    | Content | Layout |
    |---------|--------|
    | Single item | Full width |
    | List of `Text` only + `content_kind` | Equal columns with styled box |
    | List with any other element | Equal-width CSS grid (`1fr` per column) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## `configure()` — global setup

    Place this cell at the top of every notebook.
    `team`, `date`, and `palette` will be inherited by all slides automatically.
    """)
    return


@app.cell
def _(BLUE, configure):
    configure(
        team="Analytics Team",
        date="April 2026",
        palette=BLUE,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Cover

    Large centered banner. Use as the **first slide**.

    `team`, `date`, and `palette` are inherited from `configure()`.

    ```python
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
    ```
    """)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Intro

    Compact banner with gradient. For slides that open a thematic block.

    `team` and `palette` are inherited from `configure()`.

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

    `Section` slides **auto-number** starting from `01`. The counter resets
    each time `configure()` is called. Override with `number="..."` or suppress
    with `number="\"`.

    Exclusive parameters:
    - `number` — Large number on the left. Auto-assigned if omitted.
    - `footer` — Quote at the bottom as a blockquote.

    ### Text columns
    """)
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
    ### Two images side by side
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
    ### Markdown table in Text
    """)
    return


@app.cell
def _(Image, Section, Text):
    Section(
        title="Before vs after",
        content=[
            Text("""
    | Before | After |
    |--------|-------|
    | Hardcoded per model  | Parameterized for any model |
    | n models = n projects | n models = 1 framework     |
    """),
            Image("img/test.jpeg", width="100%"),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `footer` — available on all slides

    Every slide type accepts a `footer` parameter.
    It renders as a blockquote below the content.
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `Table` — pandas DataFrame

    Wrap any DataFrame in `Table(df)` to display it inside a slide.

    ```python
    import pandas as pd
    from banners.content import Table

    df = pd.DataFrame({
        "Model": ["Churn v1", "Churn v2", "LTV"],
        "AUC": [0.84, 0.91, 0.88],
        "Latency (ms)": [42, 28, 35],
    })

    Section(title="Model comparison", content=Table(df)).render()

    # Mixed with other elements:
    Section(
        title="Results",
        content=[Text("All models exceeded the 0.85 AUC baseline."), Table(df)],
    ).render()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### `Plot` — matplotlib or plotly

    Wrap any figure in `Plot(fig)`. The type is detected automatically:
    matplotlib figures use `mo.as_html`, plotly figures use `mo.ui.plotly`.

    ```python
    import matplotlib.pyplot as plt
    from banners.content import Plot

    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [10, 8, 12, 9])
    Section(title="Trend", content=Plot(fig)).render()
    ```

    ```python
    import plotly.express as px
    from banners.content import Plot

    fig = px.bar(df, x="Model", y="AUC")
    Section(
        title="Model comparison",
        content=[Text("All models exceeded the 0.85 baseline."), Plot(fig)],
    ).render()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Closing

    Large centered banner, same visual weight as `Cover`.

    `team` and `palette` are inherited from `configure()`.

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

    All slides accept a `palette` parameter. Set it globally with `configure(palette=...)`.
    The default is orange.

    | Constant | Gradient |
    |----------|----------|
    | `ORANGE` (default) | `#7c2d12 → #c2410c → #ea580c` |
    | `BLUE` | `#1e3a5f → #1d4ed8 → #3b82f6` |
    | `GREEN` | `#14532d → #15803d → #22c55e` |
    | `PURPLE` | `#3b0764 → #7e22ce → #a855f7` |
    | `GRAY` | `#111827 → #374151 → #6b7280` |

    Custom palette: `Palette(start, mid, end)`.

    A per-slide `palette=` always overrides the global value.
    """)
    return


@app.cell
def _(Cover, GRAY, Text, configure):
    configure(palette=GRAY, team="Analytics Team", date="April 2026")
    Cover(
        title="Project with gray theme",
        subtitle="Per-notebook palette set via configure().",
        content=[
            Text("**Key point 1** — Set once, inherited by all slides."),
            Text("**Key point 2** — Override per slide if needed."),
            Text("**Key point 3** — Everything else works the same."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Custom palette

    Use `Palette(start, mid, end)` to define any color scheme and pass it to
    `configure()`. All slides — including `Section` — will derive their colors
    from it automatically.

    ```python
    from banners.palette import Palette

    teal = Palette(start="#042f2e", mid="#0f766e", end="#2dd4bf")
    configure(palette=teal, team="Analytics Team", date="April 2026")
    ```

    `Section` derives its border and background from the same palette:
    - **border** → `end` color (accent)
    - **background** → darkened `start` (keeps the dark-panel feel)
    """)
    return


@app.cell
def _(Cover, Palette, Text, configure):
    teal = Palette(start="#042f2e", mid="#0f766e", end="#2dd4bf")
    configure(palette=teal, team="Analytics Team", date="April 2026")

    Cover(
        title="Custom teal palette",
        subtitle="Defined with Palette(start, mid, end) and passed to configure().",
        content=[
            Text("**Cover** — inherits palette via configure()."),
            Text("**Intro / Closing** — same gradient, no extra work."),
            Text("**Section** — border and background derived automatically."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(Intro, Text):
    Intro(
        title="Intro with teal palette",
        subtitle="Inherited automatically — no palette= needed.",
        tag="Context",
        summary="The palette flows from configure() into every slide type.",
        content=[
            Text("**Cover** — full gradient banner."),
            Text("**Intro** — compact gradient banner."),
            Text("**Section** — border accent + dark background."),
        ],
        content_kind="info",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="Section with teal palette",
        subtitle="Border and background derived from the custom palette.",
        content=Text("""
    The border takes the `end` color and the background is a darkened
    version of `start` — consistent with the overall scheme without any
    extra configuration.
    """),
        footer="All three slide types share the same color source.",
    ).render()
    return


@app.cell
def _(Closing):
    Closing(
        title="Closing with teal palette.",
        subtitle="One palette definition, every slide covered.",
        stats=[
            ("1", "Palette defined", "Palette(start, mid, end)"),
            ("4", "Slide types covered", "Cover · Intro · Section · Closing"),
            ("0", "Extra config needed", "configure() does the rest"),
        ],
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## `Manim` — mathematical animations

    Requires the optional dependency:

    ```bash
    uv pip install "banners[manim]"
    ```

    Pass a `Scene` subclass (not an instance) to `Manim`. The scene is rendered
    on the first `render()` call and cached — it won't re-render on subsequent
    marimo reruns.

    | Parameter | Default | Options |
    |-----------|---------|---------|
    | `format`  | `"gif"` | `"gif"`, `"png"`, `"mp4"` |
    | `quality` | `"low"` | `"low"`, `"medium"`, `"high"` |

    `"gif"` and `"png"` embed as `mo.image`; `"mp4"` embeds as `mo.video`.

    If `manim` is not installed, a warning callout is shown instead of an error.

    ```python
    from manim import Scene, Circle, Create
    from banners.content import Manim

    class CircleScene(Scene):
        def construct(self):
            self.play(Create(Circle()))

    # Single animation — full width
    Section(title="Demo", content=Manim(CircleScene)).render()

    # Alongside text — CSS grid
    Section(
        title="Circle",
        content=[
            Text("A circle is the set of points equidistant from a center."),
            Manim(CircleScene, format="gif", quality="low"),
        ],
    ).render()
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## `AnimatedGraph` — interactive Mermaid diagram

    Same Mermaid syntax as `Graph` but nodes highlight on click.
    Works offline — mermaid.js is bundled with the package.
    Supports any topology: linear, branches, merges, cycles.

    | Parameter | Default | Description |
    |-----------|---------|-------------|
    | `highlight_color` | `"#ea580c"` | Color applied to highlighted nodes |
    | `theme` | `"dark"` | Mermaid theme: `default`, `dark`, `neutral`, `forest` |

    ### Linear pipeline
    """)
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Pipeline flow — click nodes to highlight",
        content=AnimatedGraph("""
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
    ### With bifurcation and merge
    """)
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Parallel transforms — click nodes to highlight",
        content=AnimatedGraph("""
    graph LR
    A[Ingest] --> B[Validate]
    B --> C[Transform A]
    B --> D[Transform B]
    C --> E[Join]
    D --> E
    E --> F[Load]
    """),
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### With cycle (retry loop)
    """)
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Retry loop — click nodes to highlight",
        content=AnimatedGraph("""
    graph LR
    A[Fetch] --> B[Validate]
    B -->|ok| C[Process]
    B -->|fail| A
    C --> D[Store]
    """),
    ).render()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## `Manim` — mathematical animations

    Requires the optional dependency:

    ```bash
    uv pip install "banners[manim]"
    ```

    | Parameter | Default | Options |
    |-----------|---------|---------|
    | `format`  | `"gif"` | `"gif"`, `"png"`, `"mp4"` |
    | `quality` | `"low"` | `"low"`, `"medium"`, `"high"` |
    | `interactive` | `False` | `True` renders sections as click-to-advance frames |

    When `interactive=True` the scene must define steps with `self.next_section("name")`.
    Each section becomes a frame — click the image to advance to the next step.

    ### Standard GIF
    ]
    ```python
    from manim import Scene, Circle, Create
    from banners.content import Manim

    class CircleScene(Scene):
        def construct(self):
            self.play(Create(Circle()))

    Section(title="Demo", content=Manim(CircleScene)).render()
    ```

    ### Click-to-advance with `PipelineScene`

    `PipelineScene` builds a data pipeline step by step.
    Each click reveals the next stage: Raw → Validate → Branches → Join → Load → Status.

    ```python
    from banners.content import Manim
    from banners.scenes import PipelineScene

    Section(
        title="Pipeline architecture",
        content=Manim(PipelineScene, interactive=True, quality="medium"),
    ).render()
    ```

    ### Custom interactive scene

    ```python
    from manim import Scene, Circle, Square, Create, Transform
    from banners.content import Manim

    class MyScene(Scene):
        def construct(self):
            self.next_section("step_1")
            self.play(Create(Circle()))

            self.next_section("step_2")
            self.play(Transform(Circle(), Square()))

    Section(title="My animation", content=Manim(MyScene, interactive=True)).render()
    ```
    """)
    return


@app.cell
def _(Manim, Section):
    from manim import (
        Scene, RoundedRectangle, Arrow, Dot,
        Write, FadeIn, FadeOut, GrowArrow, Flash, Indicate,
        UP, DOWN, LEFT, RIGHT,
        WHITE as MW, YELLOW as MY, GRAY as MG,
        Text as MText,
    )

    class ETLPipelineScene(Scene):
        STAGES = [
            ("S3\nRaw",           "#3b82f6"),
            ("Glue\nJob",         "#8b5cf6"),
            ("Athena\nQuery",     "#f59e0b"),
            ("SageMaker\nTrain",  "#10b981"),
            ("Redshift\nLoad",    "#ef4444"),
        ]
        BG = "#0f172a"

        def construct(self):
            self.camera.background_color = self.BG

            title = MText("Data & ML Pipeline", font_size=32, color=MW, weight="BOLD")
            title.to_edge(UP, buff=0.35)
            self.play(Write(title), run_time=0.5)

            n = len(self.STAGES)
            spacing = 2.4
            xs = [(i - (n - 1) / 2) * spacing for i in range(n)]

            boxes, labels = [], []
            for x, (name, color) in zip(xs, self.STAGES):
                rect = RoundedRectangle(
                    width=1.9, height=1.0, corner_radius=0.15,
                    fill_color=color, fill_opacity=0.18,
                    stroke_color=color, stroke_width=2,
                ).move_to([x, -0.3, 0])
                lbl = MText(name, font_size=16, color=color, weight="BOLD")
                lbl.move_to(rect)
                boxes.append(rect)
                labels.append(lbl)

            arrows = [
                Arrow(boxes[i].get_right(), boxes[i + 1].get_left(),
                      buff=0.08, color=MG, stroke_width=2,
                      max_tip_length_to_length_ratio=0.18)
                for i in range(n - 1)
            ]

            for i, (rect, lbl) in enumerate(zip(boxes, labels)):
                self.play(FadeIn(rect, scale=0.85), Write(lbl), run_time=0.35)
                if i < len(arrows):
                    self.play(GrowArrow(arrows[i]), run_time=0.25)

            self.wait(0.3)

            for _ in range(2):
                dot = Dot(color=MY, radius=0.13).move_to(boxes[0].get_center())
                self.play(FadeIn(dot, scale=2.0), run_time=0.2)
                for box in boxes[1:]:
                    self.play(dot.animate.move_to(box.get_center()), run_time=0.3)
                    self.play(Flash(dot, color=MY, line_length=0.18, num_lines=8,
                                   flash_radius=0.28), run_time=0.25)
                self.play(FadeOut(dot, scale=0.3), run_time=0.2)

            self.play(
                *[Indicate(b, color=MY, scale_factor=1.08) for b in boxes],
                run_time=0.6,
            )
            self.wait(0.4)

    Section(title="ETL & ML pipeline", content=Manim(ETLPipelineScene, format="gif", quality="low")).render()
    return


@app.cell
def _(FlowAnimation, Section):

    Section(
        title="ETL & ML pipeline",
        content=FlowAnimation(["S3", "Glue", "Athena", "SageMaker", "Redshift"])
    ).render()
    return


if __name__ == "__main__":
    app.run()
