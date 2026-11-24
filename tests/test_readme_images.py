"""Tests for the README image generator in `scripts/readme_images.py`."""

import importlib.util
from pathlib import Path

import pytest

PIL_Image = pytest.importorskip("PIL.Image")

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "readme_images.py"


def load_script():
    """Import `scripts/readme_images.py` by path.

    Returns:
        The loaded module.
    """
    spec = importlib.util.spec_from_file_location("readme_images", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_group_by_part():
    kinds = ["title", "title", "slide", "slide", "title", "slide", "title", "slide"]
    assert load_script().group_by_part(kinds) == [[2, 3], [5], [7]]


def test_group_by_part_missing_video():
    """A part whose title animation is missing still starts a new group at the next title."""
    assert load_script().group_by_part(["slide", "title", "slide"]) == [[0], [2]]


def test_make_gif_one_frame_per_slide(tmp_path):
    """One GIF frame per slide: no blended frames between slides."""
    frames = []
    # Slides shown side by side in the showcase are captured smaller.
    for i, (color, size) in enumerate([("red", (1600, 900)), ("green", (640, 360)), ("blue", (1580, 890))]):
        path = tmp_path / f"{i}.png"
        PIL_Image.new("RGB", size, color).save(path)
        frames.append(path)
    out = tmp_path / "out.gif"
    load_script().make_gif(frames, out)
    with PIL_Image.open(out) as gif:
        assert gif.n_frames == 3
        assert gif.size == (800, 450)
        gif.seek(1)
        assert gif.convert("RGB").getpixel((799, 449)) == (0, 128, 0)
        assert gif.info["duration"] == 1500
        assert gif.info["loop"] == 0
