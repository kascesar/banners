"""Background — per-slide background for banners presentations."""

import re
from dataclasses import dataclass


_NAMED_COLORS = {
    "white": (255, 255, 255), "black": (0, 0, 0),
    "red": (255, 0, 0), "green": (0, 128, 0), "blue": (0, 0, 255),
    "yellow": (255, 255, 0), "cyan": (0, 255, 255), "magenta": (255, 0, 255),
    "gray": (128, 128, 128), "grey": (128, 128, 128),
    "silver": (192, 192, 192), "navy": (0, 0, 128), "teal": (0, 128, 128),
    "maroon": (128, 0, 0), "purple": (128, 0, 128), "orange": (255, 165, 0),
    "pink": (255, 192, 203), "transparent": (0, 0, 0),
}


def _parse_first_color(css: str):
    # Named color (e.g. "white", "black")
    key = css.strip().lower()
    if key in _NAMED_COLORS:
        return _NAMED_COLORS[key]

    # 8-digit hex  #rrggbbaa  (take RGB, ignore alpha)
    m = re.search(r'#([0-9a-fA-F]{8})', css)
    if m:
        h = m.group(1)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    # 6-digit hex  #rrggbb
    m = re.search(r'#([0-9a-fA-F]{6})', css)
    if m:
        h = m.group(1)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    # 4-digit hex  #rgba  → expand RGB channels
    m = re.search(r'#([0-9a-fA-F]{4})(?![0-9a-fA-F])', css)
    if m:
        h = m.group(1)
        return int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16)

    # 3-digit hex  #rgb  → expand to #rrggbb
    m = re.search(r'#([0-9a-fA-F]{3})(?![0-9a-fA-F])', css)
    if m:
        h = m.group(1)
        return int(h[0] * 2, 16), int(h[1] * 2, 16), int(h[2] * 2, 16)

    # rgb() / rgba()  — handles integers (0-255) and floats (0.0-1.0 / 0-255)
    m = re.search(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)', css)
    if m:
        vals = [float(m.group(i)) for i in (1, 2, 3)]
        if all(v <= 1.0 for v in vals):   # 0-1 range → scale to 0-255
            vals = [v * 255 for v in vals]
        return int(vals[0]), int(vals[1]), int(vals[2])

    return None


def _relative_luminance(r, g, b) -> float:
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


@dataclass
class Background:
    """Encapsulates a CSS background value for use as a slide backdrop.

    Do not instantiate directly — use the factory methods:

    - :meth:`color` — solid color
    - :meth:`gradient` — linear gradient
    - :meth:`image` — image with optional dark overlay

    Args:
        css: Ready-to-use CSS value for the ``background`` property.
    """

    css: str

    @staticmethod
    def color(c: str) -> "Background":
        """Solid background color.

        Args:
            c: Any CSS color value (hex, rgb, named).

        Example::

            Background.color("#0f172a")
        """
        return Background(css=c)

    @staticmethod
    def gradient(
        start: str,
        end: str,
        *,
        mid: str = None,
        angle: int = 135,
    ) -> "Background":
        """Linear gradient background.

        Args:
            start: Start color (0%).
            end: End color (100%).
            mid: Optional mid-stop color (50%).
            angle: Gradient angle in degrees. Defaults to 135.

        Example::

            Background.gradient("#0d1b2a", "#4a1a6e")
            Background.gradient("#0d1b2a", "#4a1a6e", mid="#1a2a5e", angle=45)
        """
        if mid:
            return Background(
                css=f"linear-gradient({angle}deg,{start} 0%,{mid} 50%,{end} 100%)"
            )
        return Background(css=f"linear-gradient({angle}deg,{start} 0%,{end} 100%)")

    @staticmethod
    def image(src, *, overlay: str = "rgba(0,0,0,0.55)") -> "Background":
        """Image background, with an optional dark overlay for text legibility.

        Args:
            src: File path (``str`` / ``Path``), URL, or raw ``bytes``.
            overlay: CSS color applied as a semi-transparent layer on top of
                the image. Defaults to ``"rgba(0,0,0,0.55)"``. Pass ``None``
                to disable the overlay entirely.

        Example::

            Background.image("assets/photo.jpg")
            Background.image("https://example.com/bg.jpg", overlay="rgba(0,0,0,0.7)")
            Background.image(raw_bytes, overlay=None)
        """
        from banners.slide import Slide
        data_uri = Slide._icon_src(src)
        img_css = f"url({data_uri}) center/cover no-repeat"
        if overlay:
            return Background(css=f"linear-gradient({overlay},{overlay}),{img_css}")
        return Background(css=img_css)

    def text_color(self) -> "str | None":
        """Return a contrasting text color based on the background luminance.

        Returns ``"#ffffff"`` for dark backgrounds, ``"#1f2937"`` for light
        ones, using the WCAG relative luminance formula. Returns ``None`` when
        the color cannot be parsed (unrecognized format) — in that case no
        automatic color is applied.
        """
        rgb = _parse_first_color(self.css)
        if rgb is None:
            return None
        lum = _relative_luminance(*rgb)
        return "#ffffff" if lum < 0.2 else "#1f2937"
