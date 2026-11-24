"""Palette — the colors of a deck, named by the role they play on a slide.

A `Palette` holds only colors. A `Template` holds one palette (its own
default); a palette set with `configure(palette=...)` or on a slide replaces
the template's palette as a whole. The same palette works with any template.

```python
from banners import BLUE, Palette, configure

configure(palette=BLUE)                                  # every slide
custom = Palette(primary="#0f766e", dark="#042f2e", closing_bg="#134e4a")
```
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Palette:
    """Colors of a deck, by role.

    Attributes:
        primary: Title color and main segment of the bottom bar.
        secondary: End segment of the bottom bar.
        dark: Background of the dark cover and of the logo closing slide.
        closing_bg: Background of the closing slide with a title.
        light: Background of dividers and content slides.
        text: Body text color on light backgrounds.
        muted: Labels and subtitles on light backgrounds.
        on_dark: Text color on dark backgrounds.
        panel: Background of the box that holds a chart or visual.
        icon_color: Color of named icons (`mark`, `divider_icon`); `None` uses
            the title color.
        section_colors: Colors cycled by section number for titles and icons
            of `Section` slides; `None` uses `primary` on every section.
        bar_colors: Colors of the bottom bar in equal segments; `None` draws
            `primary` and `secondary` split by `Template.bar_split`.
    """

    primary: str = "#e4572e"
    secondary: str = "#2a6fdb"
    dark: str = "#404040"
    closing_bg: str = "#363e45"
    light: str = "#f5f5f5"
    text: str = "#343e46"
    muted: str = "#6b7280"
    on_dark: str = "#f5f5f5"
    panel: str = "#ffffff"
    icon_color: str | None = None
    section_colors: tuple | None = None
    bar_colors: tuple | None = None


# ── Predefined palettes ───────────────────────────────────────────────────────
# Each one keeps the tones of the 0.4 palette with the same name: its accent
# becomes `primary`, its deepest tone `dark` and its middle tone `closing_bg`.

ORANGE = Palette()
"""Default palette: orange titles, blue accent, graphite dark slides."""

BLUE = Palette(primary="#2f6fd0", dark="#0f2340", closing_bg="#16325c")
"""Mid-blue titles on navy dark slides."""

GREEN = Palette(primary="#2e8b57", dark="#0f2a1f", closing_bg="#173d2d")
"""Green titles on dark forest slides."""

PURPLE = Palette(primary="#6e56cf", dark="#221a3a", closing_bg="#2e2450")
"""Violet titles on deep aubergine slides."""

GRAY = Palette(primary="#5b6470", dark="#1a1d21", closing_bg="#2a2e34")
"""Slate titles on graphite slides."""
