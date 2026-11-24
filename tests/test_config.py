"""Tests for the global configuration (`banners.config`) and `Section` numbering."""

from banners import BLUE, Background, Section, config, configure


def test_configure_sets_passed_values():
    """`configure()` stores the values it receives."""
    configure(team="Team", date="April 2026", palette=BLUE)
    assert config.get("team") == "Team"
    assert config.get("date") == "April 2026"
    assert config.get("palette") is BLUE


def test_configure_keeps_values_not_passed():
    """An omitted argument does not overwrite a previously configured value."""
    configure(team="Team", date="April 2026")
    configure(date="May 2026")
    assert config.get("team") == "Team"
    assert config.get("date") == "May 2026"


def test_configure_accepts_explicit_none():
    """An explicit `None` clears the value, unlike omitting the argument."""
    bg = Background.color("#000000")
    configure(background=bg)
    assert config.get("background") is bg
    configure(background=None)
    assert config.get("background") is None


def test_get_returns_default_for_unknown_key():
    """`get()` returns the default when the key does not exist."""
    assert config.get("missing", "x") == "x"


def test_next_section_number_is_zero_padded_sequence():
    """`_next_section_number()` yields "01", "02", ... from the counter."""
    configure()
    assert [config._next_section_number() for _ in range(3)] == ["01", "02", "03"]


def test_next_section_number_two_digits_past_nine():
    """The number keeps growing past "09"."""
    configure()
    numbers = [config._next_section_number() for _ in range(11)]
    assert numbers[8:] == ["09", "10", "11"]


def test_configure_resets_section_counter():
    """Every call to `configure()` resets the counter, even with no arguments."""
    configure()
    config._next_section_number()
    config._next_section_number()
    configure()
    assert config._next_section_number() == "01"


def test_section_auto_numbers_consecutively():
    """Sections created one after another are numbered in order."""
    configure()
    assert [Section(title=f"S{i}").number for i in range(3)] == ["01", "02", "03"]


def test_section_numbering_restarts_after_configure():
    """After `configure()` the next section is "01" again."""
    configure()
    Section(title="A")
    Section(title="B")
    configure()
    assert Section(title="C").number == "01"


def test_section_explicit_number_does_not_advance_counter():
    """An explicit number does not consume a counter number."""
    configure()
    assert Section(title="A", number="99").number == "99"
    assert Section(title="B").number == "01"
