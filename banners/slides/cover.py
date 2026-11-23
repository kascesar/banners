"""Cover slide — large centered banner."""

import marimo as mo

from ..slide import Slide
from ..palette import Palette
from .. import config as _cfg


class Cover(Slide):
    """Title slide with a large centered gradient banner.

    Intended as the **first slide** of every presentation.

    Args:
        title: Main project title.
        subtitle: Short context phrase displayed inside the banner.
        date: Date string shown at the bottom of the banner (e.g. `"April 2026"`).
        content: Elements displayed below the banner. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
        palette: Color palette for the banner gradient. Defaults to `ORANGE`.
        content_kind: Box style for `Text` lists (`"neutral"`, `"info"`,
            `"success"`, `"warn"`, `"danger"`).
        team: Team line shown in small caps above the title.
        icon: Institutional icon placed in the bottom-right corner of the
            banner. Pass a dict with keys `"src"` (path, URL, or bytes) and
            optionally `"size"` (CSS height, default `"44px"`).

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
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette or _cfg.get("palette"), content_kind, footer, background=background)
        self.date = date or _cfg.get("date", "")
        self.team = team or _cfg.get("team", "")
        self.icon = icon if icon is not None else _cfg.get("icon")

    def _render_banner(self) -> mo.Html:
        p = self.palette
        meta = "".join(
            f'<span>{t}</span>' for t in (self.team, self.date) if t
        )
        meta_html = (
            f'<div style="display:flex;justify-content:space-between;gap:1rem;'
            f'font-size:0.8rem;letter-spacing:0.08em;text-transform:uppercase;'
            f'color:{p.text_muted};padding-bottom:0.9rem;'
            f'border-bottom:1px solid rgba(255,255,255,0.16);">{meta}</div>'
            if meta else ""
        )
        subtitle_html = (
            f'<p style="font-size:1.25rem;font-weight:400;line-height:1.45;color:{p.text_sub};'
            f'margin:1.1rem 0 0;max-width:46ch;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        icon_html = self._icon_corner_html(self.icon, bottom="1.75rem", right="2.5rem", default_size="40px")
        return mo.Html(f"""
        <div style="position:relative;background:{p.start};color:{p.text_main};
                    padding:1.5rem 2.75rem 3rem;border-radius:3px;margin-bottom:1.75rem;">
            {meta_html}
            <div style="width:40px;height:3px;background:{p.end};margin:3.5rem 0 1.25rem;"></div>
            <h1 style="font-size:3rem;font-weight:600;letter-spacing:-0.02em;line-height:1.1;
                       margin:0;max-width:22ch;color:{p.text_main};">{self.title}</h1>
            {subtitle_html}
            {icon_html}
        </div>
        """)
