"""Tests for backgrounds (`banners.background`): color parsing and text contrast."""

import pytest

from banners.background import Background, _parse_first_color


@pytest.mark.parametrize(
    ("css", "expected"),
    [
        ("white", (255, 255, 255)),
        ("  Navy ", (0, 0, 128)),
        ("#abc", (0xAA, 0xBB, 0xCC)),
        ("#abcd", (0xAA, 0xBB, 0xCC)),
        ("#a1b2c3", (0xA1, 0xB2, 0xC3)),
        ("#a1b2c3ff", (0xA1, 0xB2, 0xC3)),
        ("rgb(10, 20, 30)", (10, 20, 30)),
        ("rgba(10,20,30,0.5)", (10, 20, 30)),
        ("rgb(0.0, 0.5, 1.0)", (0, 127, 255)),
    ],
)
def test_parse_first_color_formats(css, expected):
    """`_parse_first_color` recognizes names, 3/4/6/8-digit hex and rgb()/rgba()."""
    assert _parse_first_color(css) == expected


def test_parse_first_color_gradient_first_wins():
    """In a gradient whose colors share a format, the first one is taken."""
    css = "linear-gradient(135deg,#0f172a 0%,#ffffff 100%)"
    assert _parse_first_color(css) == (0x0F, 0x17, 0x2A)


@pytest.mark.xfail(
    reason="Each format is searched over the whole string in a fixed order (#rrggbb before "
    "#rgb and rgb()), so with mixed formats the first color does not win. See Backlog.",
    strict=True,
)
def test_parse_first_color_gradient_mixed_formats_first_wins():
    """With mixed formats the first color of the gradient should win as well."""
    assert _parse_first_color("linear-gradient(#fff 0%, #000000 100%)") == (255, 255, 255)


@pytest.mark.parametrize("css", ["", "url(foo.png)", "var(--bg)", "not-a-color"])
def test_parse_first_color_unparseable_returns_none(css):
    """A value with no recognizable color returns `None`."""
    assert _parse_first_color(css) is None


@pytest.mark.parametrize("css", ["#000000", "black", "#0f172a", "navy"])
def test_text_color_white_on_dark(css):
    """On a dark background the text is white."""
    assert Background.color(css).text_color() == "#ffffff"


@pytest.mark.parametrize("css", ["#ffffff", "white", "#f3f4f6", "yellow"])
def test_text_color_dark_on_light(css):
    """On a light background the text is dark gray."""
    assert Background.color(css).text_color() == "#1f2937"


def test_text_color_none_when_unparseable():
    """When the color cannot be read, no text color is proposed."""
    assert Background.color("var(--bg)").text_color() is None


def test_gradient_css_with_and_without_mid():
    """`Background.gradient` adds the middle color only when it is given."""
    assert Background.gradient("#000", "#fff").css == "linear-gradient(135deg,#000 0%,#fff 100%)"
    assert (
        Background.gradient("#000", "#fff", mid="#888", angle=45).css
        == "linear-gradient(45deg,#000 0%,#888 50%,#fff 100%)"
    )
