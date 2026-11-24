"""Tests for palettes (`banners.palette`): colors named by role."""

import pytest

from banners.palette import BLUE, GRAY, GREEN, ORANGE, PURPLE, Palette


def test_orange_is_default_palette():
    """`ORANGE` is the default palette, with an orange primary."""
    assert ORANGE == Palette()
    assert ORANGE.primary == "#e4572e"


@pytest.mark.parametrize(
    ("palette", "primary", "dark", "closing_bg"),
    [
        (BLUE, "#2f6fd0", "#0f2340", "#16325c"),
        (GREEN, "#2e8b57", "#0f2a1f", "#173d2d"),
        (PURPLE, "#6e56cf", "#221a3a", "#2e2450"),
        (GRAY, "#5b6470", "#1a1d21", "#2a2e34"),
    ],
)
def test_presets_by_role(palette, primary, dark, closing_bg):
    """The predefined palettes set primary, dark and closing background from their old tones."""
    assert (palette.primary, palette.dark, palette.closing_bg) == (primary, dark, closing_bg)


def test_palette_has_no_gradient_fields():
    """The 0.4 gradient fields are gone."""
    with pytest.raises(TypeError):
        Palette(start="#000000")
