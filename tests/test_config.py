"""Pruebas de la configuración global (`banners.config`) y de la numeración de `Section`."""

from banners import BLUE, Background, Section, config, configure


def test_configure_sets_passed_values():
    """`configure()` guarda los valores que recibe."""
    configure(team="Equipo", date="Abril 2026", palette=BLUE)
    assert config.get("team") == "Equipo"
    assert config.get("date") == "Abril 2026"
    assert config.get("palette") is BLUE


def test_configure_keeps_values_not_passed():
    """Un argumento omitido no sobrescribe el valor configurado antes."""
    configure(team="Equipo", date="Abril 2026")
    configure(date="Mayo 2026")
    assert config.get("team") == "Equipo"
    assert config.get("date") == "Mayo 2026"


def test_configure_accepts_explicit_none():
    """`None` explícito sí borra el valor, a diferencia de omitir el argumento."""
    bg = Background.color("#000000")
    configure(background=bg)
    assert config.get("background") is bg
    configure(background=None)
    assert config.get("background") is None


def test_get_returns_default_for_unknown_key():
    """`get()` devuelve el valor por defecto si la clave no existe."""
    assert config.get("no_existe", "x") == "x"


def test_next_section_number_is_zero_padded_sequence():
    """`_next_section_number()` entrega "01", "02", ... a partir del contador."""
    configure()
    assert [config._next_section_number() for _ in range(3)] == ["01", "02", "03"]


def test_next_section_number_two_digits_past_nine():
    """El número sigue creciendo después de "09"."""
    configure()
    numbers = [config._next_section_number() for _ in range(11)]
    assert numbers[8:] == ["09", "10", "11"]


def test_configure_resets_section_counter():
    """Cada llamada a `configure()` reinicia el contador, aunque no reciba argumentos."""
    configure()
    config._next_section_number()
    config._next_section_number()
    configure()
    assert config._next_section_number() == "01"


def test_section_auto_numbers_consecutively():
    """Las secciones creadas una tras otra se numeran en orden."""
    configure()
    assert [Section(title=f"S{i}").number for i in range(3)] == ["01", "02", "03"]


def test_section_numbering_restarts_after_configure():
    """Después de `configure()` la siguiente sección vuelve a ser "01"."""
    configure()
    Section(title="A")
    Section(title="B")
    configure()
    assert Section(title="C").number == "01"


def test_section_explicit_number_does_not_advance_counter():
    """Un número explícito no consume un número del contador."""
    configure()
    assert Section(title="A", number="99").number == "99"
    assert Section(title="B").number == "01"
