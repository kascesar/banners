"""Section slide — dividers and content slides in the middle of a presentation."""

from .. import config as _cfg
from ..palette import Palette
from ..slide import Slide


class Section(Slide):
    """Middle slide of a presentation, numbered automatically.

    Without content the template draws a divider (title, subtitle and a photo
    or a large icon). With content it picks a layout from the content: a
    visual next to text, a photo next to the content, or the title on top
    and the content in columns below.

    Sections number themselves when they are created (`"01"`, `"02"`, …), so
    the order of the notebook cells matters; `configure()` resets the count.

    Args:
        title: Section heading.
        subtitle: Short support phrase shown under the title.
        content: Elements of the slide: a single element or a list.
        palette: Colors for this slide only. `None` uses the configured or
            the template palette.
        number: Section number (e.g. `"02"`). Omit to number automatically.
        footer: Short note (source, closing remark) shown at the bottom right.
        background: `Background` that paints the canvas. Defaults to
            `configure(background=...)`.
        image: Photo for the slide: on the right half of a divider, or on the
            left half of a content slide. `False` hides the template's
            default `divider_image` on this slide.

    Example:
        ```python
        from banners.slides import Section
        from banners.content import Text, Graph

        Section(
            title="Pipeline architecture",
            content=[
                Graph("graph LR\\n  A[Ingest] --> B[Transform] --> C[Serve]"),
                Text("Each stage is independently versioned and monitored."),
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
        number: "str | None" = None,
        footer: str = "",
        background=None,
        image=None,
    ) -> None:
        background = background if background is not None else _cfg.get("background")
        super().__init__(title, subtitle, content, palette, footer, background=background)
        self.number = number if number is not None else _cfg._next_section_number()
        self.image = image
