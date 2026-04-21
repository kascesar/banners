"""AnimatedGraph — interactive graph rendered as an anywidget."""

import math
import re
import uuid
from collections import defaultdict

import anywidget
import traitlets
import marimo as mo


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def _parse(diagram: str):
    direction = "LR"
    nodes: dict[str, str] = {}
    edges: list[tuple[str, str, str]] = []

    _ns = (
        r'(?:\[\[?([^\]\)]*?)\]?\]?'
        r'|\(\(?([^\)\]]*?)\)?\)?'
        r'|\{([^\}]*?)\}'
        r'|>([^\]]*?)\]'
        r')?'
    )
    _nid = r'([A-Za-z0-9_]+)'
    _edge_re = re.compile(_nid + _ns + r'\s*-[-\.]+>+(?:\|([^|]*)\|)?\s*' + _nid + _ns)
    _solo_re = re.compile(_nid + _ns + r'\s*$')

    def _label(groups, fallback):
        return next((g for g in groups if g), fallback)

    for raw in diagram.strip().splitlines():
        line = raw.strip()
        if not line or line.startswith("%%"):
            continue
        if line.lower().startswith("graph"):
            parts = line.split()
            if len(parts) > 1:
                direction = parts[1].upper()
            continue
        m = _edge_re.match(line)
        if m:
            src = m.group(1)
            sl  = _label(m.groups()[1:5], src)
            el  = m.group(6) or ""
            dst = m.group(7)
            dl  = _label(m.groups()[7:11], dst)
            if src not in nodes:
                nodes[src] = sl
            if dst not in nodes:
                nodes[dst] = dl
            edges.append((src, dst, el.strip()))
            continue
        m = _solo_re.match(line)
        if m:
            nid   = m.group(1)
            label = _label(m.groups()[1:5], nid)
            if nid not in nodes:
                nodes[nid] = label

    return nodes, edges, direction


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def _layout(nodes, edges, direction, node_w=130, node_h=40, h_gap=70, v_gap=28):
    if not nodes:
        return {}, node_w, node_h

    succ: dict = defaultdict(list)
    pred: dict = defaultdict(list)
    for s, d, _ in edges:
        succ[s].append(d)
        pred[d].append(s)

    roots = [n for n in nodes if not pred[n]] or [next(iter(nodes))]
    levels: dict = {n: 0 for n in roots}
    queue = list(roots)
    max_level = len(nodes)
    while queue:
        n = queue.pop(0)
        for nb in succ[n]:
            lv = levels[n] + 1
            if lv > max_level:
                continue
            if nb not in levels or levels[nb] < lv:
                levels[nb] = lv
                queue.append(nb)
    for n in nodes:
        if n not in levels:
            levels[n] = 0

    by_level: dict = defaultdict(list)
    for n, lv in levels.items():
        by_level[lv].append(n)

    pos: dict = {}
    for lv, nlist in sorted(by_level.items()):
        for i, n in enumerate(nlist):
            if direction in ("LR", "RL"):
                pos[n] = (lv * (node_w + h_gap), i * (node_h + v_gap))
            else:
                pos[n] = (i * (node_w + h_gap), lv * (node_h + v_gap))

    return pos, node_w, node_h


# ---------------------------------------------------------------------------
# SVG builder
# ---------------------------------------------------------------------------

def _build_svg(nodes, edges, pos, node_w, node_h, uid):
    if not pos:
        return "<svg><text y='20'>empty diagram</text></svg>"

    pad = 24
    hw, hh = node_w // 2, node_h // 2
    xs = [x for x, _ in pos.values()]
    ys = [y for _, y in pos.values()]
    svg_w = max(xs) + node_w + pad * 2
    svg_h = max(ys) + node_h + pad * 2

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" '
        f'style="font-family:sans-serif;font-size:13px;overflow:visible;">',
        '<defs>',
        f'  <marker id="arr-{uid}" markerWidth="10" markerHeight="7" '
        f'refX="9" refY="3.5" orient="auto">',
        f'    <polygon points="0 0,10 3.5,0 7" fill="#6b7280"/>',
        '  </marker>',
        '</defs>',
    ]

    for src, dst, label in edges:
        if src not in pos or dst not in pos:
            continue
        x1 = pos[src][0] + pad + hw
        y1 = pos[src][1] + pad + hh
        x2 = pos[dst][0] + pad + hw
        y2 = pos[dst][1] + pad + hh
        angle = math.atan2(y2 - y1, x2 - x1)
        x2 -= int(math.cos(angle) * (hw + 3))
        y2 -= int(math.sin(angle) * (hh + 3))
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#9ca3af" stroke-width="1.5" marker-end="url(#arr-{uid})"/>'
        )
        if label:
            mx, my = (x1 + x2) // 2, (y1 + y2) // 2 - 5
            parts.append(
                f'<text x="{mx}" y="{my}" text-anchor="middle" '
                f'fill="#6b7280" font-size="11">{label}</text>'
            )

    for nid, label in nodes.items():
        if nid not in pos:
            continue
        nx = pos[nid][0] + pad
        ny = pos[nid][1] + pad
        parts.append(
            f'<g class="ag-node" data-hl="0" style="cursor:pointer">'
            f'<rect x="{nx}" y="{ny}" width="{node_w}" height="{node_h}" '
            f'rx="6" fill="#e5e7eb" stroke="#9ca3af" stroke-width="1.5"/>'
            f'<text x="{nx + hw}" y="{ny + hh + 5}" '
            f'text-anchor="middle" fill="#111827">{label}</text>'
            f'</g>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Widget
# ---------------------------------------------------------------------------

class _GraphWidget(anywidget.AnyWidget):
    _esm = """
function render({ model, el }) {
    const color = model.get("color");
    el.innerHTML = model.get("svg");

    el.querySelectorAll(".ag-node").forEach(function(g) {
        g.addEventListener("click", function() {
            const r = g.querySelector("rect");
            const on = g.dataset.hl === "1";
            r.style.fill   = on ? "" : color;
            r.style.filter = on ? "" : "brightness(1.15)";
            g.dataset.hl   = on ? "0" : "1";
        });
    });
}
export default { render };
"""
    _css = """
.ag-node { cursor: pointer; }
"""
    svg   = traitlets.Unicode("").tag(sync=True)
    color = traitlets.Unicode("#ea580c").tag(sync=True)


# ---------------------------------------------------------------------------
# Public class
# ---------------------------------------------------------------------------

class AnimatedGraph:
    """Interactive graph where nodes highlight on click.

    Accepts ``graph LR`` / ``graph TD`` Mermaid syntax. Rendered as an
    anywidget — no external JS libraries, no shadow DOM issues.

    Args:
        diagram: Mermaid ``graph LR`` or ``graph TD`` source.
        highlight_color: CSS color applied to highlighted nodes.
            Defaults to ``"#ea580c"``.

    Example:
        ```python
        from banners.content import AnimatedGraph

        AnimatedGraph(\"\"\"
        graph LR
        A[Ingest] --> B[Validate]
        B --> C[Transform]
        C --> D[Load]
        \"\"\")
        ```
    """

    def __init__(self, diagram: str, highlight_color: str = "#ea580c") -> None:
        self.diagram = diagram
        self.highlight_color = highlight_color

    def render(self):
        """Render the interactive graph as a marimo widget."""
        uid = uuid.uuid4().hex[:8]
        nodes, edges, direction = _parse(self.diagram)
        pos, node_w, node_h = _layout(nodes, edges, direction)
        svg = _build_svg(nodes, edges, pos, node_w, node_h, uid)
        return _GraphWidget(svg=svg, color=self.highlight_color)
