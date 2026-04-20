"""Base Slide class."""

from __future__ import annotations

import base64
import ssl
import urllib.request
from pathlib import Path
from typing import TYPE_CHECKING

import marimo as mo

from .palette import Palette

if TYPE_CHECKING:
    from .content.text import Text
    from .content.image import Image
    from .content.graph import Graph

ContentItem = object
"""Type alias for a single content element: Text, Image, Graph, or any marimo component."""


class Slide:
    """Abstract base class for all slide types.

    Subclasses must implement `_render_banner` to produce the banner HTML.
    The `render` method assembles the full slide as a `mo.vstack`.

    Content layout is resolved automatically based on what is passed:

    - **Single item** — rendered at full width.
    - **List of `Text` only** — rendered as equal columns via `mo.hstack`.
      Pass `content_kind` to wrap each column in a `mo.callout` box.
    - **List with any `Image` or `Graph`** — rendered as an equal-width CSS
      grid (`1fr` per column) automatically, no extra parameter needed.

    Args:
        title: Main heading of the slide.
        subtitle: Support phrase displayed inside the banner.
        content: Content elements below the banner. Accepts a single
            `Text`, `Image`, or `Graph` instance, a list of them, or any
            marimo component.
        palette: Color palette for the banner. Defaults to `ORANGE`.
        content_kind: Box style applied to `Text` items when the content is
            a list of text-only elements. Accepted values: `"neutral"`,
            `"info"`, `"success"`, `"warn"`, `"danger"`.

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
        content: "list[ContentItem] | ContentItem | None" = None,
        palette: Palette | None = None,
        content_kind: "str | None" = None,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.palette = palette or Palette()
        self.content_kind = content_kind

    def render(self) -> mo.Html:
        """Assemble and return the complete slide as a marimo component.

        Returns:
            A `mo.Html` component (via `mo.vstack`) ready to display in a
            marimo cell.
        """
        parts: list = [self._render_banner()]
        parts.extend(self._render_content())
        return mo.vstack(parts)

    def _display_(self):
        return self.render()

    def _render_banner(self) -> mo.Html:
        """Produce the banner HTML for this slide type.

        Raises:
            NotImplementedError: Must be implemented by each subclass.
        """
        raise NotImplementedError(f"{type(self).__name__} must implement _render_banner()")

    def _render_content(self) -> list:
        """Resolve content items into marimo components and apply layout.

        Returns:
            A list of marimo components to be stacked below the banner.
        """
        if self.content is None:
            return []

        items = self.content if isinstance(self.content, list) else [self.content]

        if len(items) == 1:
            return [self._render_item(items[0])]

        from .content.text import Text as _Text
        has_non_text = any(not isinstance(i, (_Text, str)) for i in items)

        rendered = [
            self._render_item(item, wrap_kind=self.content_kind)
            for item in items
        ]

        if has_non_text:
            return [self._css_grid(rendered)]
        return [mo.hstack(rendered, justify="space-between")]

    def _render_item(self, item: ContentItem, wrap_kind: "str | None" = None):
        """Render a single content item into a marimo component.

        Args:
            item: A `Text`, `Image`, `Graph`, plain string, or marimo component.
            wrap_kind: If set and the item is `Text` or `str`, wraps the
                rendered markdown in a `mo.callout` with this kind.

        Returns:
            A marimo component.
        """
        from .content.text import Text as _Text

        if isinstance(item, (_Text, str)):
            md = mo.md(item.body if isinstance(item, _Text) else item)
            return mo.callout(md, kind=wrap_kind) if wrap_kind else md

        if hasattr(item, "render") and callable(item.render):
            return item.render()

        return item

    @staticmethod
    def _css_grid(items: list) -> mo.Html:
        """Wrap rendered items in an equal-width CSS grid container.

        Args:
            items: List of marimo `mo.Html` components.

        Returns:
            A `mo.Html` component with a CSS grid layout (`1fr` per column).
        """
        cols = " ".join(["1fr"] * len(items))
        parts = []
        for item in items:
            html = item.text if hasattr(item, "text") else str(item)
            parts.append(f'<div style="min-width:0;">{html}</div>')
        inner = "".join(parts)
        return mo.Html(
            f'<div style="display:grid;grid-template-columns:{cols};'
            f'gap:1rem;align-items:start;">{inner}</div>'
        )

    @staticmethod
    def _tag_line(text: str, color: str) -> str:
        return (
            f'<div style="font-size:0.85rem;letter-spacing:0.2em;text-transform:uppercase;'
            f'color:{color};margin-bottom:0.5rem;">{text}</div>'
        )

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

    def _icon_corner_html(self, icon: "dict | None", bottom: str, right: str, default_size: str) -> str:
        if icon is None:
            return ""
        try:
            size = icon.get("size", default_size)
            src = self._icon_src(icon["src"])
            return (
                f'<img src="{src}" '
                f'style="position:absolute;bottom:{bottom};right:{right};'
                f'height:{size};opacity:0.85;border-radius:4px;">'
            )
        except Exception:
            return ""

    def _icon_inline_html(self, icon: "dict | None", default_size: str, style: str = "") -> str:
        if icon is None:
            return ""
        try:
            size = icon.get("size", default_size)
            src = self._icon_src(icon["src"])
            return f'<img src="{src}" style="height:{size};{style}border-radius:4px;">'
        except Exception:
            return ""
