"""Intro slide — opens a thematic block (context, problem statement)."""

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


class Intro(Slide):
    """Slide that frames a block: large title on the left, content on the right.

    Typically used for slides 2–3 to set context or frame the problem.

    Args:
        title: Slide heading.
        subtitle: Support phrase shown under the title.
        content: Elements shown in the right column, side by side.
        palette: Colors for this slide only. `None` uses the configured or
            the template palette.
        tag: Short label shown under the title when there is no subtitle
            (e.g. `"Context"`).
        summary: Key sentence shown in bold above the content. Markdown is
            supported.
        footer: Short note (source, closing remark) shown at the bottom right.
        team: Team line. Defaults to `configure(team=...)`.
        background: `Background` that paints the canvas. Defaults to
            `configure(background=...)`.

    Example:
        ```python
        from banners.slides import Intro
        from banners.content import Text

        Intro(
            title="Why we're here",
            tag="Context",
            summary="Models were running on servers with a confirmed shutdown date.",
            content=[Text("**Operational risk** — No fallback."), Text("**Manual process** — Undocumented.")],
        ).render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        content=None,
        palette: Palette | None = None,
        tag: str = "",
        summary: str = "",
        footer: str = "",
        team: str = "",
        background=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette, footer, background=background)
        self.tag = tag
        self.summary = summary
        self.team = team or _cfg.get("team", "")
