"""Plot content element — wraps matplotlib or plotly figures."""

import marimo as mo


class Plot:
    """Renders a matplotlib or plotly figure inside a slide.

    Detects the figure type automatically:
    - **matplotlib** `Figure` → `mo.as_html(fig)`
    - **plotly** `Figure` → `mo.ui.plotly(fig)`

    Args:
        fig: A `matplotlib.figure.Figure` or `plotly.graph_objects.Figure`.

    Example:
        ```python
        import matplotlib.pyplot as plt
        from banners.content import Plot

        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        Plot(fig)
        ```
    """

    def __init__(self, fig) -> None:
        self.fig = fig

    def render(self) -> mo.Html:
        """Render the figure as a marimo HTML component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.

        Raises:
            TypeError: If the figure type is not matplotlib or plotly.
        """
        cls_module = type(self.fig).__module__ or ""
        if cls_module.startswith("matplotlib"):
            return mo.as_html(self.fig)
        if cls_module.startswith("plotly"):
            return mo.ui.plotly(self.fig)
        raise TypeError(f"Unsupported figure type: {type(self.fig)}")
