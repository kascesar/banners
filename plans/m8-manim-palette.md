# M8 — Professional manim animations, player, and palette-aware plots: Implementation Plan

> **For agentic workers:** execute with superpowers:executing-plans (inline, as
> `CLAUDE.md` requires). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Animations and plots take the colors of the slide's palette, manim
steps become short and direct, renders get faster, and the minimum Python
becomes 3.11 so banners can use manim ≥ 0.21.

**Architecture:** Content elements that can follow the palette implement
`_with_palette(palette) -> same type`, returning a styled copy; the template
calls it before rendering an item, so content never reads `banners.config`.
`Manim` paints `palette.panel` as the scene background at 30 fps and passes
palette colors to the player; `FlowAnimation` and `PipelineScene` build their
scenes from the palette with one 0.25 s ease-out step per click.

**Tech Stack:** Python ≥ 3.11, manim ≥ 0.21, matplotlib, marimo, pytest, ffprobe (manim tests).

**Spec:** `MILESTONES.md` → "M8 — Professional manim animations, player, and palette-aware plots".

## Global Constraints

- `requires-python = ">=3.11"`; `manim` extra `manim>=0.21`; CI on 3.11 and 3.12; version `0.6.0`.
- Content modules in `banners/content/` must not contain `"from .."` or `"banners.config"` (existing test).
- Background of every banners manim render: `palette.panel`, opaque MP4/GIF; no transparent video.
- One `self.play` of `run_time=0.25` with `rate_func=ease_out_cubic` per step; no `Write`, no scale-in, no `self.wait()` at the end of a step.
- Frame rate 30 for every quality; resolutions stay manim's 480p/720p/1080p presets.
- A standalone animation uses `Palette()`; a standalone `Plot` renders exactly as today.
- Everything in English; Google-style docstrings; commits per task, Conventional Commits, no `Co-Authored-By`.
- Verification for every task: `make check`; tasks touching manim also `uv run pytest -m manim`.

## Review Focus

1. A `FlowAnimation` first shown standalone and then on a slide must not reuse the standalone render: the palette is in the cache key. Test in Task 3.
2. The same matplotlib figure placed on two slides with different palettes: each slide gets its own colors and the user's figure object is not modified. Test in Task 2.
3. A palette whose `section_colors` has one color, or none: node colors still cycle without error. Test in Task 4.
4. A custom `Scene` that sets `self.camera.background_color` itself keeps its color. Test in Task 3.
5. A plotly `Plot` on a slide renders unchanged and without error. Test in Task 2.

---

### Task 1: Python 3.11 and manim ≥ 0.21

**Files:**
- Modify: `pyproject.toml` (`requires-python = ">=3.11"`; ruff `target-version = "py311"`; `manim = ["manim>=0.21"]`; `manim>=0.21` in `dev`), `uv.lock`
- Modify: `.github/workflows/ci.yml` (matrix `["3.11", "3.12"]`, comment says `>=3.11`)
- Modify: `CLAUDE.md` (Conventions: "Python ≥ 3.11"), `README.md` (Installation: Python 3.11 or newer; "Upgrading to 0.6" note that 3.10 users stay on 0.5.1)

Configuration only; no new unit test. The existing suites are the gate.

- [ ] **Step 1:** Recreate the local environment on Python 3.12: `uv venv --python 3.12 --clear` then `uv pip install -e ".[dev]"` after editing `pyproject.toml`; run `uv lock`.
- [ ] **Step 2: Verify** `uv run python -c "import manim, sys; print(sys.version_info[:2], manim.__version__)"` → `(3, 12)` and a manim version ≥ 0.21.
- [ ] **Step 3: Run** `uv run ruff check banners tests`; fix what the py311 target reports without behavior changes.
- [ ] **Step 4: Run** `make check` and `uv run pytest -m manim` → green (4 manim notebooks pass). If manim ≥ 0.21 changed `format`/`save_sections` behavior, fix `banners/content/manim.py` through systematic-debugging.
- [ ] **Step 5: Measure** the cold render of `FlowAnimation([f"Ingest {time.time()}", "Validate", "Transform", "Load"], quality="low")` (unique name to skip the disk cache) and record it in the commit body next to the 2.0 s baseline.
- [ ] **Step 6: Commit** `chore!: require Python 3.11 and manim >= 0.21`.

### Task 2: Palette hand-off in the template, and palette-aware plots

**Files:**
- Modify: `banners/template.py` (`_content`), `banners/content/plot.py`
- Test: `tests/test_plot_palette.py` (new)

