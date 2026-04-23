"""Manim content element -- renders a Scene and embeds it in a slide."""

import base64
import contextlib
import io
import os
import tempfile
from pathlib import Path

import anywidget
import marimo as mo
import traitlets


class _ManimInteractiveWidget(anywidget.AnyWidget):
    _esm = r"""
function render({ model, el }) {
    const srcs = model.get("srcs");
    let idx = 0;
    let busy = false;

    el.style.cssText = "text-align:center;user-select:none;";

    const wrap = document.createElement("div");
    const maxW = model.get("width") || "100%";
    wrap.style.cssText = "display:block;width:100%;max-width:" + maxW + ";margin:0 auto;";

    const stage = document.createElement("div");
    stage.style.cssText = "position:relative;width:100%;overflow:hidden;border-radius:0.5rem;background:#000;cursor:pointer;";
    wrap.appendChild(stage);

    function makeVideo() {
        const v = document.createElement("video");
        v.muted = true;
        v.setAttribute("playsinline", "");
        v.loop = false;
        v.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;display:block;";
        return v;
    }

    const buf = [makeVideo(), makeVideo()];
    buf[0].style.zIndex = "1";
    buf[1].style.zIndex = "0";
    buf[0].src = srcs[0];
    buf[0].autoplay = true;
    stage.appendChild(buf[0]);
    stage.appendChild(buf[1]);

    buf[0].addEventListener("loadedmetadata", function onMeta() {
        buf[0].removeEventListener("loadedmetadata", onMeta);
        stage.style.aspectRatio = buf[0].videoWidth + " / " + buf[0].videoHeight;
    });

    function whenReady(video, cb) {
        let done = false;
        function fire() {
            if (done) return;
            done = true;
            video.removeEventListener("canplay", fire);
            cb();
        }
        video.addEventListener("canplay", fire);
        if (video.readyState >= 3) fire();
    }

    function preloadNext() {
        const next = idx + 1;
        if (next < srcs.length) { buf[1].src = srcs[next]; buf[1].load(); }
    }
    preloadNext();

    // Controls bar: [←]  "2 / 5"  [→]  [▶]
    const controls = document.createElement("div");
    controls.style.cssText = "display:flex;align-items:center;justify-content:center;gap:1rem;margin-top:0.5rem;";

    function makeBtn(text) {
        const b = document.createElement("button");
        b.textContent = text;
        b.style.cssText = "background:#1f2937;color:#9ca3af;border:1px solid #374151;"
            + "border-radius:0.375rem;padding:0.2rem 0.7rem;cursor:pointer;font-size:0.85rem;";
        return b;
    }

    const btnPrev = makeBtn("←");
    const label = document.createElement("span");
    label.style.cssText = "font-size:0.8rem;color:#9ca3af;min-width:4rem;display:inline-block;";
    label.textContent = "1 / " + srcs.length;
    const btnNext = makeBtn("→");
    const btnAuto = makeBtn("▶");
    controls.append(btnPrev, label, btnNext, btnAuto);

    function updateLabel() {
        label.textContent = (idx + 1) + " / " + srcs.length;
    }

    // Autoplay state (may be pre-enabled via model)
    let autoplay = model.get("autoplay");

    function onEnded() {
        if (autoplay) goForward();
    }

    function attachAutoEnded() {
        buf[0].addEventListener("ended", onEnded, { once: true });
    }

    function transition(nextIdx) {
        if (busy) return;
        busy = true;
        idx = nextIdx;
        updateLabel();
        buf[1].src = srcs[idx];
        buf[1].load();
        whenReady(buf[1], function () {
            buf[1].play();
            buf[0].style.zIndex = "0";
            buf[1].style.zIndex = "1";
            buf.reverse();
            busy = false;
            preloadNext();
            if (autoplay) attachAutoEnded();
        });
    }

    function goForward() { transition((idx + 1) % srcs.length); }
    function goBack()    { transition(idx === 0 ? srcs.length - 1 : idx - 1); }

    stage.addEventListener("click", goForward);
    btnNext.addEventListener("click", goForward);
    btnPrev.addEventListener("click", goBack);

    btnAuto.addEventListener("click", function () {
        autoplay = !autoplay;
        if (autoplay) {
            btnAuto.style.color = "#60a5fa";
            btnAuto.style.borderColor = "#3b82f6";
            if (buf[0].ended) { goForward(); } else { attachAutoEnded(); }
        } else {
            btnAuto.style.color = "#9ca3af";
            btnAuto.style.borderColor = "#374151";
        }
    });

    wrap.appendChild(controls);
    el.appendChild(wrap);

    // Apply initial autoplay state
    if (autoplay) {
        btnAuto.style.color = "#60a5fa";
        btnAuto.style.borderColor = "#3b82f6";
        attachAutoEnded();
    }
}
export default { render };
"""
    srcs = traitlets.List(traitlets.Unicode()).tag(sync=True)
    width = traitlets.Unicode("100%").tag(sync=True)
    autoplay = traitlets.Bool(False).tag(sync=True)


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
        width: str = "100%",
        autoplay: bool = False,
    ) -> None:
        self.scene = scene
        self.format = format
        self.quality = quality
        self.interactive = interactive
        self.width = width
        self.autoplay = autoplay
        self._cached = None

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
            old_level = logging.root.manager.loggerDict.copy()
            logging.disable(logging.CRITICAL)
            try:
                yield
            finally:
                logging.disable(logging.NOTSET)

    def _render_static(self, tempconfig):
        quality = self._QUALITY_MAP.get(self.quality, "low_quality")
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempconfig({
                "media_dir": tmpdir,
                "format": self.format,
                "quality": quality,
                "verbosity": "CRITICAL",
                "disable_caching": True,
            }):
                scene_cls = self.scene if isinstance(self.scene, type) else self.scene
                with self._quiet():
                    instance = scene_cls()
                    instance.render()
                data = self._find_output(tmpdir, self.format)

        if data is None:
            return mo.callout(mo.md("Manim rendered but no output file was found."), kind="danger")

        return mo.image(data) if self.format in ("gif", "png") else mo.video(data)

    def _render_interactive(self, tempconfig):
        """Render each section as mp4 and return a click-to-advance anywidget."""
        quality = self._QUALITY_MAP.get(self.quality, "low_quality")
        frames: list[bytes] = []

        with tempfile.TemporaryDirectory() as tmpdir:
            with tempconfig({
                "media_dir": tmpdir,
                "save_sections": True,
                "quality": quality,
                "verbosity": "CRITICAL",
                "disable_caching": True,
            }):
                scene_cls = self.scene if isinstance(self.scene, type) else self.scene
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

        srcs = [
            f"data:video/mp4;base64,{base64.b64encode(f).decode()}"
            for f in frames
        ]
        return _ManimInteractiveWidget(srcs=srcs, width=self.width, autoplay=self.autoplay)

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
