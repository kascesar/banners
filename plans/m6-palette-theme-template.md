# M6 — Template = Palette + Theme + layouts: Implementation Plan

> **For agentic workers:** execute with superpowers:executing-plans (inline, as
> `CLAUDE.md` requires). Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Render every slide on the 16:9 canvas through a template composed of
an independently declarable `Palette` (colors) and `Theme` (fonts, weights,
icon stroke, scale), and remove the fluid editorial style. Release 0.5.0.

**Architecture:** `Palette` and `Theme` are plain dataclasses. `Template` holds
one of each plus layouts, logos, photos, icons and bar options. At render time,
one function resolves the active palette and theme (slide > `configure` >
template), and the layouts read only `self.palette.*` and `self.theme.*` from a
copy of the template made with `dataclasses.replace`. `Slide.render()` always
delegates to the configured template, or to a default `Template()`.

**Tech Stack:** Python ≥ 3.10, marimo, pytest, ruff, uv.

**Spec:** `MILESTONES.md` → "M6 — One rendering model: Template = Palette + Theme + layouts".

## Global Constraints

- Version `0.5.0`. Breaking release: removed parameters are not deprecated, they fail.
- No slide text sized in `rem` or `px`: `grep -rnE "font-size:[0-9.]+(rem|px)" banners/` → no matches.
- Content elements in `banners/content/` must not import `banners.config` or slides.
- A user palette or theme replaces the template's one as a whole (no field merge).
- Everything in the repository is written in English; Google-style docstrings with Args/Returns.
- Commits per task on `milestone/m6-palette-theme-template`, Conventional Commits, no `Co-Authored-By`.
- Verification command for every task: `make check`.

## Review Focus

1. A user palette without `section_colors` on a preset that has them (`VIBRANT` + `palette=BLUE`): no leftover section colors. Test in Task 4.
2. `configure(palette=X)` followed later by `configure(template=Y)`: the palette still applies, because `configure` only writes the arguments it gets. Test in Task 4.
3. `Background.image(...)` on a light layout: the default dark overlay makes the text white. Test in Task 4.
4. A palette color that cannot be parsed (`primary="var(--brand)"`): rendering does not crash and the color is used as given. Test in Task 3.
5. A content element (`Text`, `Graph`, `AnimatedGraph`) rendered in a plain cell without `configure()`: works as before. Test in Task 2.

---

### Task 1: `Theme` and its use in `Template`

**Files:**
- Create: `banners/theme.py`
- Modify: `banners/template.py` (fields `font`, `heading_font`, `scale` → `theme`; `_text`, `_fs`, `_canvas`, `_resolve`; the six presets)
- Test: `tests/test_theme.py` (new), `tests/test_template.py`, `tests/test_presets.py`

**Interfaces:**
- Produces: `Theme(font: str = <current Template.font default>, heading_font: str | None = None, title_weight: int = 700, icon_stroke: float = 1.6, scale: float = 1.0)`; `Template.theme: Theme` (default `Theme()`). Layouts read `self.theme.font`, `self.theme.heading_font`, `self.theme.scale`, `self.theme.title_weight`, `self.theme.icon_stroke`.

- [ ] **Step 1: Write the failing tests** in `tests/test_theme.py`:
  - `test_theme_defaults`: `Theme()` has `heading_font is None`, `title_weight == 700`, `icon_stroke == 1.6`, `scale == 1.0`.
  - `test_title_weight_applies_to_titles`: `configure(template=Template(theme=Theme(title_weight=600)))`; the HTML of `Cover(title="A")` contains `font-weight:600`.
  - `test_icon_stroke_reaches_named_icons`: `Template(theme=Theme(icon_stroke=2.5), divider_icon="leaf")`; `Section(title="B")` HTML contains `quote('stroke-width="2.5"')`.
  - `test_theme_scale_multiplies_sizes`: replaces `test_scale_multiplies_font_sizes` in `tests/test_template.py`, using `Theme(scale=2)`.
  - In `tests/test_presets.py`, `test_heading_font_applies_to_titles_only` uses `Template(theme=Theme(heading_font="Georgia, serif"))`.