**Interfaces:**
- Produces: protocol method `_with_palette(self, palette: Palette) -> <same type>` returning a styled copy, never mutating `self`. `Template._content` replaces `item` with `item._with_palette(self.palette)` when the item has that attribute, before rendering it.
- Produces: `Plot._with_palette(palette) -> Plot`. For a matplotlib figure: works on `copy.deepcopy(self.fig)`; axes titles, axis labels and legend texts take `palette.text`; spines and ticks take `palette.muted`; lines and patches whose color equals one of matplotlib's default cycle colors (`plt.rcParams["axes.prop_cycle"]`, index `i`) take `series[i % len(series)]`, where `series = palette.section_colors or (palette.primary, palette.secondary)`. Plotly figures: returns `self`.

- [ ] **Step 1: Write the failing tests** in `tests/test_plot_palette.py` (matplotlib with `Agg`):
  - `test_auto_colored_line_takes_palette_primary`: `ax.plot([0,1])`; `Plot(fig)._with_palette(Palette(primary="#123456"))` → the copied figure's first line color is `#123456`.
  - `test_hand_colored_line_is_kept`: `ax.plot([0,1], color="#abcdef")` → stays `#abcdef` after `_with_palette`.
  - `test_axes_text_follows_palette`: `ax.set_title("T")` → title color `palette.text`, tick label color `palette.muted`.
  - `test_original_figure_is_not_modified` (Review Focus 2): after `_with_palette(BLUE)` and `_with_palette(GREEN)` the user's line color is still matplotlib's `C0`, and the two copies show `BLUE.primary` and `GREEN.primary`.
  - `test_standalone_plot_renders_as_today`: `Plot(fig).render().text` equals `mo.as_html(fig).text`.
  - `test_template_restyles_plot_on_slide`: `configure(template=Template(palette=Palette(primary="#123456")))`; a `Section` with `Plot(fig)` renders, and a spy on `Plot._with_palette` records one call with that palette.
  - `test_plotly_plot_on_slide_unchanged` (Review Focus 5): skip with `pytest.importorskip("plotly")`; `Plot(px_fig)._with_palette(BLUE) is` the same object, and a slide with it renders.
- [ ] **Step 2: Run** `uv run pytest tests/test_plot_palette.py -v` → FAIL (`AttributeError: _with_palette`).
- [ ] **Step 3: Implement** `Plot._with_palette` and the hand-off in `Template._content`.
- [ ] **Step 4: Run** `make check` → green.
- [ ] **Step 5: Commit** `feat(plot): plots on a slide follow the palette`.

### Task 3: `Manim` follows the palette, renders at 30 fps, accepts scene factories

**Files:**
- Modify: `banners/content/manim.py`, `banners/content/_manim_widget.js`
- Test: `tests/test_manim_palette.py` (new; unit tests without manim, plus `@pytest.mark.manim` ones)

**Interfaces:**
- Produces: `Manim.__init__(..., palette: Palette | None = None)`; `Manim._with_palette(palette) -> Manim` (copy with `palette` set, `_cached` reset); `Manim._palette` property → `self.palette or Palette()`.
- Produces: `Manim._scene_class() -> type`: `self.scene` if it is a class; otherwise calls it, passing `palette=self._palette` when its signature has a `palette` parameter.
- Produces: render config adds `"background_color": self._palette.panel` and `"frame_rate": 30`; the cache key adds the palette's `repr` and `fps=30`.
- Produces: the player HTML gets `colors = {"panel": ..., "muted": ..., "primary": ...}` (from `self._palette`); the page and stage background use `panel` (no `#000`); buttons are text-only in `muted`, the active autoplay toggle in `primary`, font size in `em`.

- [ ] **Step 1: Write the failing tests:**
  - `test_with_palette_returns_copy`: `m = Manim(Scene)` (a dummy class); `m2 = m._with_palette(BLUE)` → `m2.palette is BLUE`, `m.palette is None`.
  - `test_palette_changes_cache_key` (Review Focus 1): `Manim(S)._cache_key() != Manim(S)._with_palette(BLUE)._cache_key()`.
  - `test_factory_receives_palette`: a function `def factory(palette=None): seen.append(palette); return DummyScene` → `Manim(factory)._with_palette(BLUE)._scene_class() is DummyScene` and `seen == [BLUE]`; a factory without `palette` is called with no arguments.
  - `test_player_uses_palette_colors`: `Manim._build_iframe_player(["x"], "100%", False, {"panel": "#101010", "muted": "#202020", "primary": "#303030"})` → decoded HTML contains `#101010` and not `background:#000`.
  - `@pytest.mark.manim test_background_is_panel`: a one-shape scene rendered `format="png"` with `_with_palette(Palette(panel="#123456"))` → pixel (0, 0) is `(0x12, 0x34, 0x56)`.
  - `@pytest.mark.manim test_scene_background_override_is_kept` (Review Focus 4): a scene setting `self.camera.background_color = "#654321"` → pixel (0, 0) is `(0x65, 0x43, 0x21)`.
  - `@pytest.mark.manim test_pipeline_scene_renders_sections`: `Manim(PipelineScene, interactive=True).render()` succeeds and the cache directory holds 6 mp4 files.
