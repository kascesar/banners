"""Section slide — left border accent with dark background."""

import marimo as mo

from ..slide import Slide
from ..palette import SectionPalette
from .. import config as _cfg


class Section(Slide):
    """Intermediate section slide with a left color border and dark background.

    Takes less vertical space than `Cover` or `Closing`, leaving more room
    for content. Intended for **all middle slides** of a presentation.

    Args:
        title: Section heading.
        subtitle: Short support phrase shown to the right of the title.
        content: Elements displayed below the banner. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
            Lists that contain any `Image` or `Graph` automatically use
            an equal-width CSS grid layout.
        palette: `SectionPalette` instance controlling the border color and
            dark background gradient. Defaults to the orange `SectionPalette`.
        content_kind: Box style for `Text`-only lists (`"neutral"`, `"info"`,
            `"success"`, `"warn"`, `"danger"`).
        number: Section number displayed large on the left of the banner
            (e.g. `"01"`, `"02"`). Omit to hide.
        footer: Closing quote shown at the bottom of the slide as a blockquote.
        icon: Icon placed at the right end of the banner, vertically centered.
            Pass a dict with keys `"src"` (path, URL, or bytes) and optionally
            `"size"` (CSS height, default `"32px"`).

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
        slide_bg=None,
    ) -> None:
        if palette is None:
            global_palette = _cfg.get("palette")
            palette = global_palette.to_section_palette() if global_palette is not None else SectionPalette()
        super().__init__(title, subtitle, content, palette, content_kind, footer, slide_bg=slide_bg)
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
        p = self.palette
        number_html = (
            f'<div style="font-size:2.5rem;font-weight:900;color:{p.border};'
            f'line-height:1;margin-bottom:0.2rem;opacity:0.85;flex-shrink:0;">{self.number}</div>'
            if self.number else ""
        )
        subtitle_html = (
            f'<p style="font-size:0.95rem;color:{p.text_sub};margin:0.3rem 0 0;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        icon_html = self._icon_inline_html(
            self.icon, default_size="32px", style="margin-left:auto;flex-shrink:0;opacity:0.8;"
        )
        return mo.Html(f"""
        <div style="padding:1.1rem 1.5rem;background:{p.gradient};
                    border-left:5px solid {p.border};border-radius:0 0.5rem 0.5rem 0;
                    color:{p.text_main};margin-bottom:1.25rem;display:flex;align-items:center;gap:1.2rem;">
            {number_html}
            <div style="flex:1;">
                <h3 style="font-size:1.5rem;font-weight:700;margin:0;color:{p.text_main};">{self.title}</h3>
                {subtitle_html}
            </div>
            {icon_html}
        </div>
        """)
