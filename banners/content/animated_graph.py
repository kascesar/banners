"""AnimatedGraph — interactive mermaid diagram with click-to-highlight nodes."""

import uuid

import marimo as mo


class AnimatedGraph:
    """Interactive Mermaid diagram where nodes highlight on click.

    Uses the same Mermaid syntax as `Graph` but renders an interactive SVG.
    Clicking any node toggles its highlight. Uses marimo's bundled mermaid —
    no extra dependencies or large assets.

    Args:
        diagram: Mermaid diagram source (same syntax as `Graph`).
        highlight_color: CSS color applied to highlighted nodes.
            Defaults to `"#ea580c"`.

    Example:
        ```python
        from banners.content import AnimatedGraph

        AnimatedGraph(\"\"\"
        graph LR
        A[Ingest] --> B[Validate]
        B --> C[Transform]
        B --> D[Enrich]
        C --> E[Load]
        D --> E
        \"\"\")
        ```
    """

    def __init__(
        self,
        diagram: str,
        highlight_color: str = "#ea580c",
    ) -> None:
        self.diagram = diagram
        self.highlight_color = highlight_color

    def render(self) -> mo.Html:
        """Render the interactive diagram as a marimo HTML component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        uid = uuid.uuid4().hex[:10]
        mermaid_html = mo.mermaid(self.diagram).text
        color = self.highlight_color

        # Small polling script (~500 bytes) that waits for marimo to render
        # the SVG and then attaches click handlers to each .node element.
        poll_script = f"""<script>
(function() {{
    var COLOR = "{color}";
    var tries = 0;
    function attach() {{
        tries++;
        if (tries > 150) return;
        var wrapper = document.getElementById("ag-{uid}");
        if (!wrapper) {{ setTimeout(attach, 100); return; }}
        var nodes = wrapper.querySelectorAll(".node");
        if (!nodes.length) {{ setTimeout(attach, 100); return; }}
        nodes.forEach(function(n) {{
            if (n.dataset.ag) return;
            n.dataset.ag = "1";
            n.style.cursor = "pointer";
            n.addEventListener("click", function() {{
                var s = n.querySelector("rect,circle,polygon,ellipse");
                if (!s) return;
                if (n.dataset.hl === "1") {{
                    s.style.fill = ""; s.style.filter = "";
                    n.dataset.hl = "0";
                }} else {{
                    s.style.fill = COLOR; s.style.filter = "brightness(1.2)";
                    n.dataset.hl = "1";
                }}
            }});
        }});
    }}
    setTimeout(attach, 300);
}})();
</script>"""

        return mo.Html(
            f'<div id="ag-{uid}">{mermaid_html}</div>{poll_script}'
        )
