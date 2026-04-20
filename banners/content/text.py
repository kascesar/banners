"""Text content element."""

import marimo as mo


class Text:
    """Markdown text element for use inside a slide's content area.

    Renders using marimo's `mo.md`, so the full Markdown spec is supported:
    paragraphs, **bold**, *italic*, lists, tables, code blocks, etc.

    Args:
        body: Markdown string to render.

    Example:
        ```python
        from banners.content import Text

        Text("**Key finding** — The model improved accuracy by 12 pp.")
        Text(\"\"\"
        | Metric | Value |
        |--------|-------|
        | AUC    | 0.91  |
        | F1     | 0.87  |
        \"\"\")
        ```
    """

    def __init__(self, body: str) -> None:
        self.body = body

    def render(self) -> mo.Html:
        """Render the Markdown body as a marimo HTML component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        return mo.md(self.body)
