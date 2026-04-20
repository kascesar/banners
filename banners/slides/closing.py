"""Closing slide — large centered banner with optional metrics."""

import marimo as mo

from ..slide import Slide
from ..palette import Palette

_TEAM_LINE = "team"


class Closing(Slide):
    """Closing slide with a large centered banner and an optional metrics row.

    Same visual weight as `Cover`. Intended as the **last slide** of every
    presentation. The `stats` parameter renders a row of `mo.stat` boxes
    useful for summarizing key numbers.

    Args:
        title: Main closing message. Keep it conclusive and direct.
        subtitle: Support phrase displayed inside the banner below the title.
        content: Elements displayed above the stats row. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
        palette: Color palette for the banner gradient. Defaults to `ORANGE`.
        content_kind: Box style for `Text` lists (`"neutral"`, `"info"`,
            `"success"`, `"warn"`, `"danger"`).
        team: Team line shown in small caps at the bottom of the banner.
        stats: List of metric tuples `(value, label, caption)` rendered as
            a horizontal row of bordered `mo.stat` boxes. Keep `value` short
            (a number, symbol, or 1–3 words). Comfortable range: 2–4 items.
        footer: Closing quote shown at the bottom of the slide as a blockquote.
        icon: Icon placed in the bottom-right corner of the banner. Pass a
            dict with keys `"src"` (path, URL, or bytes) and optionally
            `"size"` (CSS height, default `"44px"`).

    Example:
        ```python
        from banners.slides import Closing

        Closing(
            title="One framework for all models.",
            subtitle="Infrastructure solved. Team focuses on data science.",
            stats=[
                ("Low",   "Effort per new model", "Just configure data"),
                ("↑ ROI", "Cumulative return",     "Each migration amortizes more"),
                ("100%",  "Traceability",          "Automatic end-to-end tracking"),
                ("1",     "Shared codebase",       "Everyone contributes"),
            ],
        ).render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        content=None,
        palette: Palette | None = None,
        content_kind: "str | None" = None,
        team: str = _TEAM_LINE,
        stats: "list[tuple[str, str, str]] | None" = None,
        footer: str = "",
        icon: "dict | None" = None,
    ) -> None:
        super().__init__(title, subtitle, content, palette, content_kind)
        self.team = team
        self.stats = stats
        self.footer = footer
        self.icon = icon

    def render(self) -> mo.Html:
        """Assemble banner, content, stats row, and footer.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        parts = [self._render_banner()]
        parts.extend(self._render_content())
        if self.stats:
            parts.append(
                mo.hstack(
                    [mo.stat(v, label=l, caption=c, bordered=True) for v, l, c in self.stats],
                    justify="space-around",
                )
            )
        if self.footer:
            parts.append(mo.md(f"> {self.footer}"))
        return mo.vstack(parts)

    def _render_banner(self) -> mo.Html:
        p = self.palette
        subtitle_html = (
            f'<p style="font-size:1.2rem;color:{p.text_sub};margin:1rem 0 1.5rem;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        team_html = (
            f'<div style="font-size:0.78rem;letter-spacing:0.15em;text-transform:uppercase;'
            f'color:{p.text_muted};margin-top:1rem;">{self.team}</div>'
            if self.team else ""
        )
        icon_html = self._icon_corner_html(self.icon, bottom="1rem", right="1.5rem", default_size="44px")
        return mo.Html(f"""
        <div style="position:relative;text-align:center;padding:3rem 2rem 2rem;
                    background:{p.gradient};border-radius:1rem;color:{p.text_main};margin-bottom:1.5rem;">
            <h1 style="font-size:2.6rem;font-weight:800;color:{p.text_main};margin-bottom:0.5rem;line-height:1.2;">{self.title}</h1>
            {subtitle_html}
            {team_html}
            {icon_html}
        </div>
        """)
