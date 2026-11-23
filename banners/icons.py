"""Minimal line icons for templates.

A small set of original, single-stroke icons drawn on a 24×24 grid. They are
returned as `data:` URIs, so they work anywhere an image source is accepted
(`Template.mark`, `Template.divider_icon`, `icon=`) without network access.

```python
from banners.icons import icon, ICONS

icon("chart", color="#1f2933")      # data:image/svg+xml;… URI
sorted(ICONS)                        # available names
```
"""

from __future__ import annotations

from urllib.parse import quote

ICONS: dict[str, str] = {
    "chart": '<path d="M3 20h18M5 20v-8M10 20V5M15 20v-6M20 20V9"/>',
    "layers": '<path d="M12 3l9 5-9 5-9-5 9-5z"/><path d="M3 13l9 5 9-5"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5 5-2z"/>',
    "spark": '<path d="M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2L12 3z"/>',
    "leaf": '<path d="M5 19C5 11 11 5 19 5c0 8-6 14-14 14z"/><path d="M5 19l8-8"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
    "shield": '<path d="M12 3l7 3v5c0 5-3 8.5-7 10-4-1.5-7-5-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/>',
    "grid": '<rect x="4" y="4" width="6" height="6"/><rect x="14" y="4" width="6" height="6"/>'
            '<rect x="4" y="14" width="6" height="6"/><rect x="14" y="14" width="6" height="6"/>',
    "orbit": '<circle cx="12" cy="12" r="2.5"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(-25 12 12)"/>',
    "pulse": '<path d="M3 12h4l3-7 4 14 3-7h4"/>',
    "building": '<path d="M3 10l9-6 9 6M5 10v10M19 10v10M9 20v-7M15 20v-7M3 20h18"/>',
    "flow": '<circle cx="5" cy="12" r="2"/><circle cx="19" cy="6" r="2"/><circle cx="19" cy="18" r="2"/>'
            '<path d="M7 12h4l6-6M11 12l6 6"/>',
    "mountain": '<path d="M3 20l6-10 4 6 3-4 5 8H3z"/>',
}
"""Icon name → SVG body (paths on a 24×24 grid, stroked, no fill)."""


def icon(name: str, color: str = "#111827", stroke: float = 1.6) -> str:
    """Return a line icon as an SVG `data:` URI.

    Args:
        name: One of `ICONS`.
        color: Stroke color.
        stroke: Stroke width on the 24×24 grid.

    Returns:
        A `data:image/svg+xml` URI usable as an image source.

    Raises:
        KeyError: If `name` is not in `ICONS`.
    """
    body = ICONS[name]
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
        f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">'
        f"{body}</svg>"
    )
    return "data:image/svg+xml;utf8," + quote(svg)
