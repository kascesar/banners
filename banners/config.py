"""Global presentation configuration."""

_state: dict = {
    "team": "",
    "date": "",
    "palette": None,
    "theme": None,
    "background": None,
    "template": None,
    "_section_counter": 0,
}

_UNSET = object()


def configure(
    team: str = _UNSET,
    date: str = _UNSET,
    palette=_UNSET,
    theme=_UNSET,
    background=_UNSET,
    template=_UNSET,
) -> None:
    """Set global defaults shared by all slides and reset the section counter.

    Call this once at the top of the notebook. Any slide parameter left at its
    default will inherit the value set here. Calling `configure()` without
    arguments only resets the section counter.

    Args:
        team: Team line shown in `Cover`, `Intro`, and `Closing` banners.
        date: Date string shown in `Cover` (e.g. `"April 2026"`).
        palette: `Palette` for every slide (e.g. `BLUE`). It replaces the
            template's palette as a whole; a slide's own `palette=` replaces
            it in turn. `None` uses the template's palette.
        theme: `Theme` for every slide (fonts, title weight, icon stroke,
            scale). It replaces the template's theme as a whole. `None` uses
            the template's theme.
        background: Background applied to all slides. Pass a `Background`
            instance (`Background.color()`, `Background.gradient()`, or
            `Background.image()`). Individual slides can override this with
            their own `background` argument.
        template: The `Template` that draws every slide on the 16:9 canvas.
            `None` uses a default `Template()`.

    Example:
        ```python
        from banners import configure, Background
        from banners.palette import BLUE

        configure(
            team="Analytics Team",
            date="April 2026",
            palette=BLUE,
            background=Background.gradient("#0f172a", "#1e3a5f"),
        )
        ```
    """
    if team is not _UNSET:
        _state["team"] = team
    if date is not _UNSET:
        _state["date"] = date
    if palette is not _UNSET:
        _state["palette"] = palette
    if theme is not _UNSET:
        _state["theme"] = theme
    if background is not _UNSET:
        _state["background"] = background
    if template is not _UNSET:
        _state["template"] = template
    _state["_section_counter"] = 0


def get(key: str, default=None):
    return _state.get(key, default)


def _next_section_number() -> str:
    _state["_section_counter"] += 1
    return f"{_state['_section_counter']:02d}"
