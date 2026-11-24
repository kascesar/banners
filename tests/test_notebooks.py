"""Smoke test for the marimo notebooks in `test/` and `example/`.

Prerequisite: install the `dev` extra (`uv sync --extra dev`).
This module runs each notebook as a script (`python <file>`, which calls
`app.run()`) in a subprocess with a time limit and requires exit code 0.
It does not modify the notebooks; files a notebook writes stay where the
notebook leaves them.
Notebooks that use manim carry the `manim` marker and are skipped by default,
because they need the system libraries (cairo, pango, ffmpeg and LaTeX).
Notebooks with a known error are marked `xfail(strict=True)`: if someone fixes
the error, the test fails as XPASS and signals that the marker must be removed.
Usage: `uv run pytest tests/test_notebooks.py` (no manim) or `uv run pytest -m manim`.

Error detection: in marimo 0.23 `app.run()` re-raises the exception of the first
failing cell, so the process exits with a non-zero code. This was checked with
copies of a notebook with a cell that raises `RuntimeError` and with a cell that
depends on another one dividing by zero; both exit with code 1. Checking the exit
code is therefore enough, without searching stderr for "Traceback".
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# Time limit per notebook, in seconds. `example/showcase.py` renders several
# manim scenes and takes about two minutes.
TIMEOUT = 600

# Notebooks that need manim, with paths relative to the repository root.
MANIM_NOTEBOOKS = {
    "test/08_manim.py",
    "test/09_flow_animation.py",
    "example/showcase.py",
    "example/ondas_electromagneticas.py",
}

# Notebooks with a known error, recorded in the Backlog of MILESTONES.md.
KNOWN_FAILURES = {
    "example/showcase.py": "NameError: the BasicScene cell uses MathTex, FadeOut and MW without defining them",
}


def notebook_params() -> list:
    """Build the test parameters, one per notebook.

    Returns:
        A list of `pytest.param` with the root-relative path as value and id,
        and the `manim` and `xfail` markers where they apply.
    """
    paths = sorted(ROOT.glob("test/*.py")) + sorted(ROOT.glob("example/*.py"))
    params = []
    for path in paths:
        rel = path.relative_to(ROOT).as_posix()
        marks = []
        if rel in MANIM_NOTEBOOKS:
            marks.append(pytest.mark.manim)
        if rel in KNOWN_FAILURES:
            marks.append(pytest.mark.xfail(strict=True, reason=KNOWN_FAILURES[rel]))
        params.append(pytest.param(rel, id=rel, marks=marks))
    return params


@pytest.mark.parametrize("notebook", notebook_params())
def test_notebook_runs(notebook: str) -> None:
    """Run a notebook as a script and require it to finish without errors.

    The working directory is the repository root, because the notebooks read
    files with paths relative to it (for example `img/test.jpeg` in
    `test/10_background.py`). `layout_file` does not depend on the working
    directory: `app.run()` run as a script does not read the layout file.

    Args:
        notebook: Path of the notebook relative to the repository root.
    """
    result = subprocess.run(
        [sys.executable, notebook],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=TIMEOUT,
        check=False,
    )
    assert result.returncode == 0, (
        f"{notebook} exited with code {result.returncode}\n--- stderr ---\n{result.stderr}"
    )
