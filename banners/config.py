"""Global presentation configuration."""

_state: dict = {
    "team": "",
    "date": "",
    "icon": None,
    "palette": None,
    "background": None,
    "_section_counter": 0,
}

_UNSET = object()


def configure(
    team: str = _UNSET,
    date: str = _UNSET,
    icon=_UNSET,
    palette=_UNSET,
    background=_UNSET,
) -> None:
    """Set global defaults shared by all slides and reset the section counter.

    Call this once at the top of the notebook. Any slide parameter left at its
    default will inherit the value set here. Calling `configure()` without
    arguments only resets the section counter.

    Args:
        team: Team line shown in `Cover`, `Intro`, and `Closing` banners.
        date: Date string shown in `Cover` (e.g. `"April 2026"`).
        icon: Icon applied to all slides. Pass a dict with keys `"src"`
            (path, URL, or bytes) and optionally `"size"` (CSS height).
        palette: Color palette applied to `Cover`, `Intro`, and `Closing`.
            Pass any `Palette` instance or predefined constant
            (`BLUE`, `GREEN`, `PURPLE`, `GRAY`).
        background: Background applied to all slides. Pass a `Background`
            instance (`Background.color()`, `Background.gradient()`, or
            `Background.image()`). Individual slides can override this with
            their own `background` argument.

    Example:
        ```python
        from banners import configure, Background
        from banners.palette import BLUE

        configure(
            team="Analytics Team",
            date="April 2026",
            palette=BLUE,
            icon={"src": "img/logo.png"},
            background=Background.gradient("#0f172a", "#1e3a5f"),
        )
        ```
    """
    if team is not _UNSET:
        _state["team"] = team
    if date is not _UNSET:
        _state["date"] = date
    if icon is not _UNSET:
        _state["icon"] = icon
    if palette is not _UNSET:
        _state["palette"] = palette
    if background is not _UNSET:
        _state["background"] = background
    _state["_section_counter"] = 0


def get(key: str, default=None):
    return _state.get(key, default)


def _next_section_number() -> str:
    _state["_section_counter"] += 1
    return f"{_state['_section_counter']:02d}"
