"""Cover slide — solid, left-aligned title panel."""

import marimo as mo

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


class Cover(Slide):
    """Title slide with a solid, left-aligned panel in the palette's `start` color.

    The panel shows the team and the date in a top row, a short accent bar,
    the title and the subtitle.

    Intended as the **first slide** of every presentation.

    Args:
        title: Main project title.
        subtitle: Short context phrase displayed inside the banner.
        date: Date string shown at the top right of the panel (e.g. `"April 2026"`).
        content: Elements displayed below the banner. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
        palette: Color palette: `start` fills the panel and `end` is the
            accent. Defaults to the global palette, or `ORANGE`.
        content_kind: Card style for `Text` items in a list (`"neutral"`,
            `"info"`, `"success"`, `"warn"`, `"danger"`). Each text goes in a
            light card whose top rule takes the color of the kind.
        team: Team line shown in small caps at the top left of the panel.
        icon: Institutional icon placed at the right of the title block. Pass a dict with keys `"src"` (path, URL, or bytes) and
            optionally `"size"` (CSS height, default `"40px"`).
        image: Photo for the cover. Only used by a `Template` (photo cover
            layout); ignored by the default editorial style.

    Example:
        ```python
        from banners.slides import Cover
        from banners.content import Text
        from banners.palette import BLUE

        Cover(
            title="Churn Prediction v2",
            subtitle="Model migration and deployment.",
            date="April 2026",
            palette=BLUE,
            content=[
                Text("**Accuracy** — 91% AUC on holdout."),
                Text("**Latency** — p99 under 30 ms."),
                Text("**Coverage** — All active segments."),
            ],
            content_kind="neutral",
        ).render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        date: str = "",
        content=None,
        palette: Palette | None = None,
        content_kind: "str | None" = None,
        footer: str = "",
        team: str = "",
        icon: "dict | None" = None,
        background=None,
        image=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette or _cfg.get("palette"), content_kind, footer, background=background)
        self.date = date or _cfg.get("date", "")
        self.team = team or _cfg.get("team", "")
        self.icon = icon if icon is not None else _cfg.get("icon")
        self.image = image

    def _render_banner(self) -> mo.Html:
        p = self.palette
        meta = "".join(
            f'<span>{t}</span>' for t in (self.team, self.date) if t
        )
        meta_html = (
            f'<div style="display:flex;justify-content:space-between;gap:1rem;'
            f'font-size:0.9rem;letter-spacing:0.08em;text-transform:uppercase;'
            f'color:{p.text_muted};padding-bottom:0.9rem;'
            f'border-bottom:1px solid rgba(255,255,255,0.16);">{meta}</div>'
            if meta else ""
        )
        subtitle_html = (
            f'<p style="font-size:1.25rem;font-weight:400;line-height:1.45;color:{p.text_sub};'
            f'margin:1.1rem 0 0;max-width:46ch;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        # The icon sits in its own flex column, so a long title or subtitle wraps
        # before reaching it instead of running underneath.
        icon_html = self._icon_inline_html(
            self.icon, default_size="40px", style="flex-shrink:0;align-self:flex-end;"
        )
        return mo.Html(f"""
        <div style="background:{p.start};color:{p.text_main};
                    padding:1.5rem 2.75rem 3rem;border-radius:3px;margin-bottom:1.75rem;">
            {meta_html}
            <div style="display:flex;gap:2rem;">
                <div style="flex:1;min-width:0;">
                    <div style="width:40px;height:3px;background:{p.end};margin:3.5rem 0 1.25rem;"></div>
                    <h1 style="font-size:3rem;font-weight:600;letter-spacing:-0.02em;line-height:1.1;
                               margin:0;max-width:22ch;color:{p.text_main};">{self.title}</h1>
                    {subtitle_html}
                </div>
                {icon_html}
            </div>
        </div>
        """)
