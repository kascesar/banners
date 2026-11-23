"""Base Slide class."""

from __future__ import annotations

import base64
import ssl
import textwrap
import urllib.request
import uuid
from pathlib import Path

import marimo as mo

from . import config as _cfg
from .palette import Palette

INK = "#111827"
"""Primary text color for headings drawn directly on the slide."""
MUTED = "#6b7280"
"""Secondary text color (subtitles, labels, captions)."""
RULE = "#e5e7eb"
"""Hairline color for dividers."""
BODY_SIZE = "1.2rem"
"""Font size of slide body text (marimo's default is about 1rem)."""
"""Hairline color for dividers."""

_KIND_COLORS = {
    "neutral": "#4b5563",
    "info": "#2f6fd0",
    "success": "#2e7d4f",
    "warn": "#b7791f",
    "danger": "#b42318",
}

ContentItem = object
"""Type alias for a single content element: Text, Image, Graph, or any marimo component."""


class Slide:
    """Abstract base class for all slide types.

    Subclasses must implement `_render_banner` to produce the banner HTML.
    The `render` method assembles the full slide as a `mo.vstack`.

    Content layout is resolved automatically based on what is passed:

    - **Single item** — rendered at full width.
    - **List of N items** — rendered as an equal-width CSS grid (`1fr` per
      column) regardless of type. Pass `content_kind` to wrap `Text` items
      in a light card.

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
        content: list[ContentItem] | ContentItem | None = None,
        palette: Palette | None = None,
        content_kind: str | None = None,
        footer: str = "",
        background=None,
    ) -> None:
        self.title = title
        self.subtitle = subtitle
        self.content = content
        self.palette = palette or Palette()
        self.content_kind = content_kind
        self.footer = footer
        self.background = background

    def render(self) -> mo.Html:
        """Assemble and return the complete slide as a marimo component.

        Returns:
            A `mo.Html` component (via `mo.vstack`) ready to display in a
            marimo cell.
        """
        template = _cfg.get("template")
        if template is not None:
            return template.render(self)
        banner = self._render_banner()
        content_parts = self._render_content() + self._render_footer()
        return self._wrap_slide(banner, content_parts)

    def _wrap_slide(self, banner, content_parts: list):
        if self.background is None:
            return mo.vstack([banner] + content_parts)
        bg_css = self.background.css if hasattr(self.background, "css") else str(self.background)
        banner_html = mo.as_html(banner).text
        if content_parts:
            content_inner = mo.as_html(mo.vstack(content_parts)).text
            tc = self.background.text_color() if (
                self.content_kind is None and hasattr(self.background, "text_color")
            ) else None
            if tc is not None:
                uid = f"sbg{id(self):x}"
                tags = (
                    f".{uid} h1,.{uid} h2,.{uid} h3,.{uid} h4,.{uid} h5,.{uid} h6,"
                    f".{uid} p,.{uid} li,.{uid} blockquote,.{uid} code,.{uid} pre,"
                    f".{uid} em,.{uid} strong,.{uid} td,.{uid} th"
                )
                content_html = (
                    f"<style>{tags}{{color:{tc}!important;}}</style>"
                    f'<div class="{uid}" style="color:{tc};">{content_inner}</div>'
                )
            else:
                content_html = content_inner
        else:
            content_html = ""
        return mo.Html(
            f'<div style="background:{bg_css};padding:1.5rem 2rem;border-radius:3px;">'
            f"{banner_html}{content_html}</div>"
        )

    def _render_footer(self) -> list:
        """Render the footer as a small muted note below a hairline.

        Returns:
            A one-item list with the footer `mo.Html`, or an empty list when
            the slide has no footer.
        """
        if not self.footer:
            return []
        _, muted, rule = self._ink()
        body = self._md_html(self.footer, muted)
        return [mo.Html(
            f'<div style="margin-top:1.5rem;padding-top:0.6rem;border-top:1px solid {rule};'
            f'font-size:1rem;">{body}</div>'
        )]

    # ── Design helpers ───────────────────────────────────────────────────────

    def _on_dark(self) -> bool:
        """Tell whether the slide sits on a dark `Background`.

        Returns:
            `True` when the slide has a `Background` whose `text_color()` is
            white, `False` otherwise (no background, light, or unparseable).
        """
        bg = self.background
        return bg is not None and hasattr(bg, "text_color") and bg.text_color() == "#ffffff"

    def _ink(self) -> tuple[str, str, str]:
        """Return the colors for text and lines drawn directly on the slide.

        Switches to white and translucent white when the slide has a dark
        `Background`, so headings stay legible.

        Returns:
            A tuple `(ink, muted, rule)`: heading color, secondary text color
            and hairline color.
        """
        if self._on_dark():
            return "#ffffff", "rgba(255,255,255,0.72)", "rgba(255,255,255,0.22)"
        return INK, MUTED, RULE

    def _accent(self) -> str:
        """Return the accent color of the slide palette.

        Returns:
            `Palette.end` or `SectionPalette.border`, or a neutral gray if the
            palette has neither.
        """
        p = self.palette
        return getattr(p, "end", None) or getattr(p, "border", None) or "#4b5563"

    def _accent_text(self) -> str:
        """Return the color for small accent-colored text (kickers, section numbers).

        The palette accents are mid-tones that lose contrast on a dark
        `Background`, so on dark slides the text uses translucent white and the
        accent stays only on rules and bars.

        Returns:
            A CSS color string.
        """
        return "rgba(255,255,255,0.72)" if self._on_dark() else self._accent()

    @staticmethod
    def _md_html(text: str, color: str, size: str = "inherit") -> str:
        """Render markdown to HTML forcing a text color and size on all its elements.

        marimo renders paragraphs as `<span class="paragraph">`, so the rule
        targets every descendant instead of `p`.

        Args:
            text: Markdown source.
            color: CSS color applied to the text.
            size: CSS font size applied to the text. Defaults to `"inherit"`.

        Returns:
            An HTML string with a scoped `<style>` block and the rendered markdown.
        """
        uid = f"md{uuid.uuid4().hex[:8]}"
        inner = mo.as_html(mo.md(text)).text
        return (
            f"<style>.{uid},.{uid} *{{color:{color}!important;font-size:{size}!important;}}"
            f".{uid} .paragraph,.{uid} p{{margin:0;}}</style>"
            f'<div class="{uid}">{inner}</div>'
        )

    @staticmethod
    def _prose(text: str) -> mo.Html:
        """Render markdown body text at `BODY_SIZE`, larger than marimo's default.

        marimo's default prose size (about 16 px) is hard to read when the
        notebook is projected as slides, so slide text is scaled up.

        Args:
            text: Markdown source.

        Returns:
            A `mo.Html` component.
        """
        uid = f"pr{uuid.uuid4().hex[:8]}"
        inner = mo.as_html(mo.md(textwrap.dedent(text))).text
        return mo.Html(
            f"<style>.{uid} *:not(code):not(pre):not(h1):not(h2):not(h3):not(h4)"
            f"{{font-size:inherit!important;line-height:1.5!important;}}</style>"
            f'<div class="{uid}" style="font-size:{BODY_SIZE};">{inner}</div>'
        )

    @staticmethod
    def _kicker(text: str, color: str) -> str:
        """Build the small uppercase label shown above a heading.

        Args:
            text: Label text.
            color: CSS color of the label.

        Returns:
            An HTML string.
        """
        return (
            f'<div style="font-size:0.9rem;font-weight:600;letter-spacing:0.12em;'
            f'text-transform:uppercase;color:{color};">{text}</div>'
        )

    def _accent_rule(self, rule: str, margin: str = "1rem 0 1.5rem") -> str:
        """Build a full-width hairline with a short accent segment on the left.

        Args:
            rule: CSS color of the hairline.
            margin: CSS margin of the rule block.

        Returns:
            An HTML string.
        """
        return (
            f'<div style="position:relative;height:1px;background:{rule};margin:{margin};">'
            f'<div style="position:absolute;left:0;top:-1px;width:48px;height:3px;'
            f'background:{self._accent()};"></div></div>'
        )

    @staticmethod
    def _card(md, kind: str) -> mo.Html:
        """Wrap rendered markdown in a light card with a top rule colored by `kind`.

        Args:
            md: A marimo component (usually `mo.md`) to place inside the card.
            kind: One of `"neutral"`, `"info"`, `"success"`, `"warn"`,
                `"danger"`. Unknown values fall back to `"neutral"`.

        Returns:
            A `mo.Html` card that fills the height of its grid row.
        """
        color = _KIND_COLORS.get(kind, _KIND_COLORS["neutral"])
        inner = mo.as_html(md).text
        return mo.Html(
            f'<div style="height:100%;box-sizing:border-box;background:#f9fafb;'
            f'border:1px solid {RULE};border-top:2px solid {color};border-radius:2px;'
            f'padding:0.85rem 1.1rem 0.5rem;color:{INK};">{inner}</div>'
        )

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

        rendered = [
            self._render_item(item, wrap_kind=self.content_kind)
            for item in items
        ]

        return [self._css_grid(rendered)]

    def _render_item(self, item: ContentItem, wrap_kind: str | None = None):
        """Render a single content item into a marimo component.

        Args:
            item: A `Text`, `Image`, `Graph`, plain string, or marimo component.
            wrap_kind: If set and the item is `Text` or `str`, wraps the
                rendered markdown in a card whose top rule is colored by kind.

        Returns:
            A marimo component.
        """
        from .content.text import Text as _Text

        if isinstance(item, (_Text, str)):
            md = self._prose(item.body if isinstance(item, _Text) else item)
            return self._card(md, wrap_kind) if wrap_kind else md

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
            html = mo.as_html(item).text
            parts.append(f'<div style="min-width:0;">{html}</div>')
        inner = "".join(parts)
        return mo.Html(
            f'<div style="display:grid;grid-template-columns:{cols};'
            f'gap:1.25rem;align-items:stretch;">{inner}</div>'
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

    def _icon_inline_html(self, icon: dict | None, default_size: str, style: str = "") -> str:
        if icon is None:
            return ""
        try:
            size = icon.get("size", default_size)
            src = self._icon_src(icon["src"])
            return f'<img src="{src}" style="height:{size};{style}border-radius:4px;">'
        except Exception:  # noqa: BLE001 — el ícono es decorativo; si falla, se omite
            return ""
