"""FlowAnimation -- click-to-advance pipeline animation built on top of Manim."""

from .manim import Manim

_COLORS = [
    "#3b82f6", "#8b5cf6", "#f59e0b",
    "#10b981", "#ef4444", "#ec4899", "#06b6d4",
]


def _norm(node):
    """Normalise a node spec to {name, detail}."""
    if isinstance(node, str):
        return {"name": node, "detail": ""}
    return {"name": node.get("name", ""), "detail": node.get("detail", "")}


class FlowAnimation:
    """Step-by-step pipeline animation with optional detail text.

    Delegates all rendering to ``Manim``. Requires the optional ``manim``
    dependency.

    Three input formats are supported:

    **Flat list** -- linear chain::

        FlowAnimation(["S3", "Glue", "Athena"])

        FlowAnimation([
            {"name": "S3",   "detail": "raw data"},
            {"name": "Glue", "detail": "ETL job"},
        ])

    **Nested list** -- multi-row layered layout (each outer item is a layer;
    every node in layer *i* connects to every node in layer *i+1*)::

        FlowAnimation([
            ["Ingest"],
            [{"name": "Transform A", "detail": "features"},
             {"name": "Transform B", "detail": "filters"}],
            ["Load"],
        ])

    **Explicit graph** -- arbitrary connections via ``edges``::

        FlowAnimation(
            nodes=["A", "B", "C", "D", "E"],
            edges=[
                ("A", "C"), ("A", "D"),
                ("B", "D"), ("B", "E"),
            ],
        )

    Args:
        nodes: Node list -- ``str``, ``{"name", "detail"}`` dicts, or a
            nested list of those for the multi-layer format.
        edges: Optional list of ``(source_name, target_name)`` tuples. When
            provided the flat/nested-list layout is replaced by an automatic
            BFS layout that respects the given connections.
        direction: Flow direction -- ``"LR"`` (left-to-right) or ``"TD"``
            (top-down). Defaults to ``"LR"`` for flat lists and graph mode,
            ``"TD"`` for nested lists.
        quality: Render quality -- ``"low"``, ``"medium"``, or ``"high"``.
        width: Max width of the player widget. Any CSS value (``"800px"``,
            ``"60%"``, ``"100%"``). Defaults to ``"100%"``.
    """

    def __init__(
        self,
        nodes: list,
        edges=None,
        direction: str = None,
        quality: str = "low",
        width: str = "100%",
        autoplay: bool = False,
    ) -> None:
        self.quality = quality
        self.width = width
        self.autoplay = autoplay
        self._cached = None

        if edges is not None:
            self._mode = "graph"
            self._node_specs = {}
            for n in nodes:
                spec = _norm(n)
                self._node_specs[spec["name"]] = spec
            self._edges = list(edges)
        elif nodes and isinstance(nodes[0], list):
            self._mode = "vertical"
            self._rows = [[_norm(n) for n in row] for row in nodes]
        else:
            self._mode = "horizontal"
            self._rows = [[_norm(n)] for n in nodes]

        # Default direction: preserve current behaviour for each mode
        if direction is None:
            self._direction = "TD" if self._mode == "vertical" else "LR"
        else:
            self._direction = direction.upper()

    def render(self):
        """Build the scene and delegate rendering to Manim."""
        if self._cached is not None:
            return self._cached
        self._cached = Manim(
            self._build_scene(), interactive=True, quality=self.quality, width=self.width, autoplay=self.autoplay
        ).render()
        return self._cached

    # ------------------------------------------------------------------
    # Scene builder dispatcher
    # ------------------------------------------------------------------

    def _build_scene(self):
        if self._mode == "graph":
            return self._build_graph_scene()
        return self._build_rows_scene()

    # ------------------------------------------------------------------
    # Rows scene (horizontal + vertical modes, LR + TD directions)
    # ------------------------------------------------------------------

    def _build_rows_scene(self):
        rows      = self._rows
        direction = self._direction     # "LR" | "TD"
        n_rows    = len(rows)
        max_cols  = max(len(r) for r in rows) if rows else 1
        has_any_detail = any(n["detail"] for r in rows for n in r)

        # Sequential color assignment
        k = 0
        node_colors = []
        for row in rows:
            rc = []
            for _ in row:
                rc.append(_COLORS[k % len(_COLORS)])
                k += 1
            node_colors.append(rc)

        # Geometry -- layer_sp: spacing between layers, node_sp: within a layer
        if direction == "LR":
            layer_sp = min(3.2, 12.0 / max(n_rows, 1))
            node_sp  = min(2.0,  7.0 / max(max_cols, 1))
            node_w   = layer_sp * 0.72
        else:  # TD
            layer_sp = min(2.4,  7.0 / max(n_rows, 1))
            node_sp  = min(3.2, 12.0 / max(max_cols, 1))
            node_w   = node_sp * 0.72

        node_h  = 1.2 if has_any_detail else 0.85
        name_sz = max(12, min(20, int(node_w * 7.0)))
        det_sz  = max(9,  min(13, int(node_w * 5.5)))

        try:
            from manim import (
                Scene, RoundedRectangle, Arrow,
                Write, FadeIn, GrowArrow,
                GRAY as MG, Text as MText, UP,
            )
        except ImportError:
            return None

        class _FlowScene(Scene):
            BG = "#0f172a"

            def construct(self):
                self.camera.background_color = self.BG

                boxes    = {}
                name_lbl = {}
                det_lbl  = {}
                arrows   = {}

                for r, row in enumerate(rows):
                    for c, node in enumerate(row):
                        color = node_colors[r][c]

                        if direction == "LR":
                            x = (r - (n_rows - 1) / 2.0) * layer_sp
                            y = ((len(row) - 1) / 2.0 - c) * node_sp
                        else:  # TD
                            y = ((n_rows - 1) / 2.0 - r) * layer_sp
                            x = (c - (len(row) - 1) / 2.0) * node_sp

                        rect = RoundedRectangle(
                            width=node_w, height=node_h, corner_radius=0.12,
                            fill_color=color, fill_opacity=0.2,
                            stroke_color=color, stroke_width=2,
                        ).move_to([x, y, 0])

                        lbl = MText(node["name"], font_size=name_sz,
                                    color=color, weight="BOLD")

                        det = None
                        if node["detail"]:
                            det = MText(node["detail"], font_size=det_sz,
                                        color="#9ca3af")
                            lbl.move_to(rect.get_center() + UP * (node_h * 0.22))
                            det.move_to(rect.get_center() - UP * (node_h * 0.22))
                        else:
                            lbl.move_to(rect)

                        boxes[(r, c)]    = rect
                        name_lbl[(r, c)] = lbl
                        det_lbl[(r, c)]  = det

                        inc = []
                        if r > 0:
                            for pc in range(len(rows[r - 1])):
                                pb = boxes.get((r - 1, pc))
                                if pb is None:
                                    continue
                                if direction == "LR":
                                    start, end = pb.get_right(), rect.get_left()
                                else:
                                    start, end = pb.get_bottom(), rect.get_top()
                                inc.append(Arrow(
                                    start, end,
                                    buff=0.06, color=MG, stroke_width=2,
                                    tip_length=0.15,
                                ))
                        arrows[(r, c)] = inc

                for r, row in enumerate(rows):
                    for c in range(len(row)):
                        self.next_section(f"step_{r}_{c}")
                        anims = [FadeIn(boxes[(r, c)], scale=0.85),
                                 Write(name_lbl[(r, c)])]
                        if det_lbl.get((r, c)) is not None:
                            anims.append(FadeIn(det_lbl[(r, c)]))
                        grow = [GrowArrow(a) for a in arrows.get((r, c), [])]
                        self.play(*(grow + anims), run_time=0.5)
                        self.wait(0.2)

        return _FlowScene

    # ------------------------------------------------------------------
    # Graph scene (explicit edges, BFS layout, LR + TD directions)
    # ------------------------------------------------------------------

    def _build_graph_scene(self):
        node_specs = self._node_specs   # name -> {name, detail}
        edges      = self._edges        # list of (src, dst)
        direction  = self._direction    # "LR" | "TD"

        # Adjacency
        succ = {}
        pred = {}
        for name in node_specs:
            succ[name] = []
            pred[name] = []
        for s, d in edges:
            succ.setdefault(s, []).append(d)
            pred.setdefault(d, []).append(s)

        # BFS level assignment
        roots = [n for n in node_specs if not pred.get(n)]
        if not roots:
            roots = [next(iter(node_specs))]

        levels = {n: 0 for n in roots}
        queue  = list(roots)
        guard  = len(node_specs)
        while queue:
            n = queue.pop(0)
            for nb in succ.get(n, []):
                lv = levels[n] + 1
                if lv > guard:
                    continue
                if nb not in levels or levels[nb] < lv:
                    levels[nb] = lv
                    queue.append(nb)
        for n in node_specs:
            if n not in levels:
                levels[n] = 0

        n_levels = max(levels.values()) + 1
        by_level = {lv: [] for lv in range(n_levels)}
        for name in node_specs:           # preserve insertion order
            by_level[levels[name]].append(name)

        max_per_level  = max(len(v) for v in by_level.values())
        has_any_detail = any(node_specs[n]["detail"] for n in node_specs)

        # Geometry
        if direction == "LR":
            col_sp = min(3.2, 12.0 / max(n_levels, 1))
            row_sp = min(2.0,  7.0 / max(max_per_level, 1))
            node_w = col_sp * 0.72
        else:  # TD
            col_sp = min(2.4,  7.0 / max(n_levels, 1))
            row_sp = min(3.2, 12.0 / max(max_per_level, 1))
            node_w = row_sp * 0.72

        node_h  = 1.15 if has_any_detail else 0.85
        name_sz = max(12, min(20, int(node_w * 7.0)))
        det_sz  = max(9,  min(13, int(node_w * 5.5)))

        # Positions
        positions = {}
        for lv in range(n_levels):
            names_lv = by_level[lv]
            for i, name in enumerate(names_lv):
                if direction == "LR":
                    x = (lv - (n_levels - 1) / 2.0) * col_sp
                    y = ((len(names_lv) - 1) / 2.0 - i) * row_sp
                else:  # TD
                    y = ((n_levels - 1) / 2.0 - lv) * col_sp
                    x = (i - (len(names_lv) - 1) / 2.0) * row_sp
                positions[name] = (x, y)

        # Colors
        k = 0
        node_colors = {}
        for lv in range(n_levels):
            for name in by_level[lv]:
                node_colors[name] = _COLORS[k % len(_COLORS)]
                k += 1

        # Animation order: level by level
        anim_order = [name for lv in range(n_levels) for name in by_level[lv]]

        try:
            from manim import (
                Scene, RoundedRectangle, Arrow,
                Write, FadeIn, GrowArrow,
                GRAY as MG, Text as MText, UP,
            )
        except ImportError:
            return None

        class _FlowScene(Scene):
            BG = "#0f172a"

            def construct(self):
                self.camera.background_color = self.BG

                boxes    = {}
                name_lbl = {}
                det_lbl  = {}
                arrows   = {}

                for name, spec in node_specs.items():
                    x, y  = positions[name]
                    color = node_colors[name]

                    rect = RoundedRectangle(
                        width=node_w, height=node_h, corner_radius=0.12,
                        fill_color=color, fill_opacity=0.2,
                        stroke_color=color, stroke_width=2,
                    ).move_to([x, y, 0])

                    lbl = MText(spec["name"], font_size=name_sz,
                                color=color, weight="BOLD")

                    det = None
                    if spec["detail"]:
                        det = MText(spec["detail"], font_size=det_sz,
                                    color="#9ca3af")
                        lbl.move_to(rect.get_center() + UP * (node_h * 0.22))
                        det.move_to(rect.get_center() - UP * (node_h * 0.22))
                    else:
                        lbl.move_to(rect)

                    boxes[name]    = rect
                    name_lbl[name] = lbl
                    det_lbl[name]  = det

                # Build incoming arrows (direction determined by position delta)
                for name in node_specs:
                    inc = []
                    for src in pred.get(name, []):
                        if src not in boxes:
                            continue
                        sx, sy = positions[src]
                        dx, dy = positions[name]
                        sb = boxes[src]
                        db = boxes[name]
                        if abs(sx - dx) >= abs(sy - dy):
                            start = sb.get_right() if sx < dx else sb.get_left()
                            end   = db.get_left()  if sx < dx else db.get_right()
                        else:
                            start = sb.get_bottom() if sy > dy else sb.get_top()
                            end   = db.get_top()    if sy > dy else db.get_bottom()
                        inc.append(Arrow(
                            start, end,
                            buff=0.06, color=MG, stroke_width=2,
                            tip_length=0.15,
                        ))
                    arrows[name] = inc

                for name in anim_order:
                    self.next_section(f"step_{name}")
                    anims = [FadeIn(boxes[name], scale=0.85),
                             Write(name_lbl[name])]
                    if det_lbl.get(name) is not None:
                        anims.append(FadeIn(det_lbl[name]))
                    grow = [GrowArrow(a) for a in arrows.get(name, [])]
                    self.play(*(grow + anims), run_time=0.5)
                    self.wait(0.2)

        return _FlowScene
