"""Composable slides for marimo presentations.

Every slide is drawn on a fixed 16:9 canvas by a `Template`, which combines
layouts with a `Palette` (colors) and a `Theme` (fonts, title weight, icon
stroke, scale). A palette or theme can also be declared on its own and
replaces the template's one.

```python
from banners import BLUE, TERRA, Closing, Cover, Section, Text, configure

configure(template=TERRA, palette=BLUE, team="Analytics", date="November 2026")

Cover(title="My Project", subtitle="Context in one line.")
Section(title="Results", content=[Text("**Point 1** — Concrete result."), Text("**Point 2** — Team impact.")])
Closing(title="Thank you")
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
from .theme import Theme

__all__ = [
    "configure",
    "Slide",
    "Cover", "Intro", "Section", "Closing",
    "Text", "Image", "Graph", "AnimatedGraph", "Table", "Plot", "Manim", "FlowAnimation",
    "Palette", "ORANGE", "BLUE", "GREEN", "PURPLE", "GRAY",
    "Background",
    "Template", "Theme",
    "BECH", "EXECUTIVE", "INSTITUTIONAL", "COSMOS", "VIBRANT", "TERRA", "PRESETS",
    "icon", "ICONS",
]
