"""Base Slide class.

Every slide is drawn on a fixed 16:9 canvas by the active `Template`: the one
set with `configure(template=...)`, or a default `Template()` when none is set.
`Slide` only stores what the slide says; the template decides how it looks.
"""

from __future__ import annotations

import base64
import ssl
import urllib.request
from pathlib import Path

import marimo as mo

from . import config as _cfg
from .palette import Palette

ContentItem = object
"""Type alias for a single content element: Text, Image, Graph, or any marimo component."""


class Slide:
    """Base class for all slide types.

    Subclasses add the fields of their layout (`Cover.date`, `Section.number`, …);
    the active template turns the slide into a 16:9 canvas.

    Args:
        title: Main heading of the slide.
        subtitle: Support phrase shown under the title.
        content: Content elements of the slide. Accepts a single `Text`,
            `Image`, `Graph` (or any element with `.render()`), a list of them,
            or any marimo component.
        palette: Colors for this slide only; replaces the configured and the
            template palette. `None` uses those.
        footer: Small note shown at the bottom right of content slides.
        background: `Background` that paints the canvas of this slide.

    Example:
        ```python
        from banners.slides import Section
        from banners.content import Text, Graph

        Section(
            title="Pipeline",
            content=[
                Text("Each stage runs independently."),
                Graph("graph LR\\n  A --> B --> C"),
            ],
        ).render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        content: list[ContentItem] | ContentItem | None = None,
        palette: Palette | None = None,
        footer: str = "",
        background=None,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.palette = palette
        self.footer = footer
        self.background = background

    def render(self) -> mo.Html:
        """Render the slide with the active template.

        Returns:
            A `mo.Html` 16:9 canvas ready to display in a marimo cell.
        """
        from .template import Template

        template = _cfg.get("template") or Template()
        return template.render(self)

    def _display_(self) -> mo.Html:
        """Display the slide when it is the last expression of a marimo cell.

        Returns:
            The same canvas as `render()`.
        """
        return self.render()

    @staticmethod
    def _icon_src(icon) -> str:
        """Convert a path, URL, or bytes to a base64 data URI.

        Args:
            icon: File path (`str` or `Path`), URL string, or raw `bytes`.

        Returns:
            A `data:image/<mime>;base64,...` string.
        """
        _EXT_MIME = {
            "jpg": "jpeg", "jpeg": "jpeg", "png": "png",
            "svg": "svg+xml", "gif": "gif", "webp": "webp",
        }
        if isinstance(icon, str) and icon.startswith(("http://", "https://")):
            ext = icon.split("?")[0].rsplit(".", 1)[-1].lower()
            mime = _EXT_MIME.get(ext, "png")
            req = urllib.request.Request(icon, headers={"User-Agent": "Mozilla/5.0"})
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                data = r.read()
                ct = r.headers.get("Content-Type", "")
            if "svg" in ct:
                mime = "svg+xml"
            elif "jpeg" in ct or "jpg" in ct:
                mime = "jpeg"
            elif "png" in ct:
                mime = "png"
            b64 = base64.b64encode(data).decode()
            return f"data:image/{mime};base64,{b64}"

        if isinstance(icon, (str, Path)):
            p = Path(icon)
            mime = _EXT_MIME.get(p.suffix.lower().lstrip("."), "png")
            b64 = base64.b64encode(p.read_bytes()).decode()
            return f"data:image/{mime};base64,{b64}"

        b64 = base64.b64encode(icon).decode()
        return f"data:image/png;base64,{b64}"
