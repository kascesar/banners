"""Módulo de contenido para slides.

Clases disponibles:
    Text   — Texto en Markdown.
    Image  — Imagen desde path, bytes o URL.
    Graph  — Diagrama Mermaid.
    Table  — Tabla desde un pandas DataFrame.
    Plot   — Figura de matplotlib o plotly.
    Manim  — Animación renderizada con Manim (requiere `banners[manim]`).
"""

from .text import Text
from .image import Image
from .graph import Graph
from .animated_graph import AnimatedGraph
from .table import Table
from .plot import Plot
from .manim import Manim
from .flow_animation import FlowAnimation

__all__ = ["Text", "Image", "Graph", "AnimatedGraph", "Table", "Plot", "Manim", "FlowAnimation"]
