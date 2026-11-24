"""Content elements for slides.

Available classes:
    Text   — Markdown text.
    Image  — Image from a path, bytes or URL.
    Graph  — Mermaid diagram.
    Table  — Table from a pandas DataFrame.
    Plot   — matplotlib or plotly figure.
    Manim  — Animation rendered with Manim (requires `marimo-banners[manim]`).
"""

from .animated_graph import AnimatedGraph
from .flow_animation import FlowAnimation
from .graph import Graph
from .image import Image
from .manim import Manim
from .plot import Plot
from .table import Table
from .text import Text

__all__ = ["Text", "Image", "Graph", "AnimatedGraph", "Table", "Plot", "Manim", "FlowAnimation"]
