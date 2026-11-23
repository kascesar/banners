"""Pruebas del despacho de contenido y del layout de `Slide`."""

import marimo as mo

from banners import Slide, Text


class _Renderable:
    """Objeto de prueba con un método `render()`, como los elementos de `banners.content`."""

    def render(self):
        """Devuelve un componente reconocible.

        Returns:
            `mo.Html` con el texto "rendered".
        """
        return mo.Html("<b>rendered</b>")


def _html(component) -> str:
    """Devuelve el HTML de un componente marimo.

    Args:
        component: Cualquier objeto que `mo.as_html` acepte.

    Returns:
        El HTML del componente como string.
    """
    return mo.as_html(component).text


def test_render_item_str_is_markdown():
    """Un `str` se renderiza como markdown."""
    assert "<strong>hola</strong>" in _html(Slide("t")._render_item("**hola**"))


def test_render_item_text_is_markdown():
    """Un `Text` se renderiza como markdown."""
    assert "<strong>hola</strong>" in _html(Slide("t")._render_item(Text("**hola**")))


def test_render_item_text_is_dedented():
    """Un `Text` con indentación de triple comilla no se vuelve bloque de código."""
    body = """
        **hola**
    """
    assert "<strong>hola</strong>" in _html(Slide("t")._render_item(Text(body)))


def test_render_item_wrap_kind_uses_card():
    """Con `wrap_kind`, el texto va en una tarjeta cuyo borde superior tiene el color del tipo."""
    html = _html(Slide("t")._render_item("hola", wrap_kind="info"))
    assert "border-top:2px solid #2f6fd0" in html
    assert "marimo-callout" not in html


def test_render_item_calls_render():
    """Un objeto con `.render()` se renderiza llamando a ese método."""
    assert "rendered" in _html(Slide("t")._render_item(_Renderable()))


def test_render_item_passthrough():
    """Un objeto sin `.render()` se devuelve tal cual."""
    obj = mo.Html("<i>x</i>")
    assert Slide("t")._render_item(obj) is obj


def test_render_content_none():
    """Sin contenido no se agregan componentes."""
    assert Slide("t")._render_content() == []


def test_render_content_single_item_full_width():
    """Un único elemento (solo o en lista) se renderiza sin grilla."""
    for content in ("hola", ["hola"]):
        parts = Slide("t", content=content)._render_content()
        assert len(parts) == 1
        assert "grid-template-columns" not in _html(parts[0])


def test_render_content_n_items_grid():
    """N elementos se ponen en una grilla de N columnas iguales."""
    parts = Slide("t", content=["a", "b", _Renderable()])._render_content()
    assert len(parts) == 1
    html = _html(parts[0])
    assert "grid-template-columns:1fr 1fr 1fr;" in html
    assert "rendered" in html


def test_render_content_kind_wraps_only_text():
    """`content_kind` envuelve el texto en tarjetas y deja intactos los demás elementos."""
    html = _html(Slide("t", content=["a", _Renderable()], content_kind="warn")._render_content()[0])
    assert html.count("border-top:2px solid") == 1
