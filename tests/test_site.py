"""Tests for the documentation site in `site/`: both languages, code, images, links."""

import re
from pathlib import Path

import pytest

SITE = Path(__file__).resolve().parents[1] / "site"
PAGES = {
    "index.qmd",
    "get-started.qmd",
    *(f"look/{p}.qmd" for p in ("templates", "palettes", "themes", "layouts", "backgrounds")),
    *(f"slides/{p}.qmd" for p in ("cover", "intro", "section", "closing")),
    *(f"content/{p}.qmd" for p in (
        "text", "image", "table", "plot", "graph", "animated-graph", "flow-animation", "manim",
    )),
    *(f"howto/{p}.qmd" for p in ("present", "organization-template", "manim-scene", "cache")),
    "examples.qmd",
    "whats-new.qmd",
}
CODE = re.compile(r"```python\n(.*?)```", re.DOTALL)
LINK = re.compile(r"\]\(([^)\s]+)")


def pages() -> list[Path]:
    """All page sources of both languages.

    Returns:
        The `.qmd` files under `site/en` and `site/es`.
    """
    return sorted((SITE / "en").rglob("*.qmd")) + sorted((SITE / "es").rglob("*.qmd"))


def blocks(manim: bool) -> list[tuple[str, str]]:
    """Python code blocks of the site that are meant to run.

    Args:
        manim: `True` for the blocks that import manim, `False` for the others.

    Returns:
        `(page, code)` pairs; blocks starting with `# fragment` are left out.
    """
    found = []
    for page in pages():
        for code in CODE.findall(page.read_text()):
            if code.startswith("# fragment"):
                continue
            if ("manim" in code) == manim:
                found.append((str(page.relative_to(SITE)), code))
    return found


def test_languages_have_the_same_pages():
    for lang in ("en", "es"):
        found = {str(p.relative_to(SITE / lang)) for p in (SITE / lang).rglob("*.qmd")}
        assert found == PAGES, lang


@pytest.mark.parametrize(("page", "code"), blocks(manim=False))
def test_site_code_runs(page, code):
    exec(code, {})  # noqa: S102 - the site examples are ours


@pytest.mark.manim
@pytest.mark.parametrize(("page", "code"), blocks(manim=True))
def test_site_manim_code_runs(page, code):
    exec(code, {})  # noqa: S102 - the site examples are ours


def test_site_images_exist():
    for page in pages():
        for target in LINK.findall(page.read_text()):
            if "images/" in target:
                assert (page.parent / target).resolve().exists(), f"{page}: {target}"


def test_site_links_are_relative():
    for page in pages():
        for target in LINK.findall(page.read_text()):
            assert not target.startswith("/"), f"{page}: {target}"
