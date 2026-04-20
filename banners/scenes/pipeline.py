"""PipelineScene — animated data pipeline diagram for Manim."""


def PipelineScene():
    """Return a Manim Scene that builds a data pipeline step by step.

    Each `next_section()` call marks a click-advance point when used with
    `Manim(PipelineScene, interactive=True)`.

    Stages rendered in sequence:
    1. Raw node appears
    2. Validate node + arrow
    3. Two parallel branches (Transform A / Transform B)
    4. Join node merging both branches
    5. Load node + final arrow
    6. Status labels appear on each node

    Requires `manim` to be installed:
    ```bash
    uv pip install "banners[manim]"
    ```

    Example:
        ```python
        from banners.content import Manim
        from banners.scenes import PipelineScene

        Manim(PipelineScene, interactive=True).render()
        ```
    """
    try:
        from manim import (
            Scene, VGroup, RoundedRectangle, Text, Arrow,
            FadeIn, GrowArrow, Write, FadeOut,
            UP, DOWN, LEFT, RIGHT, ORIGIN,
            WHITE, GRAY, GREEN, YELLOW, BLUE, ORANGE,
            Create, Transform,
            ManimColor,
        )
    except ImportError as e:
        raise ImportError("manim is required. Run: uv pip install 'banners[manim]'") from e

    ACCENT   = ManimColor("#ea580c")
    NODE_BG  = ManimColor("#1c1c1c")
    OK_COLOR = ManimColor("#22c55e")

    def make_node(label: str, sublabel: str = "", color=WHITE, width=2.4, height=0.75):
        box = RoundedRectangle(
            corner_radius=0.12, width=width, height=height,
            fill_color=NODE_BG, fill_opacity=1,
            stroke_color=color, stroke_width=2.5,
        )
        txt = Text(label, font_size=22, color=color)
        group = VGroup(box, txt)
        if sublabel:
            sub = Text(sublabel, font_size=14, color=GRAY)
            sub.next_to(txt, DOWN, buff=0.05)
            group.add(sub)
        group.move_to(ORIGIN)
        return group

    class _PipelineScene(Scene):
        def construct(self):
            title = Text("Data Pipeline", font_size=32, color=ACCENT)
            title.to_edge(UP, buff=0.3)
            self.play(FadeIn(title))

            # ── Step 1: Raw ────────────────────────────────────────────────
            self.next_section("raw")
            raw = make_node("Raw Data", "S3 bucket", color=WHITE)
            raw.shift(LEFT * 4.5)
            self.play(Create(raw))

            # ── Step 2: Validate ───────────────────────────────────────────
            self.next_section("validate")
            val = make_node("Validate", "schema + nulls", color=YELLOW)
            val.shift(LEFT * 1.8)
            a1 = Arrow(raw.get_right(), val.get_left(), buff=0.1,
                       color=GRAY, stroke_width=2)
            self.play(GrowArrow(a1), FadeIn(val))

            # ── Step 3: Parallel branches ──────────────────────────────────
            self.next_section("branches")
            tr_a = make_node("Transform A", "feature eng.", color=BLUE, width=2.6)
            tr_b = make_node("Transform B", "outlier filter", color=BLUE, width=2.6)
            tr_a.shift(RIGHT * 0.9 + UP * 1.1)
            tr_b.shift(RIGHT * 0.9 + DOWN * 1.1)
            a2a = Arrow(val.get_right(), tr_a.get_left(), buff=0.1,
                        color=GRAY, stroke_width=2)
            a2b = Arrow(val.get_right(), tr_b.get_left(), buff=0.1,
                        color=GRAY, stroke_width=2)
            self.play(GrowArrow(a2a), GrowArrow(a2b), FadeIn(tr_a), FadeIn(tr_b))

            # ── Step 4: Join ───────────────────────────────────────────────
            self.next_section("join")
            join = make_node("Join", "concat + dedup", color=ORANGE)
            join.shift(RIGHT * 3.6)
            a3a = Arrow(tr_a.get_right(), join.get_left(), buff=0.1,
                        color=GRAY, stroke_width=2)
            a3b = Arrow(tr_b.get_right(), join.get_left(), buff=0.1,
                        color=GRAY, stroke_width=2)
            self.play(GrowArrow(a3a), GrowArrow(a3b), FadeIn(join))

            # ── Step 5: Load ───────────────────────────────────────────────
            self.next_section("load")
            load = make_node("Load", "Athena table", color=ACCENT)
            load.shift(RIGHT * 5.8)  # noqa: E501  — intentionally wider shift
            a4 = Arrow(join.get_right(), load.get_left(), buff=0.1,
                       color=ACCENT, stroke_width=2.5)
            self.play(GrowArrow(a4), FadeIn(load))

            # ── Step 6: Status labels ──────────────────────────────────────
            self.next_section("status")
            ok_nodes = [raw, val, tr_a, tr_b, join, load]
            labels = []
            for node in ok_nodes:
                lbl = Text("✓", font_size=18, color=OK_COLOR)
                lbl.next_to(node, UP, buff=0.08)
                labels.append(lbl)
            self.play(*[Write(l) for l in labels])
            self.wait(1)

    return _PipelineScene
