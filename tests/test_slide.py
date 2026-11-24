"""Tests for `Slide`: rendering through the template and standalone content elements."""

from pathlib import Path

import banners
from banners import Text, configure
from banners.content import AnimatedGraph, Graph
from banners.slides import Cover


def test_default_template_without_configure():
    """With no template configured, slides render on the default 16:9 canvas."""
    configure(template=None)
    assert "aspect-ratio:16/9" in Cover(title="A").render().text


def test_display_returns_render():
    """`_display_` shows the same canvas as `render()`."""
    slide = Cover(title="A")
    assert slide._display_().text == slide.render().text


def test_content_elements_render_without_configure():
    """Content elements render in a plain cell, with no slide or configuration."""
    assert Text("**a**").render() is not None
    assert Graph("graph LR\n A-->B").render() is not None
    assert AnimatedGraph("graph LR\n A-->B").render() is not None


def test_content_elements_do_not_import_config():
    """No file in `banners/content/` imports slides or `banners.config`."""
    content_dir = Path(banners.__file__).parent / "content"
    for path in content_dir.glob("*.py"):
        source = path.read_text()
        assert "from .." not in source, path.name
        assert "banners.config" not in source, path.name
