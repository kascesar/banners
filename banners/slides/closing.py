"""Closing slide — the last slide of a presentation."""

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


class Closing(Slide):
    """Closing slide with the final message and an optional row of metrics.

    The template draws it on the closing background. With `title=""` it shows
    only the centered logo and the team.

    Args:
        title: Main closing message. Keep it conclusive and direct.
        subtitle: Support phrase shown under the title.
        content: Kept for compatibility with other slide types; the closing
            layout does not draw it.
        palette: Colors for this slide only. `None` uses the configured or
            the template palette.
        footer: Small note; the closing layout does not draw it.
        team: Team line. Defaults to `configure(team=...)`.
        stats: Metric tuples `(value, label, caption)` shown as a row above
            the title. Keep `value` short; 2–4 items read best.
        background: `Background` that paints the canvas. Defaults to
            `configure(background=...)`.

    Example:
        ```python
        from banners.slides import Closing

        Closing(
            title="One framework for all models.",
            stats=[("100%", "Traceability", "End to end"), ("1", "Shared codebase", "Everyone contributes")],
        ).render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        content=None,
        palette: Palette | None = None,
        footer: str = "",
        team: str = "",
        stats: "list[tuple[str, str, str]] | None" = None,
        background=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette, footer, background=background)
        self.team = team or _cfg.get("team", "")
        self.stats = stats
