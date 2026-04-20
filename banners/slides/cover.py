"""Cover slide — large centered banner."""

import marimo as mo

from ..slide import Slide
from ..palette import Palette

_TEAM_LINE = "BancoEstado · Analítica Avanzada · Modelos"


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
        team: str = _TEAM_LINE,
        icon: "dict | None" = None,
    ) -> None:
        super().__init__(title, subtitle, content, palette, content_kind)
        self.date = date
        self.team = team
        self.icon = icon

    def _render_banner(self) -> mo.Html:
        p = self.palette
        team_html = self._tag_line(self.team, p.text_tag) if self.team else ""
        subtitle_html = (
            f'<p style="font-size:1.3rem;color:{p.text_sub};margin:1rem 0 0.25rem;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        date_html = (
            f'<p style="font-size:0.9rem;color:{p.text_muted};margin-top:0.5rem;">{self.date}</p>'
            if self.date else ""
        )
        icon_html = self._icon_corner_html(self.icon, bottom="1rem", right="1.5rem", default_size="44px")
        return mo.Html(f"""
        <div style="position:relative;text-align:center;padding:3rem 2rem 1.5rem;
                    background:{p.gradient};border-radius:1rem;color:{p.text_main};margin-bottom:1.5rem;">
            {team_html}
            <h1 style="font-size:3.2rem;font-weight:800;margin:0.5rem 0;color:{p.text_main};line-height:1.15;">{self.title}</h1>
            {subtitle_html}
            {date_html}
            {icon_html}
        </div>
        """)
