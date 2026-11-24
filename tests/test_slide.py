"""Tests for content dispatch and layout of `Slide`."""

import marimo as mo

from banners import Slide, Text


class _Renderable:
    """Test object with a `render()` method, like the elements in `banners.content`."""

    def render(self):
        """Return a recognizable component.

        Returns:
            `mo.Html` with the text "rendered".
        """
        return mo.Html("<b>rendered</b>")


def _html(component) -> str:
    """Return the HTML of a marimo component.

    Args:
        component: Any object accepted by `mo.as_html`.

    Returns:
        The HTML of the component as a string.
    """
    return mo.as_html(component).text


def test_render_item_str_is_markdown():
    """A `str` is rendered as markdown."""
    assert "<strong>hello</strong>" in _html(Slide("t")._render_item("**hello**"))


def test_render_item_text_is_markdown():
    """A `Text` is rendered as markdown."""
    assert "<strong>hello</strong>" in _html(Slide("t")._render_item(Text("**hello**")))


def test_render_item_text_is_dedented():
    """A `Text` with triple-quote indentation does not become a code block."""
    body = """
        **hello**
    """
    assert "<strong>hello</strong>" in _html(Slide("t")._render_item(Text(body)))


def test_render_item_wrap_kind_uses_card():
    """With `wrap_kind`, the text goes in a card whose top border has the kind color."""
    html = _html(Slide("t")._render_item("hello", wrap_kind="info"))
    assert "border-top:2px solid #2f6fd0" in html
    assert "marimo-callout" not in html


def test_render_item_calls_render():
    """An object with `.render()` is rendered by calling that method."""
    assert "rendered" in _html(Slide("t")._render_item(_Renderable()))


def test_render_item_passthrough():
    """An object without `.render()` is returned as is."""
    obj = mo.Html("<i>x</i>")
    assert Slide("t")._render_item(obj) is obj


def test_render_content_none():
    """Without content no components are added."""
    assert Slide("t")._render_content() == []


def test_render_content_single_item_full_width():
    """A single item (alone or in a list) is rendered without a grid."""
    for content in ("hello", ["hello"]):
        parts = Slide("t", content=content)._render_content()
        assert len(parts) == 1
        assert "grid-template-columns" not in _html(parts[0])


def test_render_content_n_items_grid():
    """N items go in a grid of N equal columns."""
    parts = Slide("t", content=["a", "b", _Renderable()])._render_content()
    assert len(parts) == 1
    html = _html(parts[0])
    assert "grid-template-columns:1fr 1fr 1fr;" in html
    assert "rendered" in html


def test_render_content_kind_wraps_only_text():
    """`content_kind` wraps text in cards and leaves the other items untouched."""
    html = _html(Slide("t", content=["a", _Renderable()], content_kind="warn")._render_content()[0])
    assert html.count("border-top:2px solid") == 1
