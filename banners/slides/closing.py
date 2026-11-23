"""Closing slide — solid title panel with an optional row of metrics."""

import marimo as mo

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


class Closing(Slide):
    """Closing slide with a solid panel and an optional row of metrics.

    Uses the same panel as `Cover`, so the deck opens and closes with the same
    look. Intended as the **last slide** of every presentation. The `stats`
    parameter renders a typographic row of key numbers below the panel.

    Args:
        title: Main closing message. Keep it conclusive and direct.
        subtitle: Support phrase displayed in the panel below the title.
        content: Elements displayed above the stats row. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
        palette: Color palette: `start` fills the panel and `end` is the
            accent. Defaults to the global palette, or `ORANGE`.
        content_kind: Card style for `Text` items in a list (`"neutral"`,
            `"info"`, `"success"`, `"warn"`, `"danger"`). Each text goes in a
            light card whose top rule takes the color of the kind.
        team: Team line shown in small caps at the bottom of the panel.
        stats: List of metric tuples `(value, label, caption)` rendered as
            a horizontal row: label in small caps, large value, gray caption,
            separated by thin vertical rules. Keep `value` short
            (a number, symbol, or 1–3 words). Comfortable range: 2–4 items.
        footer: Short note (source, closing remark) shown at the bottom of
            the slide in small gray text below a thin rule.
        icon: Icon placed at the right end of the team row. Pass a
            dict with keys `"src"` (path, URL, or bytes) and optionally
            `"size"` (CSS height, default `"40px"`).

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
        footer: str = "",
        team: str = "",
        stats: "list[tuple[str, str, str]] | None" = None,
        icon: "dict | None" = None,
        background=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette or _cfg.get("palette"), content_kind, footer, background=background)
        self.team = team or _cfg.get("team", "")
        self.stats = stats
        self.icon = icon if icon is not None else _cfg.get("icon")

    def render(self) -> mo.Html:
        """Assemble banner, content, stats row, and footer.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        template = _cfg.get("template")
        if template is not None:
            return template.render(self)
        banner = self._render_banner()
        content_parts = self._render_content()
        if self.stats:
            content_parts.append(self._render_stats())
        content_parts.extend(self._render_footer())
        return self._wrap_slide(banner, content_parts)

    def _render_stats(self) -> mo.Html:
        """Render `stats` as a typographic row separated by thin vertical rules.

        Returns:
            A `mo.Html` grid with one cell per `(value, label, caption)` tuple.
        """
        ink, muted, rule = self._ink()
        cells = []
        for i, (value, label, caption) in enumerate(self.stats):
            sep = f"border-left:1px solid {rule};" if i else ""
            cells.append(
                f'<div style="padding:1.1rem 1.5rem 1.2rem;{sep}">'
                f'<div style="font-size:0.9rem;font-weight:600;letter-spacing:0.08em;'
                f'text-transform:uppercase;color:{muted};">{label}</div>'
                f'<div style="font-size:2.6rem;font-weight:600;letter-spacing:-0.02em;'
                f'line-height:1.15;color:{ink};font-variant-numeric:tabular-nums;'
                f'margin:0.4rem 0 0.2rem;">{value}</div>'
                f'<div style="font-size:1rem;color:{muted};">{caption}</div></div>'
            )
        return mo.Html(
            f'<div style="display:grid;grid-template-columns:repeat({len(cells)},1fr);'
            f'border-top:1px solid {rule};border-bottom:1px solid {rule};">{"".join(cells)}</div>'
        )

    def _render_banner(self) -> mo.Html:
        p = self.palette
        subtitle_html = (
            f'<p style="font-size:1.2rem;line-height:1.45;color:{p.text_sub};'
            f'margin:1rem 0 0;max-width:50ch;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        icon_html = self._icon_inline_html(self.icon, default_size="40px", style="flex-shrink:0;")
        # The team line and the icon share the bottom row, so the icon never
        # sits on top of the hairline or the text.
        team_html = (
            f'<div style="display:flex;justify-content:space-between;align-items:center;gap:1rem;'
            f'font-size:0.9rem;letter-spacing:0.08em;text-transform:uppercase;'
            f'color:{p.text_muted};margin-top:2.5rem;padding-top:0.9rem;'
            f'border-top:1px solid rgba(255,255,255,0.16);">'
            f'<span>{self.team}</span>{icon_html}</div>'
            if self.team or icon_html else ""
        )
        return mo.Html(f"""
        <div style="position:relative;background:{p.start};color:{p.text_main};
                    padding:3rem 2.75rem 1.5rem;border-radius:3px;margin-bottom:1.75rem;">
            <div style="width:40px;height:3px;background:{p.end};margin-bottom:1.25rem;"></div>
            <h1 style="font-size:2.6rem;font-weight:600;letter-spacing:-0.02em;line-height:1.15;
                       margin:0;max-width:24ch;color:{p.text_main};">{self.title}</h1>
            {subtitle_html}
            {team_html}
        </div>
        """)
