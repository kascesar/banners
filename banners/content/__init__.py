"""Módulo de contenido para slides.

Clases disponibles:
    Text   — Texto en Markdown.
    Image  — Imagen desde path, bytes o URL.
    Graph  — Diagrama Mermaid.
    Table  — Tabla desde un pandas DataFrame.
    Plot   — Figura de matplotlib o plotly.
"""

from .text import Text
from .image import Image
from .graph import Graph
from .table import Table
from .plot import Plot

__all__ = ["Text", "Image", "Graph", "Table", "Plot"]
