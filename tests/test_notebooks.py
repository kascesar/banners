"""Prueba de humo de los notebooks de marimo en `test/` y `example/`.

Requisito previo: instalar el extra `dev` (`uv sync --extra dev`).
Este módulo ejecuta cada notebook como script (`python <archivo>`, que llama a
`app.run()`) en un subproceso con límite de tiempo y exige código de salida 0.
No modifica los notebooks; los archivos que un notebook escriba quedan donde el
notebook los deje.
Los notebooks que usan manim llevan la marca `manim` y se omiten por defecto,
porque necesitan las librerías del sistema (cairo, pango, ffmpeg y LaTeX). Los
notebooks con un error conocido se marcan `xfail(strict=True)`: si alguien corrige
el error, la prueba pasa a fallar como XPASS y avisa que hay que quitar la marca.
Uso: `uv run pytest tests/test_notebooks.py` (sin manim) o `uv run pytest -m manim`.

Detección de errores: en marimo 0.23 `app.run()` relanza la excepción de la primera
celda que falla, así que el proceso termina con código distinto de 0. Se verificó
con copias de un notebook con una celda que lanza `RuntimeError` y con una celda
dependiente de otra que divide por cero; ambas terminan con código 1. Por eso basta
revisar el código de salida, sin buscar "Traceback" en stderr.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

# Límite de tiempo por notebook, en segundos. `example/showcase.py` renderiza
# varias escenas de manim y tarda cerca de dos minutos.
TIMEOUT = 600

# Notebooks que necesitan manim, con ruta relativa a la raíz del repositorio.
MANIM_NOTEBOOKS = {
    "test/08_manim.py",
    "test/09_flow_animation.py",
    "example/showcase.py",
    "example/ondas_electromagneticas.py",
}

# Notebooks con un error conocido, anotado en el Backlog de MILESTONES.md.
KNOWN_FAILURES = {
    "test/04_graph.py": "SyntaxError: triple comilla anidada dentro de mo.md(r\"\"\"...\"\"\")",
    "test/05_animated_graph.py": "SyntaxError: triple comilla anidada dentro de mo.md(r\"\"\"...\"\"\")",
    "test/07_plot.py": "MultipleDefinitionError: varias celdas definen `plt`",
    "example/showcase.py": "NameError: la celda de BasicScene usa MathTex, FadeOut y MW sin definirlos",
}


def notebook_params() -> list:
    """Construye los parámetros de la prueba, uno por notebook.

    Returns:
        Lista de `pytest.param` con la ruta relativa a la raíz como valor e id,
        y las marcas `manim` y `xfail` según corresponda.
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
    """Ejecuta un notebook como script y exige que termine sin error.

    El directorio de trabajo es la raíz del repositorio, porque los notebooks leen
    archivos con rutas relativas a ella (por ejemplo `img/test.jpeg` en
    `test/10_background.py`). Los `layout_file` no dependen del directorio de
    trabajo: `app.run()` ejecutado como script no lee el archivo de layout.

    Args:
        notebook: Ruta del notebook relativa a la raíz del repositorio.
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
        f"{notebook} terminó con código {result.returncode}\n--- stderr ---\n{result.stderr}"
    )
