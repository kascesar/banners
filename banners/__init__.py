"""Composable slides for marimo presentations.

Build a presentation by combining slide classes with content elements:

```python
from banners.slides import Cover, Intro, Section, Closing
from banners.content import Text, Image, Graph
from banners.palette import Palette, BLUE, GREEN

Cover(
    title="My Project",
    subtitle="Context in one line.",
    date="April 2026",
    content=[
        Text("**Point 1** — Something relevant."),
        Text("**Point 2** — Concrete result."),
        Text("**Point 3** — Team impact."),
    ],
    content_kind="neutral",
).render()
```
"""

from .slide import Slide
from .slides import Cover, Intro, Section, Closing
from .content import Text, Image, Graph, AnimatedGraph, Table, Plot
from .palette import Palette, SectionPalette, ORANGE, BLUE, GREEN, PURPLE, GRAY
from .config import configure

__all__ = [
    "configure",
    "Slide",
    "Cover", "Intro", "Section", "Closing",
    "Text", "Image", "Graph", "AnimatedGraph", "Table", "Plot", "Manim",
    "Palette", "SectionPalette", "ORANGE", "BLUE", "GREEN", "PURPLE", "GRAY",
]
