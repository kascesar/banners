"""Módulo de contenido para slides.

Clases disponibles:
    Text   — Texto en Markdown.
    Image  — Imagen desde path, bytes o URL.
    Graph  — Diagrama Mermaid.
    Table  — Tabla desde un pandas DataFrame.
    Plot   — Figura de matplotlib o plotly.
    Manim  — Animación renderizada con Manim (requiere `banners[manim]`).
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
