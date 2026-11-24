"""Manim content element -- renders a Scene and embeds it in a slide."""

import base64
import contextlib
import copy
import hashlib
import inspect
import io
import json
import tempfile
from pathlib import Path
from typing import ClassVar

_HERE = Path(__file__).parent

FRAME_RATE = 30
"""Frames per second of every render. Manim's "low" preset is 15 fps, which
leaves a 0.25 s step with about 4 frames."""

import marimo as mo


class Manim:
    """Renders a Manim Scene and embeds the result inside a slide.

    Requires the optional ``manim`` dependency::

        uv pip install "banners[manim]"

    The scene is rendered on the first ``render()`` call and cached --
    subsequent calls return the same component without re-rendering.

    Args:
        scene: A Manim ``Scene`` subclass (pass the class, not an instance).
        format: Output format. ``"gif"`` and ``"png"`` embed as ``mo.image``;
            ``"mp4"`` embeds as ``mo.video``. Defaults to ``"gif"``.
        quality: Render quality. One of ``"low"``, ``"medium"``, ``"high"``.
            Defaults to ``"low"``.
        interactive: When ``True``, the scene is rendered section by section
            and a click-to-advance widget is returned. The scene must define
            steps with ``self.next_section("name")``.
        palette: Colors for the render. The background is ``palette.panel``
            (a scene may still set its own) and the player controls use
            ``muted`` and ``primary``. ``None`` uses the default ``Palette()``;
            on a slide the template passes the slide palette.
    """

    _QUALITY_MAP: ClassVar[dict[str, str]] = {
        "low": "low_quality",
        "medium": "medium_quality",
        "high": "high_quality",
    }

    def __init__(
        self,
        scene,
        format: str = "gif",
        quality: str = "low",
        interactive: bool = False,
        width: str = "100%",
        autoplay: bool = False,
        _extra_key: str = "",
        palette=None,
    ) -> None:
        self.scene = scene
        self.format = format
        self.quality = quality
        self.interactive = interactive
        self.width = width
        self.autoplay = autoplay
        self._extra_key = _extra_key
        self.palette = palette
        self._cached = None

    @property
    def _palette(self):
        """The palette used for the render: the given one or the default `Palette()`."""
        from banners.palette import Palette

        return self.palette or Palette()

    def _with_palette(self, palette) -> "Manim":
        """Return a copy that renders with a slide palette.

        Args:
            palette: The `banners.Palette` of the slide.

        Returns:
            A new `Manim` with `palette` set and no cached render.
        """
        styled = copy.copy(self)
        styled.palette = palette
        styled._cached = None
        return styled

    def _scene_class(self):
        """Return the scene class to render.

        `scene` may be a `Scene` subclass or a factory function that returns
        one (such as `banners.scenes.PipelineScene`); a factory that accepts a
        `palette` argument receives the render palette.

        Returns:
            The `Scene` subclass.
        """
        if inspect.isclass(self.scene):
            return self.scene
        if "palette" in inspect.signature(self.scene).parameters:
            return self.scene(palette=self._palette)
        return self.scene()

    def _render_config(self) -> dict:
        """Manim settings shared by static and interactive renders.

        Returns:
            Settings for `manim.tempconfig`: the palette panel as background
            and 30 frames per second for every quality.
        """
        return {"background_color": self._palette.panel, "frame_rate": FRAME_RATE}

    def _player_colors(self) -> dict:
        """Colors of the click-to-advance player.

        Returns:
            `{"panel": ..., "muted": ..., "primary": ...}` from the palette.
        """
        p = self._palette
        return {"panel": p.panel, "muted": p.muted, "primary": p.primary}

    def _cache_key(self) -> str:
        try:
            src = inspect.getsource(self.scene)
        except OSError:
            src = self.scene.__qualname__
        raw = (
            f"{src}|{self.quality}|{self.format}|{self.interactive}|{self._extra_key}"
            f"|{self._palette!r}|fps={FRAME_RATE}"
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:24]

    @staticmethod
    def _cache_root() -> Path:
        d = Path.home() / ".cache" / "banners" / "manim"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def render(self):
        """Render the scene and return a marimo component."""
        if self._cached is not None:
            return self._cached

        try:
            from manim import tempconfig
        except ImportError:
            return mo.callout(
                mo.md("`manim` is not installed. Run: `uv pip install 'banners[manim]'`"),
                kind="warn",
            )

        if self.interactive:
            self._cached = self._render_interactive(tempconfig)
        else:
            self._cached = self._render_static(tempconfig)

        return self._cached

    @staticmethod
    @contextlib.contextmanager
    def _quiet():
        """Suppress all Manim console output."""
        import logging
        sink = io.StringIO()
        with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
            logging.disable(logging.CRITICAL)
            try:
                yield
            finally:
                logging.disable(logging.NOTSET)

    def _render_static(self, tempconfig):
        key = self._cache_key()
        cache_file = self._cache_root() / f"{key}.{self.format}"

        if cache_file.exists():
            data = cache_file.read_bytes()
        else:
            quality = self._QUALITY_MAP.get(self.quality, "low_quality")
            with tempfile.TemporaryDirectory() as tmpdir, tempconfig({
                "media_dir": tmpdir,
                "format": self.format,
                "quality": quality,
                "verbosity": "CRITICAL",
                "disable_caching": True,
                **self._render_config(),
            }):
                scene_cls = self._scene_class()
                with self._quiet():
                    instance = scene_cls()
                    instance.render()
                data = self._find_output(tmpdir, self.format)

            if data is None:
                return mo.callout(mo.md("Manim rendered but no output file was found."), kind="danger")
            cache_file.write_bytes(data)

        return mo.image(data) if self.format in ("gif", "png") else mo.video(data)

    def _render_interactive(self, tempconfig):
        """Render each section as mp4 and return a click-to-advance anywidget."""
        key = self._cache_key()
        cache_dir = self._cache_root() / key
        cached_frames = sorted(cache_dir.glob("*.mp4")) if cache_dir.exists() else []

        if cached_frames:
            frames = [p.read_bytes() for p in cached_frames]
        else:
            quality = self._QUALITY_MAP.get(self.quality, "low_quality")
            frames: list[bytes] = []

            with tempfile.TemporaryDirectory() as tmpdir:
                with tempconfig({
                    "media_dir": tmpdir,
                    "save_sections": True,
                    "quality": quality,
                    "verbosity": "CRITICAL",
                    "disable_caching": True,
                    **self._render_config(),
                }):
                    scene_cls = self._scene_class()
                    with self._quiet():
                        instance = scene_cls()
                        instance.render()

                section_dir = self._find_sections_dir(Path(tmpdir))
                if section_dir and section_dir.exists():
                    for path in sorted(section_dir.glob("*.mp4")):
                        frames.append(path.read_bytes())

            if not frames:
                return mo.callout(
                    mo.md("No sections found. Add `self.next_section()` calls to the scene."),
                    kind="warn",
                )

            cache_dir.mkdir(parents=True, exist_ok=True)
            for i, frame in enumerate(frames):
                (cache_dir / f"{i:04d}.mp4").write_bytes(frame)

        srcs = [
            f"data:video/mp4;base64,{base64.b64encode(f).decode()}"
            for f in frames
        ]
        return self._build_iframe_player(srcs, self.width, self.autoplay, self._player_colors())

    @staticmethod
    def _build_iframe_player(srcs: list, width: str, autoplay: bool, colors: dict) -> mo.Html:
        js = (_HERE / "_manim_widget.js").read_text()
        srcs_json = json.dumps(srcs)
        autoplay_json = json.dumps(autoplay)
        colors_json = json.dumps(colors)
        html = f"""<!DOCTYPE html><html><head>
<meta charset="utf-8">
<style>*{{margin:0;padding:0;box-sizing:border-box;}}body{{background:{colors["panel"]};}}</style>
</head><body>
<div id="root"></div>
<script type="module">
const srcs = {srcs_json};
const autoplay = {autoplay_json};
const colors = {colors_json};
const model = {{
    get(k) {{
        if (k === "srcs") return srcs;
        if (k === "width") return "100%";
        if (k === "autoplay") return autoplay;
        if (k === "colors") return colors;
    }}
}};
{js.replace("export default { render };", "")}
render({{ model, el: document.getElementById("root") }});
</script>
</body></html>"""
        data_url = "data:text/html;base64," + base64.b64encode(html.encode()).decode()
        return mo.Html(
            f'<iframe src="{data_url}" '
            f'style="width:{width};aspect-ratio:16/9;border:none;display:block;" '
            f'allowfullscreen></iframe>'
        )

    @staticmethod
    def _find_output(directory: str, fmt: str) -> "bytes | None":
        for path in Path(directory).rglob(f"*.{fmt}"):
            return path.read_bytes()
        return None

    @staticmethod
    def _find_sections_dir(root: Path) -> "Path | None":
        for d in root.rglob("sections"):
            if d.is_dir():
                return d
        return None
