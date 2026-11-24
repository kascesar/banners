"""Tests for the parser, layout and SVG of `AnimatedGraph` (pure functions, no widget)."""

import re

import pytest

from banners.content.animated_graph import _build_svg, _layout, _parse


def test_parse_graph_lr():
    """A simple `graph LR` yields nodes, edges and direction."""
    nodes, edges, direction = _parse("graph LR\n  A --> B\n  B --> C")
    assert direction == "LR"
    assert nodes == {"A": "A", "B": "B", "C": "C"}
    assert edges == [("A", "B", ""), ("B", "C", "")]


def test_parse_graph_td():
    """The direction is read from the first line and upper-cased."""
    _, _, direction = _parse("graph td\n  A --> B")
    assert direction == "TD"


def test_parse_source_and_solo_labels():
    """Bracketed labels of a source node and of a standalone node replace the id."""
    nodes, _, _ = _parse("graph LR\n  B[Validate]\n  A[Raw data] --> B\n  B --> C")
    assert nodes == {"B": "Validate", "A": "Raw data", "C": "C"}


@pytest.mark.xfail(
    reason="_edge_re is not anchored to the end of the line and the lazy label group "
    "accepts an empty match, so the destination node label is lost. See Backlog.",
    strict=True,
)
def test_parse_destination_label():
    """The label of an edge destination node should be read as well."""
    nodes, _, _ = _parse("graph LR\n  A --> B[Validate]")
    assert nodes["B"] == "Validate"


def test_parse_first_label_wins():
    """When a node appears again with another label, the first label is kept."""
    nodes, _, _ = _parse("graph LR\n  A[One] --> B\n  A[Other] --> C")
    assert nodes["A"] == "One"


def test_parse_edge_labels():
    """Text between bars `|...|` becomes the edge label."""
    _, edges, _ = _parse("graph LR\n  A -->| yes | B\n  A -.-> C")
    assert edges == [("A", "B", "yes"), ("A", "C", "")]


def test_parse_ignores_comments_and_solo_nodes():
    """`%%` comments are ignored and a standalone node is added without edges."""
    nodes, edges, _ = _parse("graph LR\n  %% comment\n  X[Alone]")
    assert nodes == {"X": "Alone"}
    assert edges == []


def test_layout_chain_lr():
    """In an LR chain each node moves one level along the x axis."""
    nodes, edges, d = _parse("graph LR\n A --> B\n B --> C")
    pos, w, h = _layout(nodes, edges, d)
    assert (w, h) == (130, 40)
    xs = [pos[n][0] for n in "ABC"]
    assert xs == sorted(xs) and len(set(xs)) == 3
    assert {pos[n][1] for n in "ABC"} == {0}


def test_layout_chain_td_uses_y_axis():
    """In TD the levels advance along the y axis."""
    nodes, edges, d = _parse("graph TD\n A --> B")
    pos, _, _ = _layout(nodes, edges, d)
    assert pos["A"][0] == pos["B"][0]
    assert pos["B"][1] > pos["A"][1]


def test_layout_fork_shares_level():
    """The children of a fork share a level and sit on different rows."""
    nodes, edges, d = _parse("graph LR\n A --> B\n A --> C")
    pos, _, _ = _layout(nodes, edges, d)
    assert pos["B"][0] == pos["C"][0] > pos["A"][0]
    assert pos["B"][1] != pos["C"][1]


def test_layout_cycle_terminates():
    """A cycle does not trap the BFS in an infinite loop and every node gets a position."""
    nodes, edges, d = _parse("graph LR\n A --> B\n B --> C\n C --> A")
    pos, _, _ = _layout(nodes, edges, d)
    assert set(pos) == {"A", "B", "C"}


def test_layout_empty():
    """With no nodes, the layout is empty."""
    assert _layout({}, [], "LR") == ({}, 130, 40)


def test_build_svg_one_ag_node_per_node():
    """The SVG has one `.ag-node` group per node and one line per edge."""
    nodes, edges, d = _parse("graph LR\n A[One] --> B\n B -->|x| C\n A --> C")
    pos, w, h = _layout(nodes, edges, d)
    svg = _build_svg(nodes, edges, pos, w, h, "u1")
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert len(re.findall(r'class="ag-node"', svg)) == len(nodes)
    assert "One" in svg and ">x<" in svg
    assert 'id="arr-u1"' in svg
