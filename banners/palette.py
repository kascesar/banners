"""Color palettes for slide banners."""

from dataclasses import dataclass


@dataclass
class Palette:
    """Three-stop linear gradient palette for full-banner slides (Cover, Intro, Closing).

    Attributes:
        start: Gradient start color (hex). Default is deep brown-red.
        mid: Gradient mid color (hex).
        end: Gradient end color (hex). Default is bright orange.
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

    start: str = "#7c2d12"
    mid: str = "#c2410c"
    end: str = "#ea580c"

    text_main: str = "#ffffff"
    text_sub: str = "#ffedd5"
    text_muted: str = "#fdba74"
    text_tag: str = "#fed7aa"

    @property
    def gradient(self) -> str:
        """CSS linear-gradient string built from start, mid and end stops."""
        return f"linear-gradient(135deg, {self.start} 0%, {self.mid} 50%, {self.end} 100%)"

    def to_section_palette(self) -> "SectionPalette":
        """Derive a SectionPalette from this palette.

        Uses `end` as the border accent and a darkened `start` for the background.
        """
        def _darken(hex_color: str, factor: float) -> str:
            h = hex_color.lstrip("#")
            r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
            return f"#{int(r * factor):02x}{int(g * factor):02x}{int(b * factor):02x}"

        return SectionPalette(
            border=self.end,
            bg_start=_darken(self.start, 0.30),
            bg_end=_darken(self.start, 0.42),
        )


@dataclass
class SectionPalette:
    """Palette for Section slides: left border accent over a dark background.

    Attributes:
        border: Left-border accent color (hex).
        bg_start: Dark background gradient start color (hex).
        bg_end: Dark background gradient end color (hex).
        text_main: Primary text color.
        text_sub: Subtitle text color.

    Example:
        ```python
        from banners.palette import SectionPalette

        blue_section = SectionPalette(
            border="#3b82f6",
            bg_start="#0f172a",
            bg_end="#1e293b",
        )
        Section(title="Results", palette=blue_section).render()
        ```
    """

    border: str = "#ea580c"
    bg_start: str = "#1c0a00"
    bg_end: str = "#1f1210"

    text_main: str = "#ffffff"
    text_sub: str = "#d1d5db"

    @property
    def gradient(self) -> str:
        """CSS linear-gradient string for the dark background."""
        return f"linear-gradient(90deg, {self.bg_start} 0%, {self.bg_end} 100%)"


# ── Predefined palettes ───────────────────────────────────────────────────────

ORANGE = Palette()
"""Default team palette — deep orange gradient."""

BLUE = Palette(start="#1e3a5f", mid="#1d4ed8", end="#3b82f6")
"""Dark blue gradient."""

GREEN = Palette(start="#14532d", mid="#15803d", end="#22c55e")
"""Dark green gradient."""

PURPLE = Palette(start="#3b0764", mid="#7e22ce", end="#a855f7")
"""Deep purple gradient."""

GRAY = Palette(start="#111827", mid="#374151", end="#6b7280")
"""Dark gray gradient."""
