# M7 — Security and broken notebooks: Implementation Plan

> **For agentic workers:** execute with superpowers:executing-plans (inline, as
> `CLAUDE.md` requires). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Verify TLS when banners downloads images by URL, and make the four
broken visual notebooks run.

**Architecture:** One deletion in `Slide._icon_src` (the default SSL context
already verifies), pinned by a unit test that captures the context passed to
`urllib.request.urlopen`. The notebooks are fixed in place; their smoke tests
become the regression tests once their `KNOWN_FAILURES` entries are removed.

**Tech Stack:** Python ≥ 3.10, pytest, marimo, manim (Task 3 only).

**Spec:** `MILESTONES.md` → "M7 — Security and broken notebooks".

## Global Constraints

- No change to library behavior other than TLS verification.
- Everything in English; Google-style docstrings with Args/Returns on new test helpers.
- Commits per task on `milestone/m7-security-notebooks`, Conventional Commits, no `Co-Authored-By`.
- Verification command for every task: `make check`; Task 3 also `uv run pytest -m manim`.

## Review Focus

1. A logo URL with a bad certificate on a template slide: the slide still renders, without that image. Test in Task 1.
2. A notebook fixed by renaming a variable that another cell still reads under the old name: caught by the smoke test of that notebook (Task 2).

---

### Task 1: TLS verification in `Slide._icon_src`

**Files:**
- Modify: `banners/slide.py` (`_icon_src`: delete `ctx.check_hostname = False` and `ctx.verify_mode = ssl.CERT_NONE`)
- Test: `tests/test_slide.py`

**Interfaces:**
- Produces: `Slide._icon_src(url)` calls `urllib.request.urlopen(req, timeout=10, context=ctx)` with `ctx` from `ssl.create_default_context()` unchanged.

- [ ] **Step 1: Write the failing tests** in `tests/test_slide.py`:
  - `test_icon_src_verifies_tls`: monkeypatch `urllib.request.urlopen` in `banners.slide` with a fake that records the `context` keyword and returns an object usable as a context manager with `.read()` → `b"<svg/>"` and `.headers.get("Content-Type", "")` → `"image/svg+xml"`; call `Slide._icon_src("https://example.org/logo.svg")`; assert `ctx.verify_mode == ssl.CERT_REQUIRED` and `ctx.check_hostname is True`.
  - `test_bad_certificate_image_is_omitted` (Review Focus 1): fake `urlopen` raises `ssl.SSLCertVerificationError`; `configure(template=Template(mark="https://bad.example/logo.png"))`; `Section(title="A", content=Text("x")).render()` succeeds and its HTML does not contain `bad.example`.
- [ ] **Step 2: Run** `uv run pytest tests/test_slide.py -v` → `test_icon_src_verifies_tls` FAILS (`verify_mode` is `CERT_NONE`).
- [ ] **Step 3: Implement:** delete the two lines.
- [ ] **Step 4: Run** `make check` → green.
- [ ] **Step 5: Commit** `fix(security): verify TLS certificates when downloading images`.

### Task 2: Notebooks `test/04_graph.py`, `test/05_animated_graph.py`, `test/07_plot.py`

**Files:**
- Modify: `test/04_graph.py`, `test/05_animated_graph.py` (outer `mo.md(r"""…""")` of the documentation cell → `mo.md(r'''…''')`)
- Modify: `test/07_plot.py` (one cell imports `matplotlib.pyplot as plt` and returns it; the cells at lines 61 and 97 take `plt` as a parameter instead of importing it)
- Test: `tests/test_notebooks.py` (remove the three `KNOWN_FAILURES` entries)

- [ ] **Step 1: Remove** the entries for `test/04_graph.py`, `test/05_animated_graph.py` and `test/07_plot.py` from `KNOWN_FAILURES`.
- [ ] **Step 2: Run** `uv run pytest tests/test_notebooks.py -v` → those three FAIL (`SyntaxError`, `SyntaxError`, `MultipleDefinitionError`).
- [ ] **Step 3: Fix** the three notebooks as listed under Files.
- [ ] **Step 4: Run** `make check` → green; the three notebooks PASS.
- [ ] **Step 5: Commit** `fix(notebooks): 04 and 05 compile, 07 defines plt once`.

### Task 3: `example/showcase.py`

**Files:**
- Modify: `example/showcase.py` (imports cell: add `MathTex`, `FadeOut`, `WHITE as MW` to the `from manim import (...)` and to the cell's return tuple)
- Test: `tests/test_notebooks.py` (remove the last `KNOWN_FAILURES` entry; the dict stays, empty, with its comment)

- [ ] **Step 1: Remove** the `example/showcase.py` entry from `KNOWN_FAILURES`.
- [ ] **Step 2: Run** `uv run pytest -m manim -k showcase -v` → FAIL with `NameError: name 'MathTex' is not defined`.
- [ ] **Step 3: Fix** the imports cell.
- [ ] **Step 4: Run** `uv run pytest -m manim` → 4 passed, 0 xfailed; `make check` → green.
- [ ] **Step 5: Commit** `fix(example): showcase imports MathTex, FadeOut and WHITE`.

### Task 4: Close the milestone

- [ ] **Step 1:** Remove the four items (TLS, 04/05, 07, showcase) from the Backlog of `MILESTONES.md`.
- [ ] **Step 2:** Run `make check`, `uv run pytest tests/test_notebooks.py` and `uv run pytest -m manim`; mark M7 `[x]`, add the Log line, and commit with their output in the body.
