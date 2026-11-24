"""PipelineScene — animated data pipeline diagram for Manim."""


def PipelineScene(palette=None):
    """Return a Manim Scene that builds a data pipeline step by step.

    Each `next_section()` call marks a click-advance point when used with
    `Manim(PipelineScene, interactive=True)`. On a slide, `Manim` passes the
    slide palette; every click is one 0.25 s ease-out entrance, like
    `FlowAnimation`.

    Stages rendered in sequence:
    1. Raw node appears
    2. Validate node + arrow
    3. Two parallel branches (Transform A / Transform B)
    4. Join node merging both branches
    5. Load node + final arrow
    6. Status labels appear on each node

    Args:
        palette: Colors of the scene: stages cycle `section_colors` (else
            `primary` and `secondary`), names use `text`, sublabels and arrows
            `muted`. `None` uses the default `Palette()`. The background is
            set by `Manim` (`palette.panel`).

    Returns:
        A `Scene` subclass with 7 sections: the title and 6 stages.

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
            DOWN,
            LEFT,
            ORIGIN,
            RIGHT,
            UP,
            Arrow,
            FadeIn,
            GrowArrow,
            RoundedRectangle,
            Scene,
            Text,
            VGroup,
            rate_functions,
        )
    except ImportError as e:
        raise ImportError("manim is required. Run: uv pip install 'marimo-banners[manim]'") from e

    from banners.content.flow_animation import SHIFT, STEP_TIME, node_colors
    from banners.palette import Palette

    pal = palette or Palette()
    raw_c, val_c, tr_c, join_c, load_c = node_colors(pal, 5)

    def make_node(label: str, sublabel: str, color, width=2.4, height=0.75):
        """Build one stage: a tinted rounded box with its name and sublabel."""
        box = RoundedRectangle(
            corner_radius=0.12, width=width, height=height,
            fill_color=color, fill_opacity=0.15,
            stroke_color=color, stroke_width=2.5,
        )
        txt = Text(label, font_size=22, color=pal.text, weight="BOLD")
        sub = Text(sublabel, font_size=14, color=pal.muted)
        sub.next_to(txt, DOWN, buff=0.05)
        group = VGroup(box, VGroup(txt, sub).move_to(box))
        group.move_to(ORIGIN)
        return group

    def arrow(start, end):
        """Connector between two stages."""
        return Arrow(start, end, buff=0.1, color=pal.muted, stroke_width=2)

    class _PipelineScene(Scene):
        def step(self, *animations):
            """Play one click: a single short ease-out animation group."""
            self.play(*animations, run_time=STEP_TIME, rate_func=rate_functions.ease_out_cubic)

        def construct(self):
            title = Text("Data Pipeline", font_size=32, color=pal.primary, weight="BOLD")
            title.to_edge(UP, buff=0.3)
            self.step(FadeIn(title, shift=DOWN * SHIFT))

            self.next_section("raw")
            raw = make_node("Raw Data", "S3 bucket", raw_c).shift(LEFT * 4.5)
            self.step(FadeIn(raw, shift=RIGHT * SHIFT))

            self.next_section("validate")
            val = make_node("Validate", "schema + nulls", val_c).shift(LEFT * 1.8)
            self.step(FadeIn(val, shift=RIGHT * SHIFT), GrowArrow(arrow(raw.get_right(), val.get_left())))

            self.next_section("branches")
            tr_a = make_node("Transform A", "feature eng.", tr_c, width=2.6).shift(RIGHT * 0.9 + UP * 1.1)
            tr_b = make_node("Transform B", "outlier filter", tr_c, width=2.6).shift(RIGHT * 0.9 + DOWN * 1.1)
            self.step(
                FadeIn(VGroup(tr_a, tr_b), shift=RIGHT * SHIFT),
                GrowArrow(arrow(val.get_right(), tr_a.get_left())),
                GrowArrow(arrow(val.get_right(), tr_b.get_left())),
            )

            self.next_section("join")
            join = make_node("Join", "concat + dedup", join_c).shift(RIGHT * 3.6)
            self.step(
                FadeIn(join, shift=RIGHT * SHIFT),
                GrowArrow(arrow(tr_a.get_right(), join.get_left())),
                GrowArrow(arrow(tr_b.get_right(), join.get_left())),
            )

            self.next_section("load")
            load = make_node("Load", "Athena table", load_c).shift(RIGHT * 5.8)
            self.step(FadeIn(load, shift=RIGHT * SHIFT), GrowArrow(arrow(join.get_right(), load.get_left())))

            self.next_section("status")
            checks = VGroup(*[
                Text("✓", font_size=18, color=pal.primary).next_to(node, UP, buff=0.08)
                for node in (raw, val, tr_a, tr_b, join, load)
            ])
            self.step(FadeIn(checks, shift=UP * SHIFT))

    return _PipelineScene
