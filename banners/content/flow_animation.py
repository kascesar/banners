"""FlowAnimation — click-to-advance pipeline animation built on top of Manim."""

from .manim import Manim

_COLORS = [
    "#3b82f6", "#8b5cf6", "#f59e0b",
    "#10b981", "#ef4444", "#ec4899", "#06b6d4",
]


class FlowAnimation:
    """Step-by-step pipeline animation — click to reveal each node.

    Each click adds the next node and its connecting arrow.
    Delegates all rendering to `Manim` — no duplicated infrastructure.
    Requires the optional ``manim`` dependency.

    Args:
        nodes: List of stage names, e.g. ``["Ingest", "Transform", "Load"]``.
        quality: Render quality — ``"low"``, ``"medium"``, or ``"high"``.
            Defaults to ``"low"``.

    Example:
        ```python
        from banners.content import FlowAnimation

        FlowAnimation(["S3", "Glue", "Athena", "SageMaker", "Redshift"]).render()
        ```
    """

    def __init__(self, nodes: list[str], quality: str = "low") -> None:
        self.nodes = nodes
        self.quality = quality
        self._cached = None

    def render(self):
        """Build the scene and delegate rendering to Manim."""
        if self._cached is not None:
            return self._cached
        self._cached = Manim(
            self._build_scene(), interactive=True, quality=self.quality
        ).render()
        return self._cached

    def _build_scene(self):
        """Return a Manim Scene class for this flow."""
        nodes  = self.nodes
        colors = [_COLORS[i % len(_COLORS)] for i in range(len(nodes))]
        n      = len(nodes)

        spacing = min(2.8, 11.0 / max(n, 1))
        node_w  = spacing * 0.76
        node_h  = 0.85
        font_sz = max(12, min(20, int(node_w * 10.5)))

        try:
            from manim import (
                Scene, RoundedRectangle, Arrow,
                Write, FadeIn, GrowArrow,
                GRAY as MG, Text as MText,
            )
        except ImportError:
            return None  # Manim.render() handles the missing-dependency callout

        class _FlowScene(Scene):
            BG = "#0f172a"

            def construct(self):
                self.camera.background_color = self.BG

                xs = [(i - (n - 1) / 2) * spacing for i in range(n)]
                boxes, labels, arrows = [], [], []

                for i, (x, name, color) in enumerate(zip(xs, nodes, colors)):
                    rect = RoundedRectangle(
                        width=node_w, height=node_h, corner_radius=0.12,
                        fill_color=color, fill_opacity=0.2,
                        stroke_color=color, stroke_width=2,
                    ).move_to([x, 0, 0])
                    lbl = MText(name, font_size=font_sz, color=color, weight="BOLD")
                    lbl.move_to(rect)
                    boxes.append(rect)
                    labels.append(lbl)
                    if i > 0:
                        arrows.append(Arrow(
                            boxes[i - 1].get_right(), rect.get_left(),
                            buff=0.06, color=MG, stroke_width=2,
                            max_tip_length_to_length_ratio=0.2,
                        ))

                for i in range(n):
                    self.next_section(f"step_{i}")
                    if i == 0:
                        self.play(FadeIn(boxes[0], scale=0.8), Write(labels[0]), run_time=0.5)
                    else:
                        self.play(
                            GrowArrow(arrows[i - 1]),
                            FadeIn(boxes[i], scale=0.8),
                            Write(labels[i]),
                            run_time=0.5,
                        )
                    self.wait(0.2)

        return _FlowScene
