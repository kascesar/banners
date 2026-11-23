"""Intro slide — compact banner for context or problem-statement slides."""

import marimo as mo

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


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
        background=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette or _cfg.get("palette"), content_kind, footer, background=background)
        self.tag = tag
        self.summary = summary
        self.team = team or _cfg.get("team", "")
        self.icon = icon if icon is not None else _cfg.get("icon")

    def render(self) -> mo.Html:
        """Assemble banner, summary block, content, and footer.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        banner = self._render_banner()
        content_parts = []
        if self.summary:
            ink, _, _ = self._ink()
            body = self._md_html(self.summary, ink, size="1.15rem")
            content_parts.append(mo.Html(
                f'<div style="font-size:1.15rem;line-height:1.5;padding:0.15rem 0 0.15rem 1.1rem;'
                f'border-left:3px solid {self._accent()};margin-bottom:0.5rem;">{body}</div>'
            ))
        content_parts.extend(self._render_content())
        content_parts.extend(self._render_footer())
        return self._wrap_slide(banner, content_parts)

    def _render_banner(self) -> mo.Html:
        ink, muted, rule = self._ink()
        label = self.tag if self.tag else self.team
        kicker_html = self._kicker(label, self._accent()) if label else ""
        subtitle_html = (
            f'<p style="font-size:1.1rem;line-height:1.45;color:{muted};margin:0.5rem 0 0;">{self.subtitle}</p>'
            if self.subtitle else ""
        )
        icon_html = self._icon_corner_html(self.icon, bottom="1.75rem", right="0", default_size="32px")
        return mo.Html(f"""
        <div style="position:relative;padding-top:0.5rem;">
            {kicker_html}
            <h2 style="font-size:2.25rem;font-weight:600;letter-spacing:-0.015em;line-height:1.15;
                       margin:0.5rem 0 0;color:{ink};">{self.title}</h2>
            {subtitle_html}
            {icon_html}
            {self._accent_rule(rule, margin="1.25rem 0 1.5rem")}
        </div>
        """)