- [ ] **Step 2: Run** `uv run pytest tests/test_theme.py -v` → FAIL (`ModuleNotFoundError: banners.theme`).
- [ ] **Step 3: Implement** `Theme` in `banners/theme.py`; in `Template`, replace the `font`, `heading_font` and `scale` fields with `theme: Theme = field(default_factory=Theme)`. `_text` uses `self.theme.title_weight` when `bold`; `_resolve` passes `stroke=self.theme.icon_stroke` to `icon()`. Move each preset's `font`/`heading_font`/`scale` into `theme=Theme(...)` with the same values.
- [ ] **Step 4: Run** `make check` → all green.
- [ ] **Step 5: Commit** `feat(theme): Theme for fonts, title weight, icon stroke and scale`.

### Task 2: Remove the editorial rendering

**Files:**
- Modify: `banners/slide.py`, `banners/slides/cover.py`, `intro.py`, `section.py`, `closing.py`, `banners/config.py`, `banners/palette.py` (delete `SectionPalette`, `to_section_palette`), `banners/__init__.py`
- Modify: `test/*.py`, `example/*.py` (drop `content_kind=`, `icon=`)
- Test: `tests/test_slide.py` (rewrite), `tests/test_config.py`, `tests/test_removed_api.py` (new)

**Interfaces:**
- Consumes: `Template.render(slide)` (unchanged).
- Produces: `Slide.__init__(title, subtitle="", content=None, palette=None, footer="", background=None)`, `Slide.render()` → `(_cfg.get("template") or Template()).render(self)`; `Slide._icon_src` stays (used by `Template._src`). Subclasses keep only their own fields: `Cover(date, team, image)`, `Intro(tag, summary, team)`, `Section(number, image)`, `Closing(team, stats)`, and no `render()` override. `configure(team, date, palette, background, template)` (no `icon`).

