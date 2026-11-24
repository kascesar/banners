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

from .background import Background
from .config import configure
from .content import AnimatedGraph, FlowAnimation, Graph, Image, Manim, Plot, Table, Text
from .icons import ICONS, icon
from .palette import BLUE, GRAY, GREEN, ORANGE, PURPLE, Palette
from .slide import Slide
from .slides import Closing, Cover, Intro, Section
from .template import BECH, COSMOS, EXECUTIVE, INSTITUTIONAL, PRESETS, TERRA, VIBRANT, Template

__all__ = [
    "configure",
    "Slide",
    "Cover", "Intro", "Section", "Closing",
    "Text", "Image", "Graph", "AnimatedGraph", "Table", "Plot", "Manim", "FlowAnimation",
    "Palette", "ORANGE", "BLUE", "GREEN", "PURPLE", "GRAY",
    "Background",
    "Template",
    "BECH", "EXECUTIVE", "INSTITUTIONAL", "COSMOS", "VIBRANT", "TERRA", "PRESETS",
    "icon", "ICONS",
]
