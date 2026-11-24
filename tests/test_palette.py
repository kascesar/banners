"""Tests for palettes (`banners.palette`)."""

import pytest

from banners.palette import BLUE, GRAY, GREEN, ORANGE, PURPLE, Palette


def test_gradient_uses_three_stops():
    """`Palette.gradient` builds a linear-gradient with start, mid and end."""
    p = Palette(start="#000000", mid="#111111", end="#222222")
    assert p.gradient == "linear-gradient(135deg, #000000 0%, #111111 50%, #222222 100%)"


@pytest.mark.parametrize("preset", [ORANGE, BLUE, GREEN, PURPLE, GRAY])
def test_presets_are_palettes(preset):
    """The five predefined palettes exist."""
    assert isinstance(preset, Palette)
