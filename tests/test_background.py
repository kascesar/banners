"""Pruebas de los fondos (`banners.background`): lectura de colores y contraste del texto."""

import pytest

from banners.background import Background, _parse_first_color


@pytest.mark.parametrize(
    ("css", "expected"),
    [
        ("white", (255, 255, 255)),
        ("  Navy ", (0, 0, 128)),
        ("#abc", (0xAA, 0xBB, 0xCC)),
        ("#abcd", (0xAA, 0xBB, 0xCC)),
        ("#a1b2c3", (0xA1, 0xB2, 0xC3)),
        ("#a1b2c3ff", (0xA1, 0xB2, 0xC3)),
        ("rgb(10, 20, 30)", (10, 20, 30)),
        ("rgba(10,20,30,0.5)", (10, 20, 30)),
        ("rgb(0.0, 0.5, 1.0)", (0, 127, 255)),
    ],
)
def test_parse_first_color_formats(css, expected):
    """`_parse_first_color` reconoce nombres, hex de 3/4/6/8 dígitos y rgb()/rgba()."""
    assert _parse_first_color(css) == expected


def test_parse_first_color_gradient_first_wins():
    """En un gradiente con colores del mismo formato se toma el primero."""
    css = "linear-gradient(135deg,#0f172a 0%,#ffffff 100%)"
    assert _parse_first_color(css) == (0x0F, 0x17, 0x2A)


@pytest.mark.xfail(
    reason="Busca cada formato en todo el string en orden fijo (#rrggbb antes que #rgb "
    "y rgb()), así que con formatos mezclados no gana el primer color. Ver Backlog.",
    strict=True,
)
def test_parse_first_color_gradient_mixed_formats_first_wins():
    """Con formatos mezclados también debería ganar el primer color del gradiente."""
    assert _parse_first_color("linear-gradient(#fff 0%, #000000 100%)") == (255, 255, 255)


@pytest.mark.parametrize("css", ["", "url(foo.png)", "var(--bg)", "not-a-color"])
def test_parse_first_color_unparseable_returns_none(css):
    """Un valor sin color reconocible devuelve `None`."""
    assert _parse_first_color(css) is None


@pytest.mark.parametrize("css", ["#000000", "black", "#0f172a", "navy"])
def test_text_color_white_on_dark(css):
    """Sobre un fondo oscuro el texto es blanco."""
    assert Background.color(css).text_color() == "#ffffff"


@pytest.mark.parametrize("css", ["#ffffff", "white", "#f3f4f6", "yellow"])
def test_text_color_dark_on_light(css):
    """Sobre un fondo claro el texto es gris oscuro."""
    assert Background.color(css).text_color() == "#1f2937"


def test_text_color_none_when_unparseable():
    """Si el color no se puede leer, no se propone color de texto."""
    assert Background.color("var(--bg)").text_color() is None


def test_gradient_css_with_and_without_mid():
    """`Background.gradient` agrega el color intermedio solo si se entrega."""
    assert Background.gradient("#000", "#fff").css == "linear-gradient(135deg,#000 0%,#fff 100%)"
    assert (
        Background.gradient("#000", "#fff", mid="#888", angle=45).css
        == "linear-gradient(45deg,#000 0%,#888 50%,#fff 100%)"
    )
