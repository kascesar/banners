"""Shared fixtures for the unit test suite.

Prerequisite: install the `dev` extra (`uv sync --extra dev`).
This module defines fixtures that pytest applies to every test in `tests/`.
The global state of `banners.config` is restored after each test, so a test
that calls `configure()` does not affect the ones that follow.
Usage: `make test`.
"""

import copy

import pytest

from banners import config


@pytest.fixture(autouse=True)
def restore_config_state():
    """Save `banners.config._state` before each test and restore it afterwards.

    `_state` is a module-level dictionary that `configure()` and `Section`
    modify. Without this restore, the result of a test would depend on the
    order in which the previous tests ran.

    Returns:
        A generator that hands control to the test and then restores the state.
    """
    snapshot = copy.deepcopy(config._state)
    yield
    config._state.clear()
    config._state.update(snapshot)
