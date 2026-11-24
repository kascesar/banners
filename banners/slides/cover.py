"""Cover slide — the first slide of a presentation."""

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


class Cover(Slide):
    """Title slide that opens the presentation.

    The template draws a dark cover with the logo, the team, the title in the
    primary color, the subtitle and the date; with a photo (`image=` or the
    template's `cover_image`) the title sits over the picture.

    Args:
        title: Main project title.
        subtitle: Short context phrase shown under the title.
        date: Date string (e.g. `"April 2026"`). Defaults to `configure(date=...)`.
        content: Kept for compatibility with other slide types; the cover
            layout does not draw it.
        palette: Colors for this slide only. `None` uses the configured or
            the template palette.
        footer: Small note; the cover layout does not draw it.
        team: Team line. Defaults to `configure(team=...)`.
        background: `Background` that paints the canvas. Defaults to
            `configure(background=...)`.
        image: Photo for the cover. `False` hides the template's default
            `cover_image` on this slide.

    Example:
        ```python
        from banners.slides import Cover

        Cover(title="Churn Prediction v2", subtitle="Model migration and deployment.").render()
        ```
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        date: str = "",
        content=None,
        palette: Palette | None = None,
        footer: str = "",
        team: str = "",
        background=None,
        image=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette, footer, background=background)
        self.date = date or _cfg.get("date", "")
        self.team = team or _cfg.get("team", "")
        self.image = image
