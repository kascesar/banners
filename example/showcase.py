"""
showcase.py — banners capabilities showcase.

Run with:
    uv run marimo edit example/showcase.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", layout_file="layouts/showcase.slides.json")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    from banners import configure, Background
    from banners.slides import Cover, Intro, Section, Closing
    from banners.content import (
        Text, Image, Graph, AnimatedGraph, Table, Plot, FlowAnimation, Manim,
    )
    from banners.palette import Palette, ORANGE, BLUE, GREEN, PURPLE, GRAY
    from manim import (
        Scene, Text as MT, Write, FadeIn, Create,
        Line, LEFT, RIGHT, UP,
    )

    configure(team="banners", date="2026", palette=ORANGE)
    return (
        AnimatedGraph,
        BLUE,
        Background,
        Closing,
        Cover,
        Create,
        FadeIn,
        FlowAnimation,
        GRAY,
        GREEN,
        Graph,
        Image,
        Intro,
        LEFT,
        Line,
        MT,
        Manim,
        PURPLE,
        Palette,
        Plot,
        RIGHT,
        Scene,
        Section,
        Table,
        Text,
        UP,
        Write,
        mo,
        np,
        pd,
        plt,
    )


@app.cell
def _(Create, FadeIn, LEFT, Line, MT, Manim, RIGHT, Scene, UP):
    class _Part0Title(Scene):
        def construct(self):
            self.camera.background_color = "#0f172a"
            title = MT("Showing marimo-banners", font_size=38, color="#9ca3af")
            line  = Line(LEFT * 4, RIGHT * 4, color="#374151", stroke_width=1.5).next_to(title, UP * (-1), buff=0.3)
            self.play(FadeIn(title, shift=UP * 0.15))
            self.play(Create(line))
            self.wait(1.5)

    Manim(_Part0Title, quality="high", autoplay=True).render()
    return


@app.cell
def _(Create, FadeIn, LEFT, Line, MT, Manim, RIGHT, Scene, UP, Write):
    class _Part1Title(Scene):
        def construct(self):
            self.camera.background_color = "#0f172a"
            num   = MT("01", font_size=140, color="#ea580c").shift(UP * 0.6)
            title = MT("Slide Types & Palettes", font_size=38, color="#9ca3af").next_to(num, UP * (-1), buff=0.25)
            line  = Line(LEFT * 4, RIGHT * 4, color="#374151", stroke_width=1.5).next_to(title, UP * (-1), buff=0.3)
            self.play(Write(num), run_time=1.2)
            self.play(FadeIn(title, shift=UP * 0.15))
            self.play(Create(line))
            self.wait(1.5)

    Manim(_Part1Title, quality="high", autoplay=True).render()
    return


@app.cell
def _(Cover, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    configure(team="banners", date="2026", palette=ORANGE)

    Cover(
    title="My Project",
    subtitle="One-line context for the audience.",
    content=[
        Text("**Point 1** — Something relevant."),
        Text("**Point 2** — A concrete result."),
        Text("**Point 3** — Team or business impact."),
    ],
    content_kind="neutral",
    ).render()
    ```
    """),
        Cover(
            title="Cover — large centered banner",
            subtitle="Typically the first slide. Global settings via configure().",
            content=[
                Text("**Point 1** — Something relevant."),
                Text("**Point 2** — A concrete result."),
                Text("**Point 3** — Team or business impact."),
            ],
            content_kind="neutral",
        ).render(),
    ], gap="0.5rem")
    return


@app.cell
def _(Intro, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    Intro(
    title="Why we're here",
    subtitle="Context and motivation.",
    tag="Context",
    summary="One key fact the audience must hold before the content.",
    content=[
        Text("**Risk** — What was at stake."),
        Text("**Gap** — What was missing."),
        Text("**Opportunity** — What we could gain."),
    ],
    content_kind="warn",
    footer="The question wasn't whether — but how.",
    ).render()
    ```
    """),
        Intro(
            title="Intro — context slide",
            subtitle="Sets up context before diving into content.",
            tag="Context",
            summary="One key fact the audience must hold before the content.",
            content=[
                Text("**Risk** — What was at stake."),
                Text("**Gap** — What was missing."),
                Text("**Opportunity** — What we could gain."),
            ],
            content_kind="warn",
            footer="The question wasn't whether — but how.",
        ).render(),
    ], gap="0.5rem")
    return


@app.cell
def _(Section, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    # Counter resets each time configure() is called.
    Section(
    title="Results",
    subtitle="What we achieved.",
    content=[Text("...")],
    ).render()

    Section(title="Appendix", number="A1")  # override
    Section(title="No number", number="")   # suppress
    ```
    """),
        Section(
            title="Section — auto-numbered slide",
            subtitle="Numbers itself automatically: 01, 02, 03 …",
            content=[Text("Main content — text, plots, tables, animations…")],
        ).render(),
    ], gap="0.5rem")
    return


@app.cell
def _(Closing, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    Closing(
    title="Conclusions",
    subtitle="Three things to remember.",
    content=[
        Text("**First takeaway** — concise."),
        Text("**Second takeaway** — concrete."),
        Text("**Third takeaway** — actionable."),
    ],
    content_kind="neutral",
    ).render()
    ```
    """),
        Closing(
            title="Closing — final banner",
            subtitle="Same structure as Cover — summarize and close.",
            content=[
                Text("**First takeaway** — concise."),
                Text("**Second takeaway** — concrete."),
                Text("**Third takeaway** — actionable."),
            ],
            content_kind="neutral",
        ).render(),
    ], gap="0.5rem")
    return


