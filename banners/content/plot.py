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

    def _with_palette(self, palette) -> "Plot":
        """Return a copy of the plot styled with a slide palette.

        The template calls this before placing the plot on a slide. The user's
        figure is never modified: a matplotlib figure is deep-copied and the
        copy is restyled. The figure and axes backgrounds become transparent so
        the template panel shows through; titles, axis labels and legend texts
        take `palette.text`; spines, ticks and grid lines take `palette.muted`;
        the legend box takes `palette.panel` with a `palette.muted` edge. Lines,
        patches and legend handles whose color is one of matplotlib's automatic
        cycle colors (`C0`, `C1`, …) take the palette series
        (`palette.section_colors`, else `primary` and `secondary`); colors set
        by hand are kept. Plotly figures are returned unchanged.

        Args:
            palette: The `banners.Palette` of the slide.

        Returns:
            A new `Plot` with the restyled figure, or `self` for plotly figures.
        """
        if not (type(self.fig).__module__ or "").startswith("matplotlib"):
            return self

        import copy

        import matplotlib.pyplot as plt
        from matplotlib.colors import to_hex, to_rgba

        fig = copy.deepcopy(self.fig)
        cycle = [to_hex(c) for c in plt.rcParams["axes.prop_cycle"].by_key().get("color", [])]
        series = list(palette.section_colors or (palette.primary, palette.secondary))

        def palette_color(color):
            """Map an automatic cycle color to the palette, keeping its alpha."""
            try:
                rgba = to_rgba(color)
            except ValueError:
                return None
            hex_color = to_hex(rgba, keep_alpha=False)
            if hex_color not in cycle:
                return None
            return to_rgba(series[cycle.index(hex_color) % len(series)], alpha=rgba[3])

        fig.patch.set_alpha(0)
        for ax in fig.axes:
            ax.patch.set_alpha(0)
            for line in ax.lines:
                new = palette_color(line.get_color())
                if new is not None:
                    line.set_color(new)
            for patch in ax.patches:
                new = palette_color(patch.get_facecolor())
                if new is not None:
                    patch.set_facecolor(new)
            for text in (ax.title, ax.xaxis.label, ax.yaxis.label):
                text.set_color(palette.text)
            ax.tick_params(colors=palette.muted)
            for spine in ax.spines.values():
                spine.set_edgecolor(palette.muted)
            for grid_line in ax.get_xgridlines() + ax.get_ygridlines():
                grid_line.set_color(palette.muted)
            legend = ax.get_legend()
            if legend is not None:
                legend.get_frame().set_facecolor(palette.panel)
                legend.get_frame().set_edgecolor(palette.muted)
                for text in legend.get_texts():
                    text.set_color(palette.text)
                for handle in legend.legend_handles:
                    getter = getattr(handle, "get_color", None) or getattr(handle, "get_facecolor", None)
                    setter = getattr(handle, "set_color", None) or getattr(handle, "set_facecolor", None)
                    new = palette_color(getter()) if getter else None
                    if new is not None and setter:
                        setter(new)
        return Plot(fig)
