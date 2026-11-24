"""Tests for icons, template extensions and built-in presets."""

from dataclasses import replace
from urllib.parse import quote

import pytest

from banners import Template, configure
from banners.content import Text
from banners.icons import ICONS, icon
from banners.slides import Closing, Cover, Section
from banners.template import PRESETS
from banners.theme import Theme


def html(slide) -> str:
    """Render a slide with the active template and return its HTML.

    Args:
        slide: Any slide (`Cover`, `Section`, `Intro`, `Closing`).

    Returns:
        The HTML string of the rendered slide.
    """
    return slide.render().text


@pytest.mark.parametrize("name", sorted(ICONS))
def test_icons_are_colored_svg_data_uris(name):
    uri = icon(name, color="#123456")
    assert uri.startswith("data:image/svg+xml")
    assert "%23123456" in uri


def test_unknown_icon_raises():
    with pytest.raises(KeyError):
        icon("nope")


@pytest.mark.parametrize("name", sorted(PRESETS))
def test_every_preset_renders_all_layouts(name):
    configure(template=PRESETS[name], team="T", date="D")
    for slide in (Cover(title="A"), Section(title="B"), Section(title="C", content=[Text("x"), Text("y")])):
        assert "aspect-ratio:16/9" in html(slide)


def test_presets_link_only_public_urls_or_inline_icons():
    for t in PRESETS.values():
        for field in ("cover_image", "divider_image", "logo_on_light", "logo_on_dark", "mark", "closing_image"):
            value = getattr(t, field)
            assert value is None or value in ICONS or str(value).startswith("https://commons.wikimedia.org/")


def test_bar_colors_draw_equal_segments():
    configure(template=Template(bar_colors=("#111111", "#222222", "#333333")))
    out = html(Cover(title="A"))
    assert all(f"background:{c}" in out for c in ("#111111", "#222222", "#333333"))


def test_section_colors_cycle_by_number():
    configure(template=Template(section_colors=("#aa0000", "#0000aa"), light="#ffffff", auto_contrast=False))
    first, second = Section(title="One"), Section(title="Two")
    assert "color:#aa0000" in html(first) and "color:#0000aa" in html(second)


def test_default_cover_image_and_divider_icon():
    configure(template=Template(cover_image="https://example.org/a.jpg", divider_icon="leaf"))
    assert "https://example.org/a.jpg" in html(Cover(title="A"))
    assert "data:image/svg+xml" in html(Section(title="B"))


def test_auto_contrast_swaps_unreadable_title_color():
    t = Template(primary="#222222", dark="#222222", on_dark="#fafafa")
    assert t._on(t.dark, t.primary) == "#fafafa"
    assert Template(primary="#222222", dark="#222222", auto_contrast=False)._on("#222222", "#222222") == "#222222"


def test_heading_font_applies_to_titles_only():
    configure(template=Template(theme=Theme(heading_font="Georgia, serif")))
    out = html(Section(title="T", content=Text("body")))
    # The slide has a single title: the font appears once and does not leak into the body.
    assert out.count("font-family:Georgia, serif") == 1


@pytest.mark.parametrize("name", ["EXECUTIVE", "INSTITUTIONAL"])
def test_closing_stats_and_icon_contrast_with_closing_bg(name):
    t = PRESETS[name]
    configure(template=replace(t, closing_image="chart"))
    out = html(Closing(title="Gracias", stats=[("42%", "Ahorro", "2026")]))
    assert f"color:{t.primary};\">42%" not in out
    assert quote(f'stroke="{t.primary}"') not in out


def test_icon_mark_does_not_clip_white_logo():
    configure(template=Template(logo_on_light="https://example.org/logo.svg", mark="chart"))
    out = html(Cover(title="A"))
    assert "clip-path" not in out


def test_image_false_disables_preset_photo():
    configure(template=Template(cover_image="https://example.org/a.jpg",
                                divider_image="https://example.org/b.jpg"))
    assert "https://example.org/a.jpg" not in html(Cover(title="A", image=False))
    assert "https://example.org/b.jpg" not in html(Section(title="B", image=False))


def test_divider_icon_follows_title_contrast():
    configure(template=Template(primary="#f5f5f5", light="#ffffff", divider_icon="layers"))
    out = html(Section(title="B"))
    assert quote('stroke="#f5f5f5"') not in out


def test_section_with_content_and_image_false_uses_column_layout():
    configure(template=Template())
    out = html(Section(title="B", content=[Text("x"), Text("y")], image=False))
    assert "background:url(" not in out


def test_presets_and_icons_are_exported():
    import banners

    for name in ("BECH", "EXECUTIVE", "INSTITUTIONAL", "COSMOS", "VIBRANT", "TERRA", "PRESETS", "icon", "ICONS"):
        assert name in banners.__all__ and hasattr(banners, name)
