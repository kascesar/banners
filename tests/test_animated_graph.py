"""Pruebas del parser, el layout y el SVG de `AnimatedGraph` (funciones puras, sin widget)."""

import re

import pytest

from banners.content.animated_graph import _build_svg, _layout, _parse


def test_parse_graph_lr():
    """Un `graph LR` simple produce nodos, aristas y dirección."""
    nodes, edges, direction = _parse("graph LR\n  A --> B\n  B --> C")
    assert direction == "LR"
    assert nodes == {"A": "A", "B": "B", "C": "C"}
    assert edges == [("A", "B", ""), ("B", "C", "")]


def test_parse_graph_td():
    """La dirección se lee de la primera línea y se normaliza a mayúsculas."""
    _, _, direction = _parse("graph td\n  A --> B")
    assert direction == "TD"


def test_parse_source_and_solo_labels():
    """Las etiquetas entre corchetes del origen y de un nodo suelto reemplazan al id."""
    nodes, _, _ = _parse("graph LR\n  B[Validar]\n  A[Datos crudos] --> B\n  B --> C")
    assert nodes == {"B": "Validar", "A": "Datos crudos", "C": "C"}


@pytest.mark.xfail(
    reason="_edge_re no está anclado al final de la línea y el grupo perezoso de la "
    "etiqueta acepta vacío, así que la etiqueta del nodo destino se pierde. Ver Backlog.",
    strict=True,
)
def test_parse_destination_label():
    """La etiqueta del nodo destino de una arista también debería leerse."""
    nodes, _, _ = _parse("graph LR\n  A --> B[Validar]")
    assert nodes["B"] == "Validar"


def test_parse_first_label_wins():
    """Si un nodo aparece de nuevo con otra etiqueta, se conserva la primera."""
    nodes, _, _ = _parse("graph LR\n  A[Uno] --> B\n  A[Otro] --> C")
    assert nodes["A"] == "Uno"


def test_parse_edge_labels():
    """El texto entre barras `|...|` queda como etiqueta de la arista."""
    _, edges, _ = _parse("graph LR\n  A -->| sí | B\n  A -.-> C")
    assert edges == [("A", "B", "sí"), ("A", "C", "")]


def test_parse_ignores_comments_and_solo_nodes():
    """Los comentarios `%%` se ignoran y un nodo suelto se agrega sin aristas."""
    nodes, edges, _ = _parse("graph LR\n  %% comentario\n  X[Solo]")
    assert nodes == {"X": "Solo"}
    assert edges == []


def test_layout_chain_lr():
    """En una cadena LR cada nodo avanza un nivel en el eje x."""
    nodes, edges, d = _parse("graph LR\n A --> B\n B --> C")
    pos, w, h = _layout(nodes, edges, d)
    assert (w, h) == (130, 40)
    xs = [pos[n][0] for n in "ABC"]
    assert xs == sorted(xs) and len(set(xs)) == 3
    assert {pos[n][1] for n in "ABC"} == {0}


def test_layout_chain_td_uses_y_axis():
    """En TD los niveles avanzan en el eje y."""
    nodes, edges, d = _parse("graph TD\n A --> B")
    pos, _, _ = _layout(nodes, edges, d)
    assert pos["A"][0] == pos["B"][0]
    assert pos["B"][1] > pos["A"][1]


def test_layout_fork_shares_level():
    """Los hijos de una bifurcación quedan en el mismo nivel y en filas distintas."""
    nodes, edges, d = _parse("graph LR\n A --> B\n A --> C")
    pos, _, _ = _layout(nodes, edges, d)
    assert pos["B"][0] == pos["C"][0] > pos["A"][0]
    assert pos["B"][1] != pos["C"][1]


def test_layout_cycle_terminates():
    """Un ciclo no deja el BFS en un bucle infinito y todos los nodos reciben posición."""
    nodes, edges, d = _parse("graph LR\n A --> B\n B --> C\n C --> A")
    pos, _, _ = _layout(nodes, edges, d)
    assert set(pos) == {"A", "B", "C"}


def test_layout_empty():
    """Sin nodos, el layout es vacío."""
    assert _layout({}, [], "LR") == ({}, 130, 40)


def test_build_svg_one_ag_node_per_node():
    """El SVG tiene un grupo `.ag-node` por nodo y una línea por arista."""
    nodes, edges, d = _parse("graph LR\n A[Uno] --> B\n B -->|x| C\n A --> C")
    pos, w, h = _layout(nodes, edges, d)
    svg = _build_svg(nodes, edges, pos, w, h, "u1")
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert len(re.findall(r'class="ag-node"', svg)) == len(nodes)
    assert "Uno" in svg and ">x<" in svg
    assert 'id="arr-u1"' in svg