- [ ] **Step 2: Run** `uv run pytest tests/test_manim_palette.py -v` and `uv run pytest -m manim -k "background or pipeline" -v` → FAIL.
- [ ] **Step 3: Implement** the interfaces above in `manim.py` and read `colors` in `_manim_widget.js`.
- [ ] **Step 4: Run** `make check` and `uv run pytest -m manim` → green.
- [ ] **Step 5: Commit** `feat(manim): palette background, 30 fps, scene factories, palette player`.

### Task 4: `FlowAnimation` style

**Files:**
- Modify: `banners/content/flow_animation.py` (drop `_COLORS` and `BG`)
- Test: `tests/test_flow_palette.py` (new)

**Interfaces:**
- Consumes: `Manim(..., palette=...)` from Task 3.
- Produces: `FlowAnimation.__init__(..., palette: Palette | None = None)`, `FlowAnimation._with_palette(palette) -> FlowAnimation`; module function `node_colors(palette: Palette, count: int) -> list[str]` cycling `palette.section_colors or (palette.primary, palette.secondary)`. Node fill = node color at 0.15 opacity, stroke = node color; names in `palette.text` (bold), details and arrows in `palette.muted`. Each step: one `self.play(FadeIn(node_group, shift=<0.15 toward the flow direction>), *GrowArrow(incoming), run_time=0.25, rate_func=ease_out_cubic)`; no `Write`, no `scale`, no `self.wait()`.

- [ ] **Step 1: Write the failing tests:**
  - `test_node_colors_cycle_primary_secondary`: `node_colors(Palette(primary="#1", secondary="#2"), 3) == ["#1", "#2", "#1"]`.
  - `test_node_colors_use_section_colors` (Review Focus 3): one-color `section_colors=("#9",)` → `["#9", "#9"]`; `section_colors=None` falls back to primary/secondary.
  - `test_flow_with_palette_passes_palette_to_manim`: `FlowAnimation(["A","B"])._with_palette(BLUE)` builds a `Manim` whose `palette is BLUE` (patch `Manim.render` to capture `self`).
  - `@pytest.mark.manim test_flow_steps_are_short`: render `FlowAnimation(["A","B","C","D"], quality="low")`; every cached section mp4 has an `ffprobe` duration ≤ 0.3 s.
- [ ] **Step 2: Run** `uv run pytest tests/test_flow_palette.py -v` and `uv run pytest -m manim -k flow_steps -v` → FAIL.
- [ ] **Step 3: Implement** the interfaces above for both the rows and the graph scenes.
- [ ] **Step 4: Run** `make check` and `uv run pytest -m manim` → green.
- [ ] **Step 5: Commit** `feat(flow): palette colors and 0.25 s ease-out steps`.

### Task 5: `PipelineScene` style

**Files:**
- Modify: `banners/scenes/pipeline.py` (`PipelineScene(palette=None)`; colors from the palette as in Task 4; same motion rules; drop `self.wait(1)`)
- Test: `tests/test_manim_palette.py` (extend)

- [ ] **Step 1: Write the failing test** `@pytest.mark.manim test_pipeline_steps_are_short`: every section of `Manim(PipelineScene, interactive=True)` lasts ≤ 0.3 s; and unit `test_pipeline_factory_accepts_palette`: `inspect.signature(PipelineScene).parameters` contains `palette`.
- [ ] **Step 2: Run** → FAIL.
- [ ] **Step 3: Implement**, update the docstring example.
- [ ] **Step 4: Run** `make check` and `uv run pytest -m manim` → green.
- [ ] **Step 5: Commit** `feat(scenes): PipelineScene follows the palette and the motion rules`.

### Task 6: Measure, review and close

- [ ] **Step 1:** Measure the same cold render as Task 1 Step 5; it must not exceed 2.0 s.
- [ ] **Step 2:** `uv version 0.6.0`; update README sections that mention `FlowAnimation`/`Manim` colors and `PipelineScene(palette=...)`; `uv build` + `uvx twine check dist/*`.
- [ ] **Step 3:** César reviews `test/08_manim.py`, `test/09_flow_animation.py` and `example/showcase.py` in marimo slide mode with two palettes.
- [ ] **Step 4:** Final review, then close per `CLAUDE.md` with `make check`, `uv run pytest -m manim` and both render times in the commit body.
