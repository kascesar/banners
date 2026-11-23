"""Fixtures comunes de la suite de pruebas unitarias.

Requisito previo: instalar el extra `dev` (`uv sync --extra dev`).
Este módulo define fixtures que pytest aplica a todas las pruebas de `tests/`.
El estado global de `banners.config` se restaura después de cada prueba, de modo
que una prueba que llama a `configure()` no altera a las siguientes.
Uso: `uv run pytest`.
"""

import copy

import pytest

from banners import config


@pytest.fixture(autouse=True)
def restore_config_state():
    """Guarda `banners.config._state` antes de cada prueba y lo restaura al final.

    `_state` es un diccionario global del módulo, y `configure()` y `Section`
    lo modifican. Sin esta restauración el resultado de una prueba dependería del
    orden en que se ejecutan las anteriores.

    Returns:
        Generador que entrega el control a la prueba y luego restaura el estado.
    """
    snapshot = copy.deepcopy(config._state)
    yield
    config._state.clear()
    config._state.update(snapshot)
