"""Section slide — light, left-aligned header with a numbered title and an accent rule."""

import marimo as mo

from .. import config as _cfg
from ..palette import Palette, SectionPalette
from ..slide import Slide


class Section(Slide):
    """Intermediate section slide with a light, left-aligned header.

    The header shows a small section number in the accent color, the title,
    the subtitle in gray and a full-width hairline with a short accent segment.
    There is no box around the header.

    Takes less vertical space than `Cover` or `Closing`, leaving more room
    for content. Intended for **all middle slides** of a presentation.

    Args:
        title: Section heading.
        subtitle: Short support phrase shown in gray below the title.
        content: Elements displayed below the banner. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
            Lists that contain any `Image` or `Graph` automatically use
            an equal-width CSS grid layout.
        palette: `SectionPalette` (or `Palette`, converted automatically) that
            sets the accent color through its `border` attribute. Defaults to
            the global palette, or the orange `SectionPalette`.
        content_kind: Card style for `Text` items in a list (`"neutral"`,
            `"info"`, `"success"`, `"warn"`, `"danger"`). Each text goes in a
            light card whose top rule takes the color of the kind.
        number: Section number shown small, in the accent color, to the left
            of the title (e.g. `"01"`, `"02"`). Omit to number automatically.
        footer: Short note (source, closing remark) shown at the bottom of
            the slide in small gray text below a thin rule.
        icon: Icon placed at the right end of the header.
            Pass a dict with keys `"src"` (path, URL, or bytes) and optionally
            `"size"` (CSS height, default `"28px"`).

    Example:
        ```python
        from banners.slides import Section
        from banners.content import Text, Graph

        Section(
            title="Pipeline architecture",
            subtitle="How data flows end to end.",
            number="02",
            content=[
                Text("Each stage is independently versioned and monitored."),
                Graph(\"\"\"
                graph LR
                    A[Ingest] --> B[Transform] --> C[Model] --> D[Serve]
                \"\"\"),
            ],
            footer="All stages emit structured logs to the observability stack.",
        ).render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        content=None,
        palette: SectionPalette | None = None,
        content_kind: "str | None" = None,
        number: "str | None" = None,
        footer: str = "",
        icon: "dict | None" = None,
        background=None,
    ) -> None:
        if palette is None:
            global_palette = _cfg.get("palette")
            palette = global_palette.to_section_palette() if global_palette is not None else SectionPalette()
        elif isinstance(palette, Palette) and not isinstance(palette, SectionPalette):
            palette = palette.to_section_palette()
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette, content_kind, footer, background=background)
        self.number = number if number is not None else _cfg._next_section_number()
        self.icon = icon if icon is not None else _cfg.get("icon")

    def render(self) -> mo.Html:
        """Assemble banner, content, and footer.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        banner = self._render_banner()
        content_parts = self._render_content() + self._render_footer()
        return self._wrap_slide(banner, content_parts)

    def _render_banner(self) -> mo.Html:
        ink, muted, rule = self._ink()
        number_html = (
            f'<div style="font-size:1rem;font-weight:600;letter-spacing:0.04em;color:{self._accent_text()};'
            f'font-variant-numeric:tabular-nums;min-width:2ch;flex-shrink:0;">{self.number}</div>'
            if self.number else ""
        )
        subtitle_html = (
            f'<p style="font-size:1rem;color:{muted};margin:0.35rem 0 0;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        icon_html = self._icon_inline_html(
            self.icon, default_size="28px", style="margin-left:auto;flex-shrink:0;align-self:center;"
        )
        return mo.Html(f"""
        <div style="padding-top:0.5rem;">
            <div style="display:flex;align-items:baseline;gap:1rem;">
                {number_html}
                <div style="flex:1;">
                    <h3 style="font-size:1.75rem;font-weight:600;letter-spacing:-0.01em;line-height:1.2;
                               margin:0;color:{ink};">{self.title}</h3>
                    {subtitle_html}
                </div>
                {icon_html}
            </div>
            {self._accent_rule(rule)}
        </div>
        """)
