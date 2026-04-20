"""Manim content element — renders a Scene and embeds it in a slide."""

import tempfile
import uuid
from pathlib import Path

import marimo as mo

_MERMAID_JS = (Path(__file__).parent.parent / "static" / "mermaid.min.js").read_text()


class Manim:
    """Renders a Manim Scene and embeds the result inside a slide.

    Requires the optional `manim` dependency:

    ```bash
    uv pip install "banners[manim]"
    ```

    The scene is rendered on the first `render()` call and the result is
    cached — subsequent calls return the same component without re-rendering.

    Args:
        scene: A Manim `Scene` subclass (pass the class, not an instance).
        format: Output format. `"gif"` and `"png"` embed as `mo.image`;
            `"mp4"` embeds as `mo.video`. Defaults to `"gif"`.
        quality: Render quality. One of `"low"`, `"medium"`, `"high"`.
            Defaults to `"low"`.
        interactive: When `True`, the scene is rendered section by section
            (using `self.next_section()` markers) and a click-to-advance
            HTML component is returned. Each click shows the next section.
            The scene must define sections with `self.next_section("name")`.

    Example — standard GIF:
        ```python
        from manim import Scene, Circle, Create
        from banners.content import Manim

        class CircleScene(Scene):
            def construct(self):
                self.play(Create(Circle()))

        Section(title="Demo", content=Manim(CircleScene)).render()
        ```

    Example — click-to-advance (requires `next_section()` in the scene):
        ```python
        from banners.content import Manim
        from banners.scenes import PipelineScene

        Section(
            title="Pipeline",
            content=Manim(PipelineScene, interactive=True),
        ).render()
        ```
    """

    _QUALITY_MAP = {
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
    ) -> None:
        self.scene = scene
        self.format = format
        self.quality = quality
        self.interactive = interactive
        self._cached: "mo.Html | None" = None

    def render(self) -> mo.Html:
        """Render the scene and return a marimo component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
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

    def _render_static(self, tempconfig) -> mo.Html:
        quality = self._QUALITY_MAP.get(self.quality, "low_quality")
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempconfig({
                "media_dir": tmpdir,
                "format": self.format,
                "quality": quality,
                "disable_caching": True,
            }):
                scene_cls = self.scene() if callable(self.scene) and not isinstance(self.scene, type) else self.scene
                instance = scene_cls()
                instance.render()
                data = self._find_output(tmpdir, self.format)

        if data is None:
            return mo.callout(mo.md("Manim rendered but no output file was found."), kind="danger")

        return mo.image(data) if self.format in ("gif", "png") else mo.video(data)

    def _render_interactive(self, tempconfig) -> mo.Html:
        """Render each section as mp4 and build a click-to-advance component."""
        quality = self._QUALITY_MAP.get(self.quality, "low_quality")
        frames: list[bytes] = []
        frame_fmt = "mp4"

        with tempfile.TemporaryDirectory() as tmpdir:
            with tempconfig({
                "media_dir": tmpdir,
                "save_sections": True,
                "quality": quality,
                "disable_caching": True,
            }):
                scene_cls = self.scene() if callable(self.scene) and not isinstance(self.scene, type) else self.scene
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

        return self._build_interactive_html(frames)

    @staticmethod
    def _build_interactive_html(frames: list[bytes]) -> mo.Html:
        import base64
        uid = uuid.uuid4().hex[:10]
        b64_frames = [
            f"data:video/mp4;base64,{base64.b64encode(f).decode()}"
            for f in frames
        ]

        sources_html = "\n".join(
            f'<source data-src="{u}" type="video/mp4">' for u in b64_frames
        )

        html = f"""
<div style="text-align:center;user-select:none;">
  <video id="manim-vid-{uid}"
         src="{b64_frames[0]}"
         autoplay loop muted playsinline
         style="max-width:100%;border-radius:0.5rem;cursor:pointer;">
  </video>
  <div style="margin-top:0.5rem;font-size:0.8rem;color:#9ca3af;">
    <span id="manim-step-{uid}">1</span> / {len(frames)} &mdash; click to advance
  </div>
</div>
<script>
(function() {{
    var srcs  = [{",".join(f'"{u}"' for u in b64_frames)}];
    var idx   = 0;
    var vid   = document.getElementById("manim-vid-{uid}");
    var label = document.getElementById("manim-step-{uid}");
    vid.addEventListener("click", function() {{
        idx = (idx + 1) % srcs.length;
        vid.src = srcs[idx];
        vid.play();
        label.textContent = idx + 1;
    }});
}})();
</script>
"""
        return mo.Html(html)

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
