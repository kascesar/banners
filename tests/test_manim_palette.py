"""Tests for `Manim` following the slide palette, scene factories and the player colors."""

import base64
import io
import re

import pytest

from banners import BLUE, Palette
from banners.content import Manim


class DummyScene:
    """Stand-in for a manim `Scene` class in tests that do not render."""


def decoded_player(html: str) -> str:
    """Decode the HTML document embedded in the player iframe.

    Args:
        html: HTML of the `mo.Html` returned by `Manim._build_iframe_player`.

    Returns:
        The decoded HTML document of the iframe.
    """
    b64 = re.search(r"data:text/html;base64,([A-Za-z0-9+/=]+)", html).group(1)
    return base64.b64decode(b64).decode()


def first_png_pixel(html: str) -> tuple:
    """Read the top-left pixel of the first PNG embedded in some HTML.

    Args:
        html: HTML that contains a `data:image/png;base64,...` image.

    Returns:
        The `(r, g, b)` color of pixel (0, 0).
    """
    from PIL import Image

    b64 = re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", html).group(1)
    return Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB").getpixel((0, 0))


def test_with_palette_returns_copy():
    """`_with_palette` returns a styled copy and leaves the original alone."""
    m = Manim(DummyScene)
    m2 = m._with_palette(BLUE)
    assert m2.palette is BLUE
    assert m.palette is None


def test_palette_changes_cache_key():
    """A render made with another palette is not reused."""
    assert Manim(DummyScene)._cache_key() != Manim(DummyScene)._with_palette(BLUE)._cache_key()


def test_factory_receives_palette():
    """A scene factory is called with the palette when it accepts one."""
    seen = []

    def factory(palette=None):
        seen.append(palette)
        return DummyScene

    assert Manim(factory)._with_palette(BLUE)._scene_class() is DummyScene
    assert seen == [BLUE]

    def plain_factory():
        return DummyScene

    assert Manim(plain_factory)._scene_class() is DummyScene


def test_player_uses_palette_colors():
    """The player page uses the palette colors instead of a black stage."""
    colors = {"panel": "#101010", "muted": "#202020", "primary": "#303030"}
    page = decoded_player(Manim._build_iframe_player(["x"], "100%", False, colors).text)
    assert "#101010" in page
    assert "background:#000" not in page


@pytest.mark.manim
def test_background_is_panel():
    """A banners render paints `palette.panel` behind the scene."""
    from manim import Circle, Create, Scene

    class OneShape(Scene):
        def construct(self):
            self.play(Create(Circle(radius=0.5)), run_time=0.1)

    m = Manim(OneShape, format="png")._with_palette(Palette(panel="#123456"))
    assert first_png_pixel(m.render().text) == (0x12, 0x34, 0x56)


@pytest.mark.manim
def test_scene_background_override_is_kept():
    """A scene that sets its own background keeps it."""
    from manim import Circle, Create, Scene

    class OwnBackground(Scene):
        def construct(self):
            self.camera.background_color = "#654321"
            self.play(Create(Circle(radius=0.5)), run_time=0.1)

    m = Manim(OwnBackground, format="png")._with_palette(Palette(panel="#123456"))
    assert first_png_pixel(m.render().text) == (0x65, 0x43, 0x21)


@pytest.mark.manim
def test_pipeline_scene_renders_sections():
    """`Manim(PipelineScene, interactive=True)` renders one video per section: title + 6 stages."""
    from banners.scenes import PipelineScene

    m = Manim(PipelineScene, interactive=True)
    m.render()
    assert len(list((Manim._cache_root() / m._cache_key()).glob("*.mp4"))) == 7
