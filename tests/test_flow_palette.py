"""Tests for `FlowAnimation` colors and step length."""

import json
import subprocess

import pytest

from banners import BLUE, Palette
from banners.content import FlowAnimation, Manim
from banners.content.flow_animation import node_colors


def test_node_colors_cycle_primary_secondary():
    """Without section colors, nodes alternate primary and secondary."""
    assert node_colors(Palette(primary="#1", secondary="#2"), 3) == ["#1", "#2", "#1"]


def test_node_colors_use_section_colors():
    """Section colors drive the cycle, even with a single color."""
    assert node_colors(Palette(section_colors=("#9",)), 2) == ["#9", "#9"]
    assert node_colors(Palette(primary="#1", secondary="#2", section_colors=None), 2) == ["#1", "#2"]


def test_flow_with_palette_passes_palette_to_manim(monkeypatch):
    """A flow on a slide renders through a `Manim` that carries the slide palette."""
    seen = []
    monkeypatch.setattr(Manim, "render", lambda self: seen.append(self.palette) or "html")
    flow = FlowAnimation(["A", "B"])
    styled = flow._with_palette(BLUE)
    styled.render()
    assert seen == [BLUE]
    assert flow.palette is None


def section_durations(m: Manim) -> list[float]:
    """Read the duration of every cached section video of an interactive render.

    Args:
        m: The `Manim` element that was rendered.

    Returns:
        The duration in seconds of each section, in order.
    """
    files = sorted((Manim._cache_root() / m._cache_key()).glob("*.mp4"))
    out = []
    for f in files:
        probe = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(f)],
            capture_output=True, text=True, check=True,
        )
        out.append(float(json.loads(probe.stdout)["format"]["duration"]))
    return out


@pytest.mark.manim
def test_flow_steps_are_short(monkeypatch):
    """Every click of a flow lasts at most 0.3 s."""
    built = []
    original = Manim.render

    def capture(self):
        built.append(self)
        return original(self)

    monkeypatch.setattr(Manim, "render", capture)
    FlowAnimation(["A", "B", "C", "D"], quality="low").render()
    durations = section_durations(built[0])
    assert len(durations) == 4
    assert all(d <= 0.3 for d in durations), durations


def test_direction_changes_the_cache_key():
    """The same nodes drawn LR and TD must not share a cached render."""
    nodes = ["S3", "Glue", "Athena"]
    lr = FlowAnimation(nodes, direction="LR")._data_key()
    td = FlowAnimation(nodes, direction="TD")._data_key()
    assert lr != td
