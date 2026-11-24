"""Tests for how a slide picks its palette and theme, and for canvas backgrounds."""

import pytest

from banners import BLUE, Background, Palette, Template, Text, configure
from banners.slides import Closing, Cover, Intro, Section
from banners.template import PRESETS, TERRA, VIBRANT
from banners.theme import Theme

PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


def html(slide) -> str:
    """Render a slide with the active configuration and return its HTML.

    Args:
        slide: Any slide (`Cover`, `Section`, `Intro`, `Closing`).

    Returns:
        The HTML string of the rendered slide.
    """
    return slide.render().text


def test_slide_palette_beats_configure_and_template():
    """A slide palette wins over the configured palette and the template palette."""
    configure(template=Template(palette=Palette(primary="#111111")), palette=Palette(primary="#222222"))
    out = html(Cover(title="A", palette=Palette(primary="#333333")))
    assert "#333333" in out and "#222222" not in out and "#111111" not in out


def test_configure_palette_beats_template():
    """The configured palette wins over the template palette."""
    configure(template=Template(palette=Palette(primary="#111111")), palette=Palette(primary="#222222"))
    out = html(Cover(title="A"))
    assert "#222222" in out and "#111111" not in out


def test_template_palette_is_the_fallback():
    """With no other palette, the template palette is used."""
    configure(template=Template(palette=Palette(primary="#111111")), palette=None)
    assert "#111111" in html(Cover(title="A"))


def test_configure_theme_beats_template():
    """The configured theme wins over the template theme."""
    configure(template=Template(theme=Theme(font="Serif1")), theme=Theme(font="Sans2"))
    out = html(Cover(title="A"))
    assert "font-family:Sans2" in out and "Serif1" not in out


def test_palette_and_theme_work_without_template():
    """A palette and a theme apply on the default template too."""
    configure(template=None, palette=BLUE, theme=Theme(font="X"))
    out = html(Cover(title="A"))
    assert "#2f6fd0" in out and "font-family:X" in out


@pytest.mark.parametrize("name", sorted(PRESETS))
def test_every_preset_with_user_palette(name):
    """Every preset renders all layouts with a user palette."""
    configure(template=PRESETS[name], palette=BLUE, team="T", date="D")
    slides = [
        Cover(title="A"),
        Intro(title="B", content=[Text("x"), Text("y")]),
        Section(title="C"),
        Section(title="D", content=[Text("x"), Text("y")]),
        Closing(title="E", stats=[("1", "a", "b")]),
    ]
    # Each layout shows at least one BLUE color; a title color may be swapped
    # by the contrast check, so any of BLUE's own tones counts.
    blue = (BLUE.primary, BLUE.dark, BLUE.closing_bg)
    for slide in slides:
        out = html(slide)
        assert any(c in out for c in blue), type(slide).__name__


def test_user_palette_drops_preset_section_colors():
    """A user palette without section colors leaves none of the preset's behind."""
    configure(template=VIBRANT, palette=BLUE)
    out = html(Section(title="S"))
    assert not any(c in out for c in VIBRANT.palette.section_colors)


def test_palette_survives_later_template_change():
    """A palette configured before the template still applies."""
    configure(palette=BLUE)
    configure(template=TERRA)
    assert "#2f6fd0" in html(Cover(title="A"))


def test_background_paints_canvas():
    """`background=` paints the canvas and sets a readable text color."""
    configure(template=None)
    out = html(Cover(title="A", background=Background.color("#000000")))
    assert "background:#000000" in out and "color:#ffffff" in out


def test_background_image_makes_text_white():
    """An image background with the default dark overlay makes the text white."""
    configure(template=None)
    out = html(Section(title="A", content=Text("x"), background=Background.image(PNG)))
    assert "url(data:image/png" in out and "#ffffff" in out
