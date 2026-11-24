"""Theme — the visual style of a template that is not color.

A `Theme` groups the typography and drawing style of a deck: body and title
fonts, the weight of titles, the stroke width of line icons and a global size
multiplier. A `Template` holds one theme; colors live in its `Palette`.

```python
from banners import Template, Theme, configure

configure(template=Template(theme=Theme(heading_font="Georgia, serif", title_weight=600)))
```
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Theme:
    """Typography and drawing style of a template.

    Attributes:
        font: CSS font-family stack for every text on the slide.
        heading_font: CSS font-family for titles; `None` uses `font`.
        title_weight: CSS font weight of titles (e.g. 400, 600, 700).
        icon_stroke: Stroke width of the named line icons, on their 24×24 grid.
        scale: Multiplier applied to every font size.
    """

    font: str = "'Century Gothic', 'URW Gothic', 'URW Gothic L', 'Questrial', 'Avenir Next', sans-serif"
    heading_font: str | None = None
    title_weight: int = 700
    icon_stroke: float = 1.6
    scale: float = 1.0
