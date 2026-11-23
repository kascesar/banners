"""Mermaid diagram content element."""

import marimo as mo

_THEME = (
    "%%{init: {'theme': 'base', 'themeVariables': {"
    "'primaryColor': '#f3f4f6', 'primaryBorderColor': '#9ca3af', "
    "'primaryTextColor': '#111827', 'lineColor': '#6b7280', "
    "'secondaryColor': '#e5e7eb', 'tertiaryColor': '#ffffff', "
    "'fontSize': '14px'}}}%%"
)
"""Neutral Mermaid theme applied unless the diagram declares its own `%%{init}%%`."""


class Graph:
    """Mermaid diagram element for use inside a slide's content area.

    Wraps marimo's `mo.mermaid`. Supports all standard Mermaid diagram types:
    `graph LR`, `graph TD`, `sequenceDiagram`, `gantt`, `pie`, etc.

    Args:
        diagram: Mermaid diagram definition string.

    Example:
        ```python
        from banners.content import Graph

        Graph('''
        graph LR
            A[Ingest] --> B[Transform]
            B --> C[Model]
            C --> D[Predictions]
        ''')
        ```
    """

    def __init__(self, diagram: str) -> None:
        self.diagram = diagram

    def render(self) -> mo.Html:
        """Render the Mermaid diagram as a marimo HTML component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        diagram = self.diagram
        if "%%{init" not in diagram:
            diagram = _THEME + "\n" + diagram.strip("\n")
        return mo.mermaid(diagram)
