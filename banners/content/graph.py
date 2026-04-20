"""Mermaid diagram content element."""

import marimo as mo


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
        return mo.mermaid(self.diagram)
