"""Image content element."""

import marimo as mo


class Image:
    """Image element for use inside a slide's content area.

    Wraps marimo's `mo.image`, so it accepts the same source formats:
    a file path (`str` or `Path`), raw `bytes`, or a URL string.

    Args:
        src: Image source — file path, bytes, or URL.
        width: CSS width value applied to the image. Defaults to `"100%"`.
        alt: Alternative text for accessibility. Defaults to `""`.

    Example:
        ```python
        from banners.content import Image

        # From a local path
        Image("img/architecture.png", width="80%")

        # From bytes — more portable across machines
        from pathlib import Path
        Image(Path("img/architecture.png").read_bytes(), width="80%")
        ```
    """

    def __init__(self, src, width: str = "100%", alt: str = "") -> None:
        self.src = src
        self.width = width
        self.alt = alt

    def render(self) -> mo.Html:
        """Render the image as a marimo HTML component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        return mo.image(self.src, width=self.width, alt=self.alt)