@app.cell
def _(BLUE, GRAY, GREEN, PURPLE, Section, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    from banners.palette import ORANGE, BLUE, GREEN, PURPLE, GRAY

    Cover(title="...", palette=BLUE, ...).render()
    ```
    """),
        mo.hstack([
            Section(title="BLUE",   subtitle="palette=BLUE",   content=[Text("…")], palette=BLUE).render(),
            Section(title="GREEN",  subtitle="palette=GREEN",  content=[Text("…")], palette=GREEN).render(),
            Section(title="PURPLE", subtitle="palette=PURPLE", content=[Text("…")], palette=PURPLE).render(),
            Section(title="GRAY",   subtitle="palette=GRAY",   content=[Text("…")], palette=GRAY).render(),
        ], gap="0.75rem"),
    ], gap="0.5rem")
    return


@app.cell
def _(Cover, Palette, Text, mo):
    _custom = Palette(start="#1a0533", mid="#6d28d9", end="#a78bfa")
    mo.vstack([
        mo.md("""
    ```python
    from banners.palette import Palette

    custom = Palette(start="#1a0533", mid="#6d28d9", end="#a78bfa")
    Cover(title="...", palette=custom, ...).render()
    ```
    """),
        Cover(
            title="Custom palette",
            subtitle="Palette(start, mid, end) — any CSS colors.",
            content=[Text("The gradient flows `start` → `mid` → `end`.")],
            palette=_custom,
        ).render(),
    ], gap="0.5rem")
    return


@app.cell
def _(Create, FadeIn, LEFT, Line, MT, Manim, RIGHT, Scene, UP, Write):
    class _Part2Title(Scene):
        def construct(self):
            self.camera.background_color = "#0f172a"
            num   = MT("02", font_size=140, color="#1d4ed8").shift(UP * 0.6)
            title = MT("Content Types", font_size=38, color="#9ca3af").next_to(num, UP * (-1), buff=0.25)
            line  = Line(LEFT * 4, RIGHT * 4, color="#374151", stroke_width=1.5).next_to(title, UP * (-1), buff=0.3)
            self.play(Write(num), run_time=1.2)
            self.play(FadeIn(title, shift=UP * 0.15))
            self.play(Create(line))
            self.wait(1.5)

    Manim(_Part2Title, quality="high", autoplay=True).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="Text — markdown + LaTeX",
        subtitle="Full CommonMark support including tables and math.",
        content=[
            Text(r"""
    ```python
    Text(r'''
    **Bold**, *italic*, `code`.
    - Lists
    | Col A | Col B |
    |-------|-------|
    | 1     | 2     |
    $$E = mc^2$$
    ''')
    ```
    """),
            Text(r"""
    **Bold**, *italic*, `code`.

    - Bullet lists
    - Multiple items

    | Col A | Col B |
    |-------|-------|
    | 1     | 2     |

    $$E = mc^2$$
    """),
        ],
    ).render()


    # ── content_kind ──────────────────────────────────────
    return


@app.cell
def _(Section, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    Section(
    content=[Text("..."), Text("...")],
    content_kind="info",   # "neutral" | "info" | "success" | "warn" | "danger"
    ).render()
    ```
    """),
        mo.hstack([
            Section(title="neutral", content=[Text("neutral"), Text("neutral")], content_kind="neutral").render(),
            Section(title="info",    content=[Text("info"),    Text("info")],    content_kind="info").render(),
            Section(title="success", content=[Text("success"), Text("success")], content_kind="success").render(),
            Section(title="warn",    content=[Text("warn"),    Text("warn")],    content_kind="warn").render(),
            Section(title="danger",  content=[Text("danger"),  Text("danger")],  content_kind="danger").render(),
        ], gap="0.75rem"),
    ], gap="0.5rem")
    return


@app.cell
def _(Image, Section, Text):
    Section(
        title="Image — path, URL, or bytes",
        subtitle="Accepts a file path, URL, or raw bytes.",
        content=[
            Text("""
    ```python
    Section(
    content=[Image("https://picsum.photos/seed/banners/800/450")],
    ).render()
    ```
    """),
            Image("https://picsum.photos/seed/banners/800/450"),
        ],
    ).render()
    return


@app.cell
def _(Graph, Section, Text):
    Section(
        title="Graph — static Mermaid diagram",
        subtitle="Renders any Mermaid graph LR / TD syntax.",
        content=[
            Text("""
    ```python
    Graph(\"\"\"
    graph LR
    A[Ingest] --> B[Validate]
    B --> C[Transform]
    C --> D[Load]
    \"\"\")
    ```
    """),
            Graph("""
    graph LR
    A[Ingest] --> B[Validate]
    B --> C[Transform]
    C --> D[Load]
    """),
        ],
    ).render()
    return


@app.cell
def _(AnimatedGraph, Section, Text):
    Section(
        title="AnimatedGraph — click nodes to highlight",
        subtitle="Interactive: click any node to toggle its highlight color.",
        content=[
            Text("""
    ```python
    AnimatedGraph(\"\"\"
    graph LR
    A[Raw data] --> B[Validate]
    B --> C[Feature eng.]
    C --> D[Train]
    D --> E[Deploy]
    \"\"\", highlight_color="#3b82f6")
    ```
    """),
            AnimatedGraph("""
    graph LR
    A[Raw data] --> B[Validate]
    B --> C[Feature eng.]
    C --> D[Train]
    D --> E[Deploy]
    """, highlight_color="#3b82f6"),
        ],
    ).render()
    return


@app.cell
def _(Section, Table, Text, pd):
    _df = pd.DataFrame({
        "Model":        ["Baseline", "v1",        "v2"],
        "AUC":          [0.71,       0.84,         0.91],
        "Latency (ms)": [12,         18,           22],
        "Status":       ["retired",  "production", "staging"],
    })
    Section(
        title="Table — pandas DataFrame",
        subtitle="Wrap any DataFrame with Table().",
        content=[
            Text("""
    ```python
    import pandas as pd

    df = pd.DataFrame({...})
    Section(content=[Table(df)]).render()
    ```
    """),
            Table(_df),
        ],
    ).render()
    return


@app.cell
def _(Plot, Section, Text, np, plt):
    _fig, _ax = plt.subplots(figsize=(7, 3.2))
    _fig.patch.set_facecolor("#0f172a")
    _ax.set_facecolor("#0f172a")
    _x = np.linspace(0, 10, 300)
    _ax.plot(_x, np.sin(_x), color="#3b82f6", linewidth=2, label="sin(x)")
    _ax.plot(_x, np.cos(_x), color="#22c55e", linewidth=2, label="cos(x)")
    _ax.tick_params(colors="#6b7280")
    for _sp in _ax.spines.values():
        _sp.set_color("#374151")
    _ax.legend(facecolor="#1f2937", edgecolor="#374151", labelcolor="white")
    _ax.grid(color="#1f2937")
    plt.tight_layout()

    Section(
        title="Plot — matplotlib or plotly",
        subtitle="Figure type is auto-detected.",
        content=[
            Text("""
    ```python
    fig, ax = plt.subplots(...)
    ax.plot(x, np.sin(x), ...)

    Section(content=[Plot(fig)]).render()
    # Also accepts plotly figures.
    ```
    """),
            Plot(_fig),
        ],
    ).render()
    return


@app.cell
def _(FlowAnimation, Section, Text):
    Section(
        title="FlowAnimation — click to advance",
        subtitle="Step-by-step pipeline animation. Three input formats.",
        content=[
            Text("""
    ```python
    # Flat list → linear chain
    FlowAnimation(["Ingest", "Validate", "Transform", "Load"])

    # Nested list → layered topology
    FlowAnimation([["Ingest"], [{"name":"A"}, {"name":"B"}], ["Load"]])

    # Explicit graph → arbitrary edges
    FlowAnimation(nodes=["A","B","C"], edges=[("A","B"),("A","C")])
    ```
    """),
            FlowAnimation(["Ingest", "Validate", "Transform", "Load"]),
        ],
    ).render()
    return


@app.cell
def _(FadeOut, MW, Manim, MathTex, Scene, Section, Text, Write):
    class BasicScene(Scene):
        def construct(self):
            self.camera.background_color = "#0f172a"
            self.next_section("eq1")
            eq1 = MathTex(r"E = mc^2", font_size=72, color=MW)
            self.play(Write(eq1)); self.wait(1)
            self.next_section("eq2")
            eq2 = MathTex(r"F = ma", font_size=72, color=MW)
            self.play(FadeOut(eq1)); self.play(Write(eq2)); self.wait(1)
            self.next_section("eq3")
            eq3 = MathTex(
                r"\nabla^2 \mathbf{E} = \frac{1}{c^2}\frac{\partial^2\mathbf{E}}{\partial t^2}",
                font_size=52, color=MW,
            )
            self.play(FadeOut(eq2)); self.play(Write(eq3)); self.wait(1)

    Section(
        title="Manim — click-to-advance animation",
        subtitle="Each next_section() call becomes one click. Results are cached on disk.",
        content=[
            Text("""
    ```python
    class MyScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        self.next_section("step1")   # one click per section
        self.play(Write(MathTex(r"E = mc^2", color=MW)))
        self.wait(1)

        self.next_section("step2")
        # ...

    Section(content=[Manim(MyScene, interactive=True, quality="medium")]).render()
    ```
    """),
            Manim(BasicScene, interactive=True, quality="medium", width="100%"),
        ],
    ).render()
    return


@app.cell
def _(Create, FadeIn, LEFT, Line, MT, Manim, RIGHT, Scene, UP, Write):
    class _Part3Title(Scene):
        def construct(self):
            self.camera.background_color = "#0f172a"
            num   = MT("03", font_size=140, color="#15803d").shift(UP * 0.6)
            title = MT("Slide Backgrounds", font_size=38, color="#9ca3af").next_to(num, UP * (-1), buff=0.25)
            line  = Line(LEFT * 4, RIGHT * 4, color="#374151", stroke_width=1.5).next_to(title, UP * (-1), buff=0.3)
            self.play(Write(num), run_time=1.2)
            self.play(FadeIn(title, shift=UP * 0.15))
            self.play(Create(line))
            self.wait(1.5)

    Manim(_Part3Title, quality="high", autoplay=True).render()
    return


@app.cell
def _(Background, Cover, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    Cover(
    title="...",
    background=Background.color("#0f172a"),
    ).render()
    ```
    """),
        Cover(
            title="Solid color background",
            subtitle="Background.color() — any CSS color.",
            content=[Text("The entire slide area uses the specified color.")],
            background=Background.color("#0f172a"),
        ).render(),
    ], gap="0.5rem")
    return


