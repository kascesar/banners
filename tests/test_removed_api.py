"""Tests that the parameters removed in 0.5 fail instead of being ignored."""

import pytest

from banners import configure
from banners.slides import Closing, Cover, Intro, Section


@pytest.mark.parametrize(
    "call",
    [
        lambda: Cover(title="A", content_kind="info"),
        lambda: Intro(title="A", content_kind="info"),
        lambda: Section(title="A", content_kind="info"),
        lambda: Closing(title="A", content_kind="info"),
        lambda: Cover(title="A", icon={"src": "x"}),
        lambda: Intro(title="A", icon={"src": "x"}),
        lambda: Section(title="A", icon={"src": "x"}),
        lambda: Closing(title="A", icon={"src": "x"}),
        lambda: configure(icon={"src": "x"}),
    ],
    ids=[
        "cover-content_kind", "intro-content_kind", "section-content_kind", "closing-content_kind",
        "cover-icon", "intro-icon", "section-icon", "closing-icon", "configure-icon",
    ],
)
def test_removed_parameters_raise(call):
    """`content_kind` and `icon` are no longer accepted."""
    with pytest.raises(TypeError):
        call()


def test_section_palette_is_gone():
    """`SectionPalette` no longer exists."""
    with pytest.raises(ImportError):
        from banners.palette import SectionPalette  # noqa: F401