- [ ] **Step 1: Write the failing tests:**
  - `tests/test_removed_api.py::test_removed_parameters_raise` parametrized over `Cover(title="A", content_kind="info")`, `Section(title="A", icon={"src": "x"})`, `configure(icon={"src": "x"})` → `pytest.raises(TypeError)`; `test_section_palette_is_gone`: `from banners.palette import SectionPalette` → `ImportError`.
  - `tests/test_slide.py` (replaces the editorial tests): `test_default_template_without_configure` (`configure(template=None)`; `Cover(title="A").render().text` contains `aspect-ratio:16/9`); `test_display_returns_render`.
  - `test_content_elements_render_without_configure`: `Text("**a**")`, `Graph("graph LR\n A-->B")` and `AnimatedGraph("graph LR\n A-->B")` render without any `configure()` call; and no file in `banners/content/` contains `"from .."` or `"banners.config"` in its source (manim's own `tempconfig` is fine).
  - Remove `test_configure_none_restores_editorial` from `tests/test_template.py`.
- [ ] **Step 2: Run** `uv run pytest tests/test_removed_api.py tests/test_slide.py -v` → FAIL.
- [ ] **Step 3: Implement:** delete from `slide.py` everything except `__init__`, `render`, `_display_` and `_icon_src` (with the module constants it no longer needs); delete `_render_banner`, `_render_stats` and the `render` overrides in `banners/slides/`; drop `content_kind` and `icon` from every signature and from `configure`/`_state`; delete `SectionPalette` and its export. `Section.__init__` takes `palette: Palette | None` without conversion. Update docstrings of the edited classes.
- [ ] **Step 4: Migrate the notebooks** in `test/` and `example/`: remove `content_kind=` and `icon=` arguments; nothing else.
- [ ] **Step 5: Run** `make check` and `grep -rnE "font-size:[0-9.]+(rem|px)" banners/` → green, no matches.
- [ ] **Step 6: Commit** `feat!: render every slide on the 16:9 canvas; remove the editorial style`.

### Task 3: `Palette` by role, composed into `Template`

**Files:**
- Modify: `banners/palette.py` (rewrite), `banners/template.py` (color fields → `palette`; presets), `test/01_intro.py`, `example/showcase.py`, `example/ondas_electromagneticas.py` (`Palette(start=...)`, `.gradient`)
- Test: `tests/test_palette.py` (rewrite), `tests/test_template.py`, `tests/test_presets.py`

**Interfaces:**
- Produces: `Palette(primary="#e4572e", secondary="#2a6fdb", dark="#404040", closing_bg="#363e45", light="#f5f5f5", text="#343e46", muted="#6b7280", on_dark="#f5f5f5", panel="#ffffff", icon_color: str | None = None, section_colors: tuple | None = None, bar_colors: tuple | None = None)`. `ORANGE = Palette()`. `BLUE`, `GREEN`, `PURPLE`, `GRAY` set `primary` = current `end`, `dark` = current `start`, `closing_bg` = current `mid`, other fields default (BLUE `#2f6fd0/#0f2340/#16325c`, GREEN `#2e8b57/#0f2a1f/#173d2d`, PURPLE `#6e56cf/#221a3a/#2e2450`, GRAY `#5b6470/#1a1d21/#2a2e34`). `Template.palette: Palette` (default `Palette()`); layouts read only `self.palette.<color>`.

- [ ] **Step 1: Write the failing tests:**
  - `tests/test_palette.py`: `test_orange_is_default_palette` (`ORANGE == Palette()`, `ORANGE.primary == "#e4572e"`); `test_presets_by_role` parametrized with the four tuples above; `test_palette_has_no_gradient_fields` (`Palette(start="#000")` → `TypeError`).
  - `tests/test_template.py`: fixture uses `Template(palette=Palette(primary="#ff6600", secondary="#054af6"), ...)`; `test_template_default_palette_is_orange`.
  - `tests/test_presets.py`: every `Template(<color>=...)` becomes `Template(palette=Palette(<color>=...))`; `test_every_preset_has_palette_and_theme` (`isinstance(t.palette, Palette) and isinstance(t.theme, Theme)` for all `PRESETS`).
  - Review Focus 4: `test_unparseable_palette_color_is_used_as_is`: `Template(palette=Palette(primary="var(--brand)"))` renders `Cover(title="A")` without error and the HTML contains `var(--brand)`.
- [ ] **Step 2: Run** `uv run pytest tests/test_palette.py tests/test_template.py tests/test_presets.py -v` → FAIL.
- [ ] **Step 3: Implement** the new `Palette`; in `Template`, replace the twelve color fields with `palette: Palette = field(default_factory=Palette)` and rewrite every `self.<color>` reference as `self.palette.<color>` (a script with one `assert` per replaced name is fine). Rewrite the six presets as `Template(palette=Palette(...), theme=Theme(...), <layout fields>)` with today's values.
- [ ] **Step 4: Migrate** `Palette(start=..., mid=..., end=...)` and `.gradient` in the three notebooks to role-based palettes (`Palette(primary=<end>, dark=<start>, closing_bg=<mid>)`); `Background.gradient(...)` calls stay.
- [ ] **Step 5: Run** `make check` → green.
- [ ] **Step 6: Commit** `feat(palette)!: role-based Palette composed into Template`.

### Task 4: Style resolution, `configure(theme=)` and canvas backgrounds

**Files:**
- Modify: `banners/template.py` (`render`, `_canvas`, new `_resolve_style`), `banners/config.py` (`theme`)
- Test: `tests/test_style.py` (new)

**Interfaces:**
- Consumes: `Palette`, `Theme`, `Template.palette`, `Template.theme`, `Slide.palette`, `Slide.background`.
- Produces: `_resolve_style(template: Template, slide) -> tuple[Palette, Theme]` (module-level, in `template.py`): palette = `slide.palette` or `config.get("palette")` or `template.palette`; theme = `config.get("theme")` or `template.theme`. `configure(..., theme=_UNSET, ...)`. `Template.render` builds `active = replace(self, palette=p, theme=t)` and renders the layout on `active`. When the slide has a `background`, `_canvas` paints `background.css` instead of the layout color, and if `background.text_color()` returns a color `c`, the palette used for that slide is `replace(p, text=c, muted=c, on_dark=c)`.

- [ ] **Step 1: Write the failing tests** in `tests/test_style.py`:
  - `test_slide_palette_beats_configure_and_template`: template `palette=Palette(primary="#111111")`, `configure(palette=Palette(primary="#222222"))`, slide `palette=Palette(primary="#333333")` → HTML contains `#333333` and not `#222222` or `#111111`.
  - `test_configure_palette_beats_template` and `test_template_palette_is_the_fallback`.
  - `test_configure_theme_beats_template`: template `theme=Theme(font="Serif1")`, `configure(theme=Theme(font="Sans2"))` → `font-family:Sans2` in HTML, `Serif1` absent.
  - `test_palette_and_theme_work_without_template`: `configure(template=None, palette=BLUE, theme=Theme(font="X"))`; `Cover(title="A")` HTML contains `#2f6fd0` and `font-family:X`.
  - `test_every_preset_with_user_palette` parametrized over `PRESETS`: with `palette=BLUE`, `Cover`, `Intro`, `Section` (divider and with content) and `Closing(stats=...)` render and contain `#2f6fd0`.
  - Review Focus 1: `test_user_palette_drops_preset_section_colors`: `configure(template=VIBRANT, palette=BLUE)`; HTML of `Section(title="S")` contains none of `VIBRANT.palette.section_colors`.
  - Review Focus 2: `test_palette_survives_later_template_change`: `configure(palette=BLUE)` then `configure(template=TERRA)` → `#2f6fd0` in `Cover` HTML.
  - `test_background_paints_canvas`: `Cover(title="A", background=Background.color("#000000"))` → `background:#000000` and `color:#ffffff` in HTML.
  - Review Focus 3: `test_background_image_makes_text_white`: `Section(title="A", content=Text("x"), background=Background.image("https://example.org/a.jpg"))` → `url(https://example.org/a.jpg)` and `#ffffff` in HTML.
- [ ] **Step 2: Run** `uv run pytest tests/test_style.py -v` → FAIL.
- [ ] **Step 3: Implement** `_resolve_style`, the `theme` argument of `configure` (with docstring entry) and the background handling in `render`/`_canvas`.
- [ ] **Step 4: Run** `make check` → green.
- [ ] **Step 5: Commit** `feat(template): resolve palette and theme by precedence; backgrounds on the canvas`.

### Task 5: Public API, docs and version 0.5.0

**Files:**
- Modify: `banners/__init__.py` (export `Theme`; module docstring example), `banners/template.py` and `banners/palette.py` module docstrings, `README.md` (sections "Upgrading from 0.2" → "Upgrading to 0.5", "Global configuration", "Slides", "Palettes", "Slide backgrounds", "Templates"), `CLAUDE.md` ("Architecture": `Slide` base class, Templates, Palette system), `pyproject.toml` + `uv.lock` (`uv version 0.5.0`)
- Test: `tests/test_presets.py::test_presets_and_icons_are_exported` extended with `"Theme"`, `"Palette"`; `"SectionPalette"` not in `banners.__all__`.

- [ ] **Step 1: Extend the export test** and run it → FAIL on `Theme`.
- [ ] **Step 2: Implement** the exports and rewrite the listed README and `CLAUDE.md` sections for the 0.5 model; "Upgrading to 0.5" lists every removed parameter and its replacement (`content_kind` → none; `icon=` → `Template(mark=...)`; `Palette(start, mid, end)` → `Palette(primary, dark, closing_bg)`; `SectionPalette` → `Palette`). The full README rewrite is M8.
- [ ] **Step 3: Run** `uv version 0.5.0`, `make check`, `rm -rf dist && uv build && uvx twine check dist/*` → green, both files PASSED.
- [ ] **Step 4: Commit** `docs: 0.5 model in README, CLAUDE.md and docstrings; version 0.5.0`.

### Task 6: Visual review

Not code; produces no repository files.

- [ ] **Step 1:** Write a script in the session scratchpad that renders, for `EXECUTIVE`, `INSTITUTIONAL`, `COSMOS`, `VIBRANT`, `TERRA` and the default `Template()`, the layouts `Cover`, `Intro`, `Section` (divider and with content) and `Closing`, each with its own palette and with `palette=BLUE`, into one HTML page. `BECH` is left out of the published page because it imitates a real organization's branding; César reviews it in `test/` notebooks instead.
- [ ] **Step 2:** Publish the page as a private artifact and give César the link.
- [ ] **Step 3:** César reviews the gallery and presents one existing deck full screen in marimo slide mode. Fixes he asks for go back through Tasks 1–4 as new commits.
- [ ] **Step 4:** Close the milestone per `CLAUDE.md`: mark M6 `[x]`, add the Log line, paste the `make check` output in the commit body, commit and stop.
