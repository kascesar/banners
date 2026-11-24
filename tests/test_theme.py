"""Tests for `Theme` (fonts, title weight, icon stroke and scale) and its use in `Template`."""

from urllib.parse import quote

from banners import Template, configure
from banners.slides import Cover, Section
from banners.theme import Theme


def html(slide) -> str:
    """Render a slide with the active template and return its HTML.

    Args:
        slide: Any slide (`Cover`, `Section`, `Intro`, `Closing`).

    Returns:
        The HTML string of the rendered slide.
    """
    return slide.render().text


def test_theme_defaults():
    """A default `Theme` has no heading font, bold titles, 1.6 icon stroke and scale 1."""
    t = Theme()
    assert t.heading_font is None
    assert t.title_weight == 700
    assert t.icon_stroke == 1.6
    assert t.scale == 1.0


def test_title_weight_applies_to_titles():
    """`title_weight` sets the font weight of slide titles."""
    configure(template=Template(theme=Theme(title_weight=600)))
    assert "font-weight:600" in html(Cover(title="A"))


def test_icon_stroke_reaches_named_icons():
    """`icon_stroke` sets the stroke width of named line icons."""
    configure(template=Template(theme=Theme(icon_stroke=2.5), divider_icon="leaf"))
    assert quote('stroke-width="2.5"') in html(Section(title="B"))


def test_theme_scale_multiplies_sizes():
    """`scale` multiplies every font size of the canvas."""
    t = Template(theme=Theme(scale=2))
    assert t._fs("body") == f"{1.77 * 2:.3f}cqw"
