"""
08_manim.py — Manim content element: static and interactive animations.
Run with: uv run marimo edit test/08_manim.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full", layout_file="layouts/08_manim.slides.json")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Section
    from banners.content import Manim, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return Manim, Section, Text, mo


@app.cell
def _(mo):
    mo.md(r"""
    # Manim element

    `Manim(scene, ...)` renders a [Manim](https://www.manim.community/) `Scene`
    subclass and embeds the result in a slide.

    Requires the optional dependency:

    ```bash
    uv pip install "banners[manim]"
    ```

    | Parameter | Default | Options |
    |-----------|---------|---------|
    | `scene` | — | A `Scene` subclass (pass the class, not an instance) |
    | `format` | `"gif"` | `"gif"`, `"png"`, `"mp4"` |
    | `quality` | `"low"` | `"low"`, `"medium"`, `"high"` |
    | `interactive` | `False` | `True` renders sections as click-to-advance frames |
    | `width` | `"100%"` | Any CSS value — controls player width |

    The scene is **rendered once and cached** — re-running the cell won't re-render.

    **Important:** when defining a scene inside a marimo cell, import Manim symbols
    with aliases to avoid conflicts with banners exports:
    ```python
    from manim import Text as MText, WHITE as MW, GRAY as MG
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Static GIF — basic scene
    """)
    return


@app.cell
def _(Manim, Section):
    from manim import (
        Scene, Circle, Square, Create, Transform, FadeOut,
        WHITE as MW,
    )

    class ShapeScene(Scene):
        def construct(self):
            self.camera.background_color = "#0f172a"
            c = Circle(color=MW, fill_opacity=0.3)
            s = Square(color="#3b82f6", fill_opacity=0.3)
            self.play(Create(c))
            self.play(Transform(c, s))
            self.play(FadeOut(c))

    Section(
        title="Shape animation",
        subtitle="Static GIF — format='gif', quality='low'.",
        content=Manim(ShapeScene, format="gif", quality="low"),
    ).render()
    return (Scene,)


@app.cell
def _(mo):
    mo.md("""
    ## Interactive — click to advance
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    When `interactive=True`, the scene must define steps with `self.next_section("name")`.
    Each section becomes a frame — **click the widget** to advance to the next step.

    ```python
    class MyScene(Scene):
        def construct(self):
            self.next_section("step_1")
            self.play(Create(Circle()))

            self.next_section("step_2")
            self.play(Transform(Circle(), Square()))
    ```
    """)
    return


@app.cell
def _(Manim, Scene, Section):
    from manim import (
        RoundedRectangle, Arrow, Dot,
        Write, FadeIn, FadeOut as MFO, GrowArrow, Flash,
        UP as MUP, DOWN as MDN, LEFT as ML, RIGHT as MR,
        WHITE as MW2, YELLOW as MY, GRAY as MG2,
        Text as MText2,
    )

    class ETLScene(Scene):
        STAGES = [
            ("S3\nRaw",          "#3b82f6"),
            ("Glue\nJob",        "#8b5cf6"),
            ("Athena\nQuery",    "#f59e0b"),
            ("SageMaker\nTrain", "#10b981"),
            ("Redshift\nLoad",   "#ef4444"),
        ]
        BG = "#0f172a"

        def construct(self):
            self.camera.background_color = self.BG

            title = MText2("Data & ML Pipeline", font_size=32, color=MW2, weight="BOLD")
            title.to_edge(MUP, buff=0.35)
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
                lbl = MText2(name, font_size=16, color=color, weight="BOLD")
                lbl.move_to(rect)
                boxes.append(rect)
                labels.append(lbl)

            arrows = [
                Arrow(boxes[i].get_right(), boxes[i + 1].get_left(),
                      buff=0.08, color=MG2, stroke_width=2,
                      max_tip_length_to_length_ratio=0.18)
                for i in range(n - 1)
            ]

            for i, (rect, lbl) in enumerate(zip(boxes, labels)):
                self.next_section(f"stage_{i}")
                self.play(FadeIn(rect, scale=0.85), Write(lbl), run_time=0.35)
                if i < len(arrows):
                    self.play(GrowArrow(arrows[i]), run_time=0.25)

    Section(
        title="ETL & ML pipeline",
        subtitle="Click to reveal each stage.",
        content=Manim(ETLScene, interactive=True, quality="low", width="500px"),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Interactive — width control
    """)
    return


@app.cell
def _(Manim, Section, Text):
    from manim import (
        Scene as MScene2,
        Circle as MCircle, Square as MSq, Triangle as MTri,
        Create as MCreate, Transform as MTrans, FadeOut as MFO2,
        WHITE as MW3, BLUE as MB3, GREEN as MGRN,
    )

    class ColorScene(MScene2):
        def construct(self):
            self.camera.background_color = "#0f172a"
            shapes = [
                MCircle(color=MW3, fill_opacity=0.4),
                MSq(color="#3b82f6", fill_opacity=0.4),
                MTri(color="#22c55e", fill_opacity=0.4),
            ]
            self.next_section("circle")
            self.play(MCreate(shapes[0]))
            self.next_section("square")
            self.play(MTrans(shapes[0], shapes[1]))
            self.next_section("triangle")
            self.play(MTrans(shapes[0], shapes[2]))

    Section(
        title="Shapes — constrained width",
        content=[
            Text("Use `width=` to control the player size.\nClick to advance between shapes."),
            Manim(ColorScene, interactive=True, quality="low", width="800px"),
        ],
    ).render()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
