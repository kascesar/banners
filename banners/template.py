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
        heading_font: CSS font-family for titles; `None` uses `font`.
        cover_image: Photo used by `Cover` when the slide passes no `image`;
            `Cover(image=False)` turns it off for one slide.
        divider_image: Photo used by dividers when the slide passes no `image`;
            `Section(image=False)` turns it off for one slide.
        divider_icon: Large icon on dividers without a photo: an icon name
            from `banners.icons.ICONS` or any image source.
        icon_color: Color of named icons (`mark`, `divider_icon`); defaults to
            the title color.
        bar_colors: Colors of the bottom bar in equal segments; overrides
            `primary`/`secondary`/`bar_split`.
        section_colors: Colors cycled by section number for titles and icons
            of `Section` slides (colorful decks).
        panel: Background of the box that holds a chart or visual.
        auto_contrast: Replace title colors that fall below a 3:1 contrast
            ratio with the background. Turn off to keep exact brand colors.
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
    heading_font: str | None = None
    cover_image: object = None
    divider_image: object = None
    divider_icon: object = None
    icon_color: str | None = None
    bar_colors: tuple | None = None
    section_colors: tuple | None = None
    panel: str = "#ffffff"
    auto_contrast: bool = True

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
        if self.bar and self.bar_colors:
            n = len(self.bar_colors)
            bar = "".join(
                self._box(i * 100 / n, bar_top, 100 / n, 4.6, "", f"background:{c};")
                for i, c in enumerate(self.bar_colors)
            )
        elif self.bar:
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
        if self.heading_font and size in ("display", "title", "closing"):
            extra = f"font-family:{self.heading_font};" + extra
        return (
            f'<div style="font-size:{self._fs(size)};font-weight:{weight};color:{color};'
            f'line-height:1.1;{extra}">{text}</div>'
        )

    def _on(self, bg: str, color: str) -> str:
        """Return `color`, or a readable fallback when it lacks contrast with `bg`.

        The check uses the WCAG contrast ratio with a 3:1 minimum, the threshold
        for large text. It does nothing when `auto_contrast` is off or when
        either color cannot be parsed.

        Args:
            bg: CSS color of the background the text or icon sits on.
            color: CSS color wanted for the text or icon.

        Returns:
            `color` when it is readable on `bg`; otherwise `on_dark` for dark
            backgrounds and `text` for light ones.
        """
        from .background import _parse_first_color, _relative_luminance

        if not self.auto_contrast:
            return color
        a, b = _parse_first_color(bg), _parse_first_color(color)
        if a is None or b is None:
            return color
        la, lb = _relative_luminance(*a), _relative_luminance(*b)
        ratio = (max(la, lb) + 0.05) / (min(la, lb) + 0.05)
        if ratio >= 3:
            return color
        return self.on_dark if la < 0.18 else self.text

    def _title_color(self, slide) -> str:
        """Return the title color of a slide.

        Args:
            slide: The slide being rendered; a numbered `Section` picks its
                color from `section_colors`.

        Returns:
            The `section_colors` entry for the section number (cycled), or
            `primary` when there are no section colors or no number.
        """
        number = getattr(slide, "number", None)
        if self.section_colors and number and str(number).isdigit():
            return self.section_colors[(int(number) - 1) % len(self.section_colors)]
        return self.primary

    def _resolve(self, image, color: str):
        """Turn an icon name into a colored icon; pass other sources through.

        Args:
            image: An icon name from `banners.icons.ICONS`, or any image
                source (path, URL, bytes, `None`).
            color: Stroke color for a named icon; `icon_color` wins when set.

        Returns:
            A `data:` URI for icon names, or `image` unchanged otherwise.
        """
        from .icons import ICONS, icon

        if isinstance(image, str) and image in ICONS:
            return icon(image, color=self.icon_color or color)
        return image

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
        from .icons import ICONS

        if self.logo_on_dark is not None:
            return self._logo(self.logo_on_dark, x, y, w)
        # A named icon is not part of the logo artwork, so the logo is not
        # clipped and the icon is not drawn over it.
        isotype = None if isinstance(self.mark, str) and self.mark in ICONS else self.mark
        white = self._img(self.logo_on_light, "width:100%;height:auto;filter:brightness(0) invert(1);"
                          + (f"clip-path:inset(0 0 0 {self.logo_mark_width * 100:.1f}%);" if isotype else ""))
        if not white:
            return ""
        # Keep the isotype in color: the white copy hides its own mark area and
        # `mark` is drawn on top, at the left, with the logo's full height.
        color_mark = (
            self._img(isotype, "position:absolute;left:0;top:0;height:100%;width:auto;")
            if isotype else ""
        )
        return self._box(x, y, w, None, f'<div style="position:relative;">{white}{color_mark}</div>')

    def _mark(self, color: str | None = None) -> str:
        mark = self._resolve(self.mark, self._on(self.light, color or self.primary))
        return self._box(91.9, 5.7, 2.9, None, self._img(mark, "width:100%;height:auto;"))

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
    def _slide_image(slide, default):
        """Choose the photo of a slide: its own `image`, or the preset default.

        Args:
            slide: The slide being rendered; its `image` attribute may be a
                source, `None` (use `default`) or `False` (no photo).
            default: The template's photo for this layout (`cover_image` or
                `divider_image`).

        Returns:
            The image source to draw, or `None` for no photo.
        """
        image = getattr(slide, "image", None)
        if image is False:
            return None
        return default if image is None else image

    @staticmethod
    def _items(slide) -> list:
        if slide.content is None:
            return []
        return slide.content if isinstance(slide.content, list) else [slide.content]

    # ── Layouts ──────────────────────────────────────────────────────────────

    def _cover(self, s) -> str:
        image = self._slide_image(s, self.cover_image)
        if image is None:
            inner = (
                self._dark_logo(5.1, 6.1, 21.3)
                + (self._box(50, 7, 44.9, None, self._text(s.team, "label", self.on_dark, extra="text-align:right;")) if s.team else "")
                + self._box(11.7, 37, 80, None, self._text(s.title, "display", self._on(self.dark, self._title_color(s)), bold=True))
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
        image = self._slide_image(s, self.divider_image)
        accent = self._title_color(s)
        title_color = self.text if image is not None else self._on(self.light, accent)
        icon_html = ""
        if image is None and self.divider_icon is not None:
            src = self._resolve(self.divider_icon, self._on(self.light, accent))
            icon_html = self._box(66, 24, 22, None, self._img(src, "width:100%;height:auto;opacity:0.9;"))
        width = 38 if image is not None or icon_html else 85
        inner = (
            icon_html
            + self._photo(image, 46.5, 0, 53.5, 95.4)
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
            self._text(s.title, "title", self._on(self.light, self._title_color(s)), bold=True)
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

        if image:
            # Photo on the left half, title and content on the right.
            inner = (
                self._photo(image, 0, 0, 54, 95.4)
                + self._stack(s, 57.8, 14, 34, 74, self._content(s, items, self.text, columns=False))
                + self._mark(self._title_color(s))
            )
            return self._canvas(self.light, inner, self.text)

        if len(items) >= 2 and not isinstance(items[0], (Text, str)):
            # Visual on the left, title and text on the right.
            visual = self._content(s, items[:1], self.text)
            inner = (
                self._box(5.1, 22, 44.9, 62, visual, f"background:{self.panel};padding:1.2cqw;box-sizing:border-box;")
                + self._stack(s, 54.4, 22, 40.4, 66, self._content(s, items[1:], self.text, columns=False))
                + self._mark(self._title_color(s))
                + self._footer(s, self.muted)
            )
            return self._canvas(self.light, inner, self.text)

        # Title on top, content in columns below.
        inner = (
            self._stack(s, 5.2, 10, 84, 76, self._content(s, items, self.text))
            + self._mark(self._title_color(s))
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
            + self._box(5.2, 28.8, 27.1, 42, self._text(s.title, "display", self._on(self.light, self._title_color(s)), bold=True))
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

        accent = self._on(self.closing_bg, self.primary)
        closing_image = self._resolve(self.closing_image, accent)
        has_image = self._src(closing_image) is not None
        dy = 6 if s.stats else 0  # push the title down to make room for the stats row
        if has_image:
            head = (
                self._box(5, 40 + dy, 45, 20,
                          self._text(s.title, "closing", "#ffffff", bold=True, extra="text-align:right;"),
                          "display:flex;align-items:center;justify-content:flex-end;")
                + self._box(51.5, 42.9 + dy, None, 14.2, "", "border-left:1px solid rgba(255,255,255,0.7);")
                + self._box(54.8, 38.8 + dy, 9.9, 22.5, self._img(closing_image, "height:100%;width:auto;"))
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
                f'<div style="font-size:{self._fs("title")};font-weight:700;color:{accent};">{v}</div>'
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
    auto_contrast=False,  # keep the brand orange exactly as in the deck
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


def _commons(name: str, width: int = 1920) -> str:
    """Build a Wikimedia Commons URL that serves a file resized.

    Args:
        name: File name on Wikimedia Commons, without the `File:` prefix.
        width: Width in pixels of the served image.

    Returns:
        A `https://commons.wikimedia.org/wiki/Special:FilePath/...` URL.
    """
    return f"{_COMMONS}{name}?width={width}"


EXECUTIVE = Template(
    primary="#1f2933",
    secondary="#9aa5b1",
    dark="#1f2933",
    closing_bg="#1f2933",
    light="#ffffff",
    text="#323f4b",
    muted="#7b8794",
    on_dark="#f5f7fa",
    font="'Helvetica Neue', Arial, sans-serif",
    heading_font="Georgia, Cambria, 'Times New Roman', serif",
    mark="chart",
    divider_icon="layers",
    bar=False,
)
"""Sober, monochrome: graphite on white, serif titles, thin line icons, no bar."""

INSTITUTIONAL = Template(
    primary="#0b2545",
    secondary="#8da9c4",
    dark="#0b2545",
    closing_bg="#0b2545",
    light="#f7f9fb",
    text="#13315c",
    muted="#6b7c93",
    font="'Helvetica Neue', Arial, sans-serif",
    heading_font="Cambria, Georgia, serif",
    mark="building",
    divider_icon="shield",
)
"""Formal navy with steel blue, serif titles and monochrome navy icons."""

COSMOS = Template(
    primary="#22d3ee",
    secondary="#a78bfa",
    dark="#070912",
    closing_bg="#070912",
    light="#0d1024",
    text="#e5e7eb",
    muted="#9ca3af",
    on_dark="#e5e7eb",
    panel="#151936",
    font="'Helvetica Neue', Arial, sans-serif",
    cover_image=_commons("Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg"),
    divider_image=_commons("The_Earth_seen_from_Apollo_17.jpg"),
    mark="orbit",
    bar_colors=("#22d3ee", "#a78bfa", "#f472b6"),
    section_colors=("#22d3ee", "#a78bfa", "#f472b6", "#facc15"),
)
"""Dark, colorful space theme with NASA public-domain photos (Hubble's Pillars
of Creation on the cover, Apollo 17's Earth on dividers)."""

VIBRANT = Template(
    primary="#ef476f",
    secondary="#118ab2",
    dark="#073b4c",
    closing_bg="#073b4c",
    light="#ffffff",
    text="#1f2937",
    muted="#6b7280",
    font="'Trebuchet MS', 'Segoe UI', Arial, sans-serif",
    mark="spark",
    divider_icon="target",
    bar_colors=("#ef476f", "#ffd166", "#06d6a0", "#118ab2"),
    section_colors=("#ef476f", "#118ab2", "#0a9396", "#e76f51"),
)
"""Bright and playful: four-color bar, each section in its own color."""

TERRA = Template(
    primary="#2d6a4f",
    secondary="#c8553d",
    dark="#1b4332",
    closing_bg="#1b4332",
    light="#f4f1ea",
    text="#283618",
    muted="#6b705c",
    font="Verdana, 'DejaVu Sans', sans-serif",
    heading_font="Georgia, Cambria, serif",
    cover_image=_commons("Grand_Canyon_National_Park_GRCA9857.jpg"),
    mark="mountain",
    divider_icon="leaf",
    bar_colors=("#2d6a4f", "#dda15e", "#c8553d"),
    section_colors=("#2d6a4f", "#bc6c25", "#c8553d"),
)
"""Earthy greens and terracotta with a public-domain Grand Canyon photo
(U.S. National Park Service) on the cover; good for climate and nature topics."""

PRESETS = {
    "BECH": BECH,
    "EXECUTIVE": EXECUTIVE,
    "INSTITUTIONAL": INSTITUTIONAL,
    "COSMOS": COSMOS,
    "VIBRANT": VIBRANT,
    "TERRA": TERRA,
}
"""All built-in templates by name."""
