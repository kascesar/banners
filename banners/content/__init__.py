"""Módulo de contenido para slides.

Clases disponibles:
    Text   — Texto en Markdown.
    Image  — Imagen desde path, bytes o URL.
    Graph  — Diagrama Mermaid.
"""

from .text import Text
from .image import Image
from .graph import Graph

__all__ = ["Text", "Image", "Graph"]
