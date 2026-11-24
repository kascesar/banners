"""Tests for palette-aware plots: the template restyles a figure placed on a slide."""

import matplotlib

matplotlib.use("Agg")

import marimo as mo
import matplotlib.pyplot as plt
import pytest
from matplotlib.colors import to_hex

from banners import BLUE, GREEN, Palette, Plot, Section, Template, configure

DEFAULT_C0 = to_hex(plt.rcParams["axes.prop_cycle"].by_key()["color"][0])


def line_figure(**plot_kwargs):
    """Build a figure with one line and a title.

    Args:
        **plot_kwargs: Keyword arguments passed to `Axes.plot`.

    Returns:
        A `(figure, axes)` pair.
    """
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], **plot_kwargs)
    ax.set_title("T")
    return fig, ax


def test_auto_colored_line_takes_palette_primary():
    """A line with matplotlib's automatic color takes the palette primary."""
    fig, _ = line_figure()
    styled = Plot(fig)._with_palette(Palette(primary="#123456"))
    assert to_hex(styled.fig.axes[0].lines[0].get_color()) == "#123456"


def test_hand_colored_line_is_kept():
    """A color set by hand is not replaced."""
    fig, _ = line_figure(color="#abcdef")
    styled = Plot(fig)._with_palette(Palette(primary="#123456"))
    assert to_hex(styled.fig.axes[0].lines[0].get_color()) == "#abcdef"


def test_axes_text_follows_palette():
    """Titles take `palette.text`; tick labels take `palette.muted`."""
    fig, _ = line_figure()
    pal = Palette(text="#111111", muted="#222222")
    ax = Plot(fig)._with_palette(pal).fig.axes[0]
    assert to_hex(ax.title.get_color()) == "#111111"
    assert to_hex(ax.get_xticklabels()[0].get_color()) == "#222222"


def test_original_figure_is_not_modified():
    """Two slides with different palettes get their own colors; the user's figure is untouched."""
    fig, ax = line_figure()
    blue = Plot(fig)._with_palette(BLUE)
    green = Plot(fig)._with_palette(GREEN)
    assert to_hex(ax.lines[0].get_color()) == DEFAULT_C0
    assert to_hex(blue.fig.axes[0].lines[0].get_color()) == BLUE.primary
    assert to_hex(green.fig.axes[0].lines[0].get_color()) == GREEN.primary


def test_standalone_plot_renders_as_today():
    """Outside a slide, a plot renders exactly as `mo.as_html(fig)`."""
    fig, _ = line_figure()
    assert Plot(fig).render().text == mo.as_html(fig).text


def test_template_restyles_plot_on_slide(monkeypatch):
    """The template hands its palette to a plot before rendering it."""
    calls = []
    original = Plot._with_palette

    def spy(self, palette):
        calls.append(palette)
        return original(self, palette)

    monkeypatch.setattr(Plot, "_with_palette", spy)
    pal = Palette(primary="#123456")
    configure(template=Template(palette=pal))
    fig, _ = line_figure()
    Section(title="S", content=Plot(fig)).render()
    assert calls == [pal]


def test_plotly_plot_on_slide_unchanged():
    """A plotly figure is returned as is and still renders on a slide."""
    px = pytest.importorskip("plotly.express")
    fig = px.bar(x=["a", "b"], y=[1, 2])
    plot = Plot(fig)
    assert plot._with_palette(BLUE) is plot
    configure(template=Template())
    assert "aspect-ratio:16/9" in Section(title="S", content=plot).render().text


def test_dark_legend_and_grid_follow_the_palette():
    """A legend box and grid styled for a dark figure stay readable on the panel."""
    fig, ax = line_figure(label="a")
    ax.legend(facecolor="#1f2937", edgecolor="#374151", labelcolor="white")
    ax.grid(color="#1f2937")
    styled_ax = Plot(fig)._with_palette(BLUE).fig.axes[0]
    frame = styled_ax.get_legend().get_frame()
    assert to_hex(frame.get_facecolor()) == BLUE.panel
    assert to_hex(frame.get_edgecolor()) == BLUE.muted
    assert to_hex(styled_ax.get_legend().get_texts()[0].get_color()) == BLUE.text
    assert {to_hex(g.get_color()) for g in styled_ax.get_xgridlines()} == {BLUE.muted}
