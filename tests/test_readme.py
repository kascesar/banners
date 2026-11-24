"""Tests for README.md: short, and every Python example runs."""

import re
from pathlib import Path

README = (Path(__file__).resolve().parents[1] / "README.md").read_text()
BLOCKS = re.findall(r"```python\n(.*?)```", README, re.DOTALL)


def test_readme_is_short():
    assert len(README.splitlines()) <= 120


def test_readme_code_runs():
    assert BLOCKS
    for block in BLOCKS:
        exec(block, {})  # noqa: S102 - the README examples are ours
