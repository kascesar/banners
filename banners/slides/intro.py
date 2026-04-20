"""Intro slide — compact banner for context or problem-statement slides."""

import marimo as mo

from ..slide import Slide
from ..palette import Palette
from .. import config as _cfg


class Intro(Slide):
    """Compact gradient banner for slides that open a thematic block.

    Typically used for slides 2–3 to set context or frame the problem.
    Supports an optional `summary` callout block between the banner and
    the content area, and an optional `footer` blockquote.

    Args:
        title: Slide heading.
        subtitle: Support phrase displayed inside the banner below the title.
        content: Elements displayed below the summary block. Accepts a single
            `Text`, `Image`, or `Graph` instance, or a list of them.
        palette: Color palette for the banner gradient. Defaults to `ORANGE`.
        content_kind: Box style for `Text` lists (`"neutral"`, `"info"`,
            `"success"`, `"warn"`, `"danger"`).
        tag: Short label shown in small caps above the title
            (e.g. `"Context"`, `"Problem"`). Falls back to the team line
            when empty.
        summary: Full-width highlighted block rendered between the banner
            and the content area. Displayed as a yellow `warn` callout.
        footer: Closing quote shown at the bottom of the slide as a blockquote.
        team: Team line used as the tag fallback.
        icon: Icon placed in the bottom-right corner of the banner. Pass a
            dict with keys `"src"` (path, URL, or bytes) and optionally
            `"size"` (CSS height, default `"36px"`).

    Example:
        ```python
        from banners.slides import Intro
        from banners.content import Text

        Intro(
            title="Why we're here",
            subtitle="What was at stake and what motivated this work.",
            tag="Context",
            summary="Models were running on servers with a confirmed shutdown date.",
            content=[
                Text("**Operational risk** — No fallback if the server goes down."),
                Text("**No traceability** — No record of the active version."),
                Text("**Manual process** — Undocumented and person-dependent."),
            ],
            content_kind="warn",
            footer="The question wasn't whether to migrate — but how.",
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
        tag: str = "",
        summary: str = "",
        footer: str = "",
        team: str = "",
        icon: "dict | None" = None,
    ) -> None:
        super().__init__(title, subtitle, content, palette or _cfg.get("palette"), content_kind, footer)
        self.tag = tag
        self.summary = summary
        self.team = team or _cfg.get("team", "")
        self.icon = icon if icon is not None else _cfg.get("icon")

    def render(self) -> mo.Html:
        """Assemble banner, summary callout, content, and footer.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        parts = [self._render_banner()]
        if self.summary:
            parts.append(mo.callout(mo.md(self.summary), kind="warn"))
        parts.extend(self._render_content())
        parts.extend(self._render_footer())
        return mo.vstack(parts)

    def _render_banner(self) -> mo.Html:
        p = self.palette
        label = self.tag if self.tag else self.team
        top_html = self._tag_line(label, p.text_tag)
        subtitle_html = (
            f'<p style="font-size:1.1rem;color:{p.text_sub};margin:0.5rem 0 0;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        icon_html = self._icon_corner_html(self.icon, bottom="0.75rem", right="1.25rem", default_size="36px")
        return mo.Html(f"""
        <div style="position:relative;padding:1.6rem 2rem;background:{p.gradient};
                    border-radius:0.75rem;color:{p.text_main};margin-bottom:1.25rem;">
            {top_html}
            <h2 style="font-size:2rem;font-weight:700;margin:0;color:{p.text_main};line-height:1.2;">{self.title}</h2>
            {subtitle_html}
            {icon_html}
        </div>
        """)
