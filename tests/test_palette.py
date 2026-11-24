"""Tests for palettes (`banners.palette`)."""

import pytest

from banners.palette import BLUE, GRAY, GREEN, ORANGE, PURPLE, Palette, SectionPalette


def test_gradient_uses_three_stops():
    """`Palette.gradient` builds a linear-gradient with start, mid and end."""
    p = Palette(start="#000000", mid="#111111", end="#222222")
    assert p.gradient == "linear-gradient(135deg, #000000 0%, #111111 50%, #222222 100%)"


def test_to_section_palette_darkens_start():
    """`to_section_palette()` uses `end` as the border and darkens `start` for the background."""
    sp = Palette(start="#646464", mid="#000000", end="#abcdef").to_section_palette()
    assert isinstance(sp, SectionPalette)
    assert sp.border == "#abcdef"
    # 0x64 = 100 → 100 * 0.30 = 30 = 0x1e; 100 * 0.42 = 42 = 0x2a
    assert sp.bg_start == "#1e1e1e"
    assert sp.bg_end == "#2a2a2a"


@pytest.mark.parametrize("preset", [ORANGE, BLUE, GREEN, PURPLE, GRAY])
def test_presets_are_palettes_with_valid_section(preset):
    """The five presets exist and derive a `SectionPalette` darker than `start`."""
    assert isinstance(preset, Palette)
    sp = preset.to_section_palette()
    start = int(preset.start[1:3], 16)
    assert int(sp.bg_start[1:3], 16) <= start


def test_section_palette_gradient():
    """`SectionPalette.gradient` builds a horizontal gradient from bg_start to bg_end."""
    sp = SectionPalette(bg_start="#000000", bg_end="#ffffff")
    assert sp.gradient == "linear-gradient(90deg, #000000 0%, #ffffff 100%)"
