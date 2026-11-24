"""Color palettes for slide banners."""

from dataclasses import dataclass


@dataclass
class Palette:
    """Color palette for slides.

    `start` is the solid panel color used by `Cover` and `Closing`; `end` is
    the accent used sparingly for rules, section numbers and kickers. `mid`
    is only used by the `gradient` property, kept for custom backgrounds.

    Attributes:
        start: Panel color (hex), a deep, low-saturation tone.
        mid: Secondary panel tone (hex), used by `gradient`.
        end: Accent color (hex).
        text_main: Primary text color on the banner.
        text_sub: Subtitle text color.
        text_muted: Muted text color (dates, captions).
        text_tag: Small-caps tag/team line color.

    Example:
        ```python
        from banners.palette import Palette, BLUE

        # Use a predefined palette
        Cover(title="My Project", palette=BLUE).render()

        # Build a custom palette
        custom = Palette(start="#0f172a", mid="#1e40af", end="#3b82f6")
        Cover(title="My Project", palette=custom).render()
        ```
    """

    start: str = "#2a1810"
    mid: str = "#3d2216"
    end: str = "#c4561b"

    text_main: str = "#ffffff"
    text_sub: str = "#d6d3d1"
    text_muted: str = "#a8a29e"
    text_tag: str = "#a8a29e"

    @property
    def gradient(self) -> str:
        """CSS linear-gradient string built from start, mid and end stops."""
        return f"linear-gradient(135deg, {self.start} 0%, {self.mid} 50%, {self.end} 100%)"


# ── Predefined palettes ───────────────────────────────────────────────────────
# Deep, desaturated panel tones with one restrained accent each.

ORANGE = Palette()
"""Default palette — dark umber panel, burnt-orange accent."""

BLUE = Palette(start="#0f2340", mid="#16325c", end="#2f6fd0",
               text_sub="#cbd5e1", text_muted="#94a3b8", text_tag="#94a3b8")
"""Navy panel, mid-blue accent."""

GREEN = Palette(start="#0f2a1f", mid="#173d2d", end="#2e8b57",
                text_sub="#cfd8d3", text_muted="#94a89c", text_tag="#94a89c")
"""Dark forest panel, green accent."""

PURPLE = Palette(start="#221a3a", mid="#2e2450", end="#6e56cf",
                 text_sub="#d4d0e0", text_muted="#a09ab8", text_tag="#a09ab8")
"""Deep aubergine panel, violet accent."""

GRAY = Palette(start="#1a1d21", mid="#2a2e34", end="#5b6470",
               text_sub="#d1d5db", text_muted="#9ca3af", text_tag="#9ca3af")
"""Graphite panel, slate accent."""
