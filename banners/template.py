"""Template — render slides on a fixed 16:9 canvas, like a PowerPoint master.

By default banners renders slides in its editorial style, which flows with the
notebook width. A `Template` replaces that with a fixed 16:9 canvas where every
element has a position and size relative to the slide, exactly like a
corporate PowerPoint template. Font sizes are expressed in container-query
units (`cqw`, percent of the slide width), so a slide keeps its proportions and
stays legible at any screen size.

Activate a template for the whole deck with `configure(template=...)`:

```python
from banners import configure, Template

corp = Template(
    primary="#ff6600",
    secondary="#054af6",
    logo_on_dark="assets/logo_white.png",
    logo_on_light="assets/logo_color.png",
    mark="assets/isotype.png",
)
configure(template=corp, team="Analytics", date="November 2026")
```

Each slide type maps to a template layout:

| Slide | Layout |
|-------|--------|
| `Cover()` | Dark cover with logo, title in the primary color. |
| `Cover(image=...)` | Photo cover with the title over the picture. |
| `Section()` with no content | Divider. With `image=`, the photo fills the right half. |
| `Section(content=[visual, Text(...)])` | Visual on the left, title and text on the right. |
| `Section(content=..., image=...)` | Photo on the left half, title and content on the right. |
| `Section(content=...)` otherwise | Title on top, content in columns below. |
| `Intro()` | Large title in the left column, content in columns on the right. |
| `Closing()` | Dark closing slide; `title=""` shows the centered logo. |
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import marimo as mo

# Slide-relative font sizes, in percent of the slide width (cqw). They come
# from the point sizes of a 16:9 PowerPoint master (slide width ≈ 1583 pt):
# 94.5 pt display titles, 52 pt content titles, 44 pt subtitles, 37 pt labels,
# 28 pt body text and 25 pt dates.
SIZES = {
    "display": 5.97,
    "closing": 4.17,
    "title": 3.28,
    "subtitle": 2.78,
    "label": 2.34,
    "body": 1.77,
    "small": 1.58,
}


@dataclass
class Template:
    """Fixed 16:9 slide template.

    Images (`logo_on_dark`, `logo_on_light`, `mark`, `closing_image`) accept a
    URL, a file path, or raw bytes. URLs are loaded by the browser when the
    slide is shown (nothing is downloaded or embedded); paths and bytes are
    embedded in the slide. Leave them as `None` to omit them.

    Attributes:
        primary: Title color and main segment of the bottom bar.
        secondary: End segment of the bottom bar.
        dark: Background of the dark cover and of the logo closing slide.
        closing_bg: Background of the closing slide with a title.
        light: Background of dividers and content slides.
        text: Body text color on light backgrounds.
        muted: Labels and subtitles on light backgrounds.
        on_dark: Text color on dark backgrounds.
        font: CSS font-family stack.
        logo_on_dark: Full logo for dark backgrounds. When `None`,
            `logo_on_light` is shown in white, with `mark` kept in color over
            its left `logo_mark_width` fraction.
        logo_on_light: Full logo for light backgrounds.
        mark: Small isotype shown in the top-right corner of content slides.
        closing_image: Picture shown next to the closing title.
        logo_mark_width: Fraction of the logo width taken by the isotype at
            its left (used only by the white-logo fallback).
        bar: Draw the two-color bar along the bottom edge.
        bar_split: Fraction of the bar width taken by `primary`.
        scale: Multiplier applied to every font size.
    """

    primary: str = "#e4572e"
    secondary: str = "#2a6fdb"
    dark: str = "#404040"
    closing_bg: str = "#363e45"
    light: str = "#f5f5f5"
    text: str = "#343e46"
    muted: str = "#6b7280"
    on_dark: str = "#f5f5f5"
    font: str = "'Century Gothic', 'URW Gothic', 'URW Gothic L', 'Questrial', 'Avenir Next', sans-serif"
    logo_on_dark: object = None
    logo_on_light: object = None
    mark: object = None
    closing_image: object = None
    logo_mark_width: float = 0.205
    bar: bool = True
    bar_split: float = 2 / 3
    scale: float = 1.0

    # ── Entry point ──────────────────────────────────────────────────────────

    def render(self, slide) -> mo.Html:
        """Render `slide` with the layout that matches its type and content.

        Args:
            slide: A `Cover`, `Intro`, `Section`, or `Closing` instance.

        Returns:
            A `mo.Html` 16:9 canvas.
        """
        kind = type(slide).__name__
        if kind == "Cover":
            html = self._cover(slide)
        elif kind == "Closing":
            html = self._closing(slide)
        elif kind == "Intro":
            html = self._intro(slide)
        else:
            html = self._section(slide)
        return mo.Html(html)

    # ── Primitives ───────────────────────────────────────────────────────────

    def _fs(self, size: str) -> str:
        return f"{SIZES[size] * self.scale:.3f}cqw"

    def _canvas(self, bg: str, inner: str, color: str, bar_top: float = 95.4) -> str:
        bar = ""
        if self.bar:
            split = self.bar_split * 100
            bar = (
                self._box(0, bar_top, split, 4.6, "", f"background:{self.primary};")
                + self._box(split, bar_top, 100 - split, 4.6, "", f"background:{self.secondary};")
            )
        return (
            '<div style="container-type:inline-size;width:100%;">'
            f'<div style="position:relative;width:100%;aspect-ratio:16/9;overflow:hidden;'
            f'background:{bg};color:{color};font-family:{self.font};">'
            f"{inner}{bar}</div></div>"
        )

    @staticmethod
    def _box(x: float, y: float, w: float | None, h: float | None, html: str, style: str = "") -> str:
        size = (f"width:{w}%;" if w is not None else "") + (f"height:{h}%;" if h is not None else "")
        return f'<div style="position:absolute;left:{x}%;top:{y}%;{size}{style}">{html}</div>'

    def _text(self, text: str, size: str, color: str, bold: bool = False, extra: str = "") -> str:
        weight = "700" if bold else "400"
        return (
            f'<div style="font-size:{self._fs(size)};font-weight:{weight};color:{color};'
            f'line-height:1.1;{extra}">{text}</div>'
        )

    @staticmethod
    def _src(image) -> str | None:
        """Return an `<img>`-ready source: URLs pass through and are loaded by
        the browser; paths and bytes are embedded as base64 data URIs."""
        if image is None:
            return None
        if isinstance(image, str) and image.startswith(("http://", "https://", "data:")):
            return image
        from .slide import Slide

        try:
            return Slide._icon_src(image)
        except Exception:  # noqa: BLE001 — a decorative image that fails is omitted
            return None

    def _img(self, image, style: str) -> str:
        src = self._src(image)
        return f'<img src="{src}" alt="" style="display:block;{style}">' if src else ""

    def _photo(self, image, x: float, y: float, w: float, h: float, overlay: str = "") -> str:
        src = self._src(image)
        if not src:
            return ""
        layers = f"{overlay}," if overlay else ""
        return self._box(x, y, w, h, "", f"background:{layers}url({src}) center/cover no-repeat;")

    def _logo(self, image, x: float, y: float, w: float, style: str = "") -> str:
        return self._box(x, y, w, None, self._img(image, f"width:100%;height:auto;{style}"))

    def _dark_logo(self, x: float, y: float, w: float) -> str:
        """Logo for dark backgrounds: `logo_on_dark`, or else `logo_on_light`
        turned solid white with a CSS filter."""
        if self.logo_on_dark is not None:
            return self._logo(self.logo_on_dark, x, y, w)
        white = self._img(self.logo_on_light, "width:100%;height:auto;filter:brightness(0) invert(1);"
                          + (f"clip-path:inset(0 0 0 {self.logo_mark_width * 100:.1f}%);" if self.mark else ""))
        if not white:
            return ""
        # Keep the isotype in color: the white copy hides its own mark area and
        # `mark` is drawn on top, at the left, with the logo's full height.
        color_mark = (
            self._img(self.mark, "position:absolute;left:0;top:0;height:100%;width:auto;")
            if self.mark else ""
        )
        return self._box(x, y, w, None, f'<div style="position:relative;">{white}{color_mark}</div>')

    def _mark(self) -> str:
        return self._box(91.9, 5.7, 2.9, None, self._img(self.mark, "width:100%;height:auto;"))

    def _content(self, slide, items: list, color: str, columns: bool = True, lead: str = "") -> str:
        """Render content items as body text, side by side when `columns` is set."""
        from .content.text import Text

        uid = f"tp{uuid.uuid4().hex[:8]}"
        parts = []
        for item in items:
            if isinstance(item, (Text, str)):
                body = item.body if isinstance(item, Text) else item
                html = mo.as_html(Text(body).render()).text
            elif hasattr(item, "render") and callable(item.render):
                html = mo.as_html(item.render()).text
            else:
                html = mo.as_html(item).text
            parts.append(f'<div style="min-width:0;min-height:0;">{html}</div>')
        cols = len(parts) if columns and parts else 1
        grid = (
            f'<div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));'
            f'column-gap:3cqw;row-gap:1.5cqw;align-items:start;">{"".join(parts)}</div>'
        )
        lead_html = (
            f'<div class="{uid}-lead" style="margin-bottom:1.5cqw;font-weight:700;">{lead}</div>'
            if lead else ""
        )
        accent = self.primary
        return (
            f"<style>"
            f".{uid}{{font-size:{self._fs('body')};line-height:1.4;color:{color};}}"
            f".{uid} *:not(code):not(pre):not(svg *){{font-size:inherit!important;color:inherit!important;"
            f"line-height:inherit!important;font-family:inherit!important;}}"
            f".{uid} .paragraph,.{uid} p{{margin:0 0 0.8em!important;}}"
            f".{uid} ul,.{uid} ol{{margin:0!important;padding-left:1.1em!important;}}"
            f".{uid} li{{margin:0 0 0.6em!important;}}"
            f".{uid} li::marker{{color:{accent};}}"
            f".{uid} img,.{uid} svg,.{uid} video{{max-width:100%;height:auto;}}"
            f"</style>"
            f'<div class="{uid}" style="width:100%;height:100%;overflow:auto;">{lead_html}{grid}</div>'
        )

    def _footer(self, slide, color: str) -> str:
        if not getattr(slide, "footer", ""):
            return ""
        return self._box(
            50, 88.5, 44.8, None,
            self._text(slide.footer, "small", color, extra="text-align:right;line-height:1.3;"),
        )

    @staticmethod
    def _items(slide) -> list:
        if slide.content is None:
            return []
        return slide.content if isinstance(slide.content, list) else [slide.content]

    # ── Layouts ──────────────────────────────────────────────────────────────

    def _cover(self, s) -> str:
        image = getattr(s, "image", None)
        if image is None:
            inner = (
                self._dark_logo(5.1, 6.1, 21.3)
                + (self._box(50, 7, 44.9, None, self._text(s.team, "label", self.on_dark, extra="text-align:right;")) if s.team else "")
                + self._box(11.7, 37, 80, None, self._text(s.title, "display", self.primary, bold=True))
                + (self._box(12.2, 52, 75, None, self._text(s.subtitle, "subtitle", self.on_dark, extra="line-height:1.25;")) if s.subtitle else "")
                + (self._box(5.8, 87.5, 50, None, self._text(s.date, "small", self.on_dark)) if s.date else "")
            )
            return self._canvas(self.dark, inner, self.on_dark)
        shade = "linear-gradient(90deg,rgba(0,0,0,0.55) 0%,rgba(0,0,0,0.15) 55%,rgba(0,0,0,0) 100%)"
        inner = (
            self._photo(image, 0, 0, 100, 76.1, overlay=shade)
            + self._box(5.2, 29, 60, None, self._text(s.title, "display", "#ffffff", bold=True))
            + (self._box(5.6, 44.5, 55, None, self._text(s.subtitle, "subtitle", "#ffffff", extra="line-height:1.25;")) if s.subtitle else "")
            + (self._box(5.6, 68.4, 60, None, self._text(s.team, "label", "#ffffff")) if s.team else "")
            + (self._box(7.3, 87.5, 50, None, self._text(s.date, "small", self.text)) if s.date else "")
            + self._logo(self.logo_on_light, 77.9, 86, 18.4)
        )
        return self._canvas(self.light, inner, self.text, bar_top=76.1)

    def _divider(self, s) -> str:
        image = getattr(s, "image", None)
        title_color = self.text if image is not None else self.primary
        width = 38 if image is not None else 85
        inner = (
            self._photo(image, 46.5, 0, 53.5, 95.4)
            + self._logo(self.logo_on_light, 5.2, 7, 21.3)
            + self._box(5.2, 36, width, None, self._text(s.title, "display", title_color, bold=True))
            + (self._box(5.2, 72.9, width, None, self._text(s.subtitle, "label", self.muted, extra="line-height:1.25;")) if s.subtitle else "")
        )
        return self._canvas(self.light, inner, self.text)

    def _stack(self, s, x: float, y: float, w: float, h: float, body: str) -> str:
        """Title, subtitle and body in one vertical flow, so a long title pushes
        the body down instead of overlapping it."""
        subtitle = (
            self._text(s.subtitle, "body", self.muted, extra="margin-top:0.6cqw;line-height:1.3;")
            if s.subtitle else ""
        )
        return self._box(
            x, y, w, h,
            self._text(s.title, "title", self.primary, bold=True)
            + subtitle
            + f'<div style="flex:1;min-height:0;margin-top:2.2cqw;">{body}</div>',
            "display:flex;flex-direction:column;",
        )

    def _section(self, s) -> str:
        from .content.text import Text

        items = self._items(s)
        if not items:
            return self._divider(s)
        image = getattr(s, "image", None)

        if image is not None:
            # Photo on the left half, title and content on the right.
            inner = (
                self._photo(image, 0, 0, 54, 95.4)
                + self._stack(s, 57.8, 14, 34, 74, self._content(s, items, self.text, columns=False))
                + self._mark()
            )
            return self._canvas(self.light, inner, self.text)

        if len(items) >= 2 and not isinstance(items[0], (Text, str)):
            # Visual on the left, title and text on the right.
            visual = self._content(s, items[:1], self.text)
            inner = (
                self._box(5.1, 22, 44.9, 62, visual, "background:#ffffff;padding:1.2cqw;box-sizing:border-box;")
                + self._stack(s, 54.4, 22, 40.4, 66, self._content(s, items[1:], self.text, columns=False))
                + self._mark()
                + self._footer(s, self.muted)
            )
            return self._canvas(self.light, inner, self.text)

        # Title on top, content in columns below.
        inner = (
            self._stack(s, 5.2, 10, 84, 76, self._content(s, items, self.text))
            + self._mark()
            + self._footer(s, self.muted)
        )
        return self._canvas(self.light, inner, self.text)

    def _intro(self, s) -> str:
        label_text = s.subtitle or s.tag or ""
        lead = ""
        if s.summary:
            lead = mo.as_html(mo.md(s.summary)).text
        items = self._items(s)
        inner = (
            self._logo(self.logo_on_light, 5.2, 7, 21.3)
            + self._box(5.2, 28.8, 27.1, 42, self._text(s.title, "display", self.primary, bold=True))
            + (self._box(5.2, 72.9, 27.1, None, self._text(label_text, "label", self.muted, extra="line-height:1.25;")) if label_text else "")
            + self._box(35.8, 28.8, 57.2, 56, self._content(s, items, self.text, lead=lead))
            + self._footer(s, self.muted)
        )
        return self._canvas(self.light, inner, self.text)

    def _closing(self, s) -> str:
        if not s.title:
            inner = (
                self._dark_logo(38, 45.7, 24)
                + (self._box(5.1, 86.5, 50, None, self._text(s.team, "label", self.on_dark)) if s.team else "")
            )
            return self._canvas(self.dark, inner, self.on_dark)

        has_image = self._src(self.closing_image) is not None
        dy = 6 if s.stats else 0  # push the title down to make room for the stats row
        if has_image:
            head = (
                self._box(5, 40 + dy, 45, 20,
                          self._text(s.title, "closing", "#ffffff", bold=True, extra="text-align:right;"),
                          "display:flex;align-items:center;justify-content:flex-end;")
                + self._box(51.5, 42.9 + dy, None, 14.2, "", "border-left:1px solid rgba(255,255,255,0.7);")
                + self._box(54.8, 38.8 + dy, 9.9, 22.5, self._img(self.closing_image, "height:100%;width:auto;"))
            )
        else:
            head = self._box(10, 40 + dy, 80, 20,
                             self._text(s.title, "closing", "#ffffff", bold=True, extra="text-align:center;"),
                             "display:flex;align-items:center;justify-content:center;")
        sub = (
            self._box(10, 62 + dy, 80, None,
                      self._text(s.subtitle, "body", self.on_dark, extra="text-align:center;line-height:1.3;"))
            if s.subtitle else ""
        )
        stats = ""
        if s.stats:
            cells = "".join(
                f'<div style="text-align:center;padding:0 1cqw;">'
                f'<div style="font-size:{self._fs("title")};font-weight:700;color:{self.primary};">{v}</div>'
                f'<div style="font-size:{self._fs("body")};color:{self.on_dark};margin-top:0.4cqw;">{label}</div>'
                f'<div style="font-size:{self._fs("small")};color:{self.on_dark};opacity:0.7;">{cap}</div></div>'
                for v, label, cap in s.stats
            )
            stats = self._box(10, 14, 80, None,
                              f'<div style="display:grid;grid-template-columns:repeat({len(s.stats)},1fr);">{cells}</div>')
        team = self._box(5.1, 86.5, 50, None, self._text(s.team, "label", self.on_dark)) if s.team else ""
        return self._canvas(self.closing_bg, head + sub + stats + team, self.on_dark)


# ── Presets ───────────────────────────────────────────────────────────────────

_COMMONS = "https://commons.wikimedia.org/wiki/Special:FilePath/"

BECH = Template(
    primary="#ff6600",
    secondary="#054af6",
    dark="#404040",
    closing_bg="#363e45",
    light="#f5f5f5",
    text="#343e46",
    muted="#6b7280",
    font="'Century Gothic', 'URW Gothic', 'URW Gothic L', 'Questrial', sans-serif",
    logo_on_light=_COMMONS + "Logo_BancoEstado.svg",
    mark=_COMMONS + "Logo_BancoEstado_(cropped).svg",
)
"""Template inspired by BancoEstado's 16:9 decks (colors, font and layout).

This is not an official BancoEstado template and is not endorsed by BancoEstado.

Logos are linked from Wikimedia Commons and loaded by the
browser, so no brand files live in this repository. On dark slides the logo is
shown in solid white. Photos are not included: pass your own with
`Cover(image=...)` / `Section(image=...)`. To add more images, copy the preset:

```python
from dataclasses import replace
from banners.template import BECH

mine = replace(BECH, closing_image="assets/pato.png")
```
"""
