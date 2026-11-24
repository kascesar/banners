"""Tests for the documentation image generator in `scripts/docs_images.py`."""

import ast
import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "docs_images.py"


def load_script():
    """Import `scripts/docs_images.py` by path.

    Returns:
        The loaded module.
    """
    spec = importlib.util.spec_from_file_location("docs_images", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_notebook_source_has_one_cell_per_shot():
    shots = {"a": "from banners import Section\nSection(title='A')", "b": "Section(title='B')"}
    source = load_script().notebook_source(shots)
    tree = ast.parse(source)
    cells = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
    # One setup cell plus one cell per shot, in order.
    assert len(cells) == 3
    assert source.index("title='A'") < source.index("title='B'")


def test_every_shot_is_valid_python():
    for name, snippet in load_script().SHOTS.items():
        ast.parse(snippet, filename=name)
