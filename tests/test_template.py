"""Tests for the fixed 16:9 Template renderer."""

import pytest

from banners import Template, configure
from banners.content import Graph, Text
from banners.slides import Closing, Cover, Intro, Section

PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\rIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
)


@pytest.fixture
def tpl():
    t = Template(primary="#ff6600", secondary="#054af6", logo_on_dark=PNG, logo_on_light=PNG, mark=PNG)
    configure(template=t, team="Team", date="Nov 2026")
    return t


def html(slide) -> str:
    return slide.render().text


def test_canvas_is_16_9_with_container_units(tpl):
    out = html(Cover(title="Deck"))
    assert "aspect-ratio:16/9" in out
    assert "container-type:inline-size" in out
    assert "cqw" in out


def test_bar_uses_primary_and_secondary(tpl):
    out = html(Cover(title="Deck"))
    assert "background:#ff6600" in out and "background:#054af6" in out


def test_no_bar_when_disabled():
    configure(template=Template(primary="#ff6600", secondary="#054af6", bar=False))
    assert "background:#054af6" not in html(Cover(title="Deck"))


def test_cover_dark_vs_photo(tpl):
    dark = html(Cover(title="Deck"))
    photo = html(Cover(title="Deck", image=PNG))
    assert f"background:{tpl.dark}" in dark
    assert "center/cover" in photo and "center/cover" not in dark


def test_section_without_content_is_divider(tpl):
    out = html(Section(title="Divider"))
    assert "Divider" in out and tpl._fs("display") in out


def test_section_with_content_uses_title_size(tpl):
    out = html(Section(title="Results", content=[Text("a"), Text("b")]))
    assert tpl._fs("title") in out
    assert "repeat(2,minmax(0,1fr))" in out


def test_section_visual_first_is_split(tpl):
    out = html(Section(title="Chart", content=[Graph("graph LR\n A-->B"), Text("text")]))
    assert "background:#ffffff" in out


def test_intro_and_closing_render(tpl):
    assert "Why" in html(Intro(title="Why", summary="**lead**", content=Text("x")))
    assert "Thanks" in html(Closing(title="Thanks", stats=[("1", "a", "b")]))
    assert "Thanks" not in html(Closing(title=""))


def test_scale_multiplies_font_sizes():
    t = Template(scale=2)
    assert t._fs("body") == f"{1.77 * 2:.3f}cqw"


def test_bad_image_is_omitted(tpl):
    t = Template(logo_on_dark="/does/not/exist.png")
    configure(template=t)
    assert "<img" not in html(Cover(title="Deck"))


def test_configure_none_restores_editorial(tpl):
    configure(template=None)
    assert "aspect-ratio:16/9" not in html(Cover(title="Deck"))