@app.cell
def _(Background, Section, Text, mo):
    mo.vstack([
        mo.md("""
    ```python
    # 2-stop
    Background.gradient("#0d1b2a", "#4a1a6e")

    # 3-stop with angle
    Background.gradient("#0d1b2a", "#4a1a6e", mid="#1a2a5e", angle=45)
    ```
    """),
        mo.vstack([
            Section(
                title="2-stop gradient",
                content=[Text("Background.gradient(start, end)")],
                background=Background.gradient("#0d1b2a", "#4a1a6e"),
            ).render(),
            Section(
                title="3-stop + angle",
                content=[Text("Background.gradient(start, end, mid=, angle=)")],
                background=Background.gradient("#0d1b2a", "#4a1a6e", mid="#1a2a5e", angle=45),
            ).render(),
        ]),
    ])
    return


@app.cell
def _(Background, Section, Text, mo):

    mo.md("""
    ```python
    Cover(
    title="...",
    background=Background.image(
        "path/or/url.jpg",
        overlay="rgba(0,0,0,0.55)",
    ),
    ).render()
    ```
    """)
    Section(
            title="Image background",
            subtitle="Background.image() — path, URL, or raw bytes.",
            content=[Text("Dark overlay applied automatically. Pass `overlay=None` to disable."),
                     Text("Dark overlay applied automatically. Pass `overlay=None` to disable.")],
            background=Background.image(
                "https://picsum.photos/seed/wave/1200/600",
                #overlay="rgba(0,0,0,0.55)",
            ),
            content_kind="warn"
    )
    return


@app.cell
def _(BLUE, Background, Cover, Intro, Section, Text, mo):
    _bg = Background.gradient("#0d1b2a", "#1e3a5f")
    mo.vstack([
        mo.md("""
    ```python
    configure(
    team="banners",
    palette=BLUE,
    background=Background.gradient("#0d1b2a", "#1e3a5f"),
    )
    # All slides inherit this background.
    # Override per slide: Cover(title="...", background=Background.color("#000"))
    ```
    """),
        mo.vstack([
            Cover(title="Cover",     subtitle="inherits bg", content=[Text("…")], palette=BLUE, background=_bg).render(),
            Intro(title="Intro",     subtitle="inherits bg", content=[Text("…")], palette=BLUE, background=_bg).render(),
            Section(title="Section", subtitle="inherits bg", content=[Text("…")], palette=BLUE, background=_bg).render(),
        ]),
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
