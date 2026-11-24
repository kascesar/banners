"""Generate the README images in `media/`.

The README shows a gallery of the same slide drawn with each public template
and one GIF per part of `example/showcase.py`. This script renders both in
headless Chromium (Playwright) so they always match the current look.

Run it with `make readme-images` (it installs Chromium first). It overwrites
the files in `media/`; commit them together with the change that altered the
look.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media"
SHOWCASE = ROOT / "example" / "showcase.py"
ONDAS = ROOT / "example" / "ondas_electromagneticas.py"
# The 16:9 slide canvas drawn by `Template.render` (marimo normalizes the style
# attribute, so match the property name only).
CANVAS = '[style*="container-type"]'
# The part title animations of the showcase (MP4 videos). Interactive players
# are iframes, so a video in the page is always a title.
PART_NAMES = ["showcase-1-slide-types", "showcase-2-content-types", "showcase-3-backgrounds"]
GALLERY_WIDTH = 960
GIF_WIDTH = 800


def group_by_part(kinds: list[str]) -> list[list[int]]:
    """Split the slides of the exported showcase into its parts.

    Each part of the showcase starts with a title animation, followed by its
    slides.

    Args:
        kinds: `"title"` or `"slide"` for each element, in document order.

    Returns:
        The indexes of the slides of each part, split at every title; empty
        groups are dropped.
    """
    groups: list[list[int]] = [[]]
    for i, kind in enumerate(kinds):
        if kind == "title":
            groups.append([])
        else:
            groups[-1].append(i)
    return [g for g in groups if g]


def make_gif(frames: list[Path], out: Path, duration: int = 1500) -> None:
    """Join PNG screenshots into a looping GIF with hard cuts.

    Args:
        frames: PNG files, one per slide, in order.
        out: Path of the GIF to write.
        duration: Time each slide stays on screen, in milliseconds.
    """
    from PIL import Image

    # Every frame gets the same 16:9 size: a smaller frame would leave parts of
    # the previous slide visible around it.
    size = (GIF_WIDTH, GIF_WIDTH * 9 // 16)
    images = [Image.open(path).convert("RGB").resize(size, Image.LANCZOS) for path in frames]
    images[0].save(out, save_all=True, append_images=images[1:], duration=duration, loop=0, optimize=True)


# The gallery slide, one marimo cell per template. Plots are drawn by the
# marimo front end, so the gallery is exported like the showcase.
GALLERY_NOTEBOOK = """
import marimo

app = marimo.App(width="full")


@app.cell
def _():
    import matplotlib.pyplot as plt

    from banners import COSMOS, EXECUTIVE, INSTITUTIONAL, TERRA, VIBRANT, Template, configure
    from banners.content import Plot, Text
    from banners.slides import Section

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot([1, 2, 3, 4], [3.1, 3.8, 4.6, 5.9], linewidth=2.5, marker="o")
    ax.set_xticks([1, 2, 3, 4], ["Q1", "Q2", "Q3", "Q4"])
    ax.set_title("Revenue (M$)")
    fig.tight_layout()
    return COSMOS, EXECUTIVE, INSTITUTIONAL, Plot, Section, TERRA, Template, Text, VIBRANT, configure, fig
"""
GALLERY_CELL = """

@app.cell
def _(COSMOS, EXECUTIVE, INSTITUTIONAL, Plot, Section, TERRA, Template, Text, VIBRANT, configure, fig):
    configure(template={template}, team="Data Team", date="2026")
    Section(
        title="Quarterly results",
        subtitle="Revenue grew every quarter.",
        content=[
            Text("- Revenue up **90%** over the year\\n- Churn down to **2.1%**\\n- Two new markets opened"),
            Plot(fig),
        ],
    ).render()
    return
"""
TEMPLATES = {
    "default": "Template()", "executive": "EXECUTIVE", "institutional": "INSTITUTIONAL",
    "cosmos": "COSMOS", "vibrant": "VIBRANT", "terra": "TERRA",
}


def export(notebook: Path, out: Path) -> Path:
    """Run a marimo notebook and export it as static HTML.

    Args:
        notebook: The notebook file.
        out: The HTML file to write.

    Returns:
        `out`.
    """
    subprocess.run(["marimo", "export", "html", str(notebook), "-o", str(out)], check=True)
    return out


def shoot(page, html_path: Path, out_dir: Path, prefix: str) -> tuple[list[str], list[Path | None]]:
    """Screenshot every slide canvas of a page.

    Args:
        page: A Playwright page.
        html_path: The HTML file to open.
        out_dir: Directory for the PNG files.
        prefix: File name prefix of the PNG files.

    Returns:
        The kind of each element (`"title"` or `"slide"`) in document order,
        and the PNG of each element (`None` for titles).
    """
    page.goto(html_path.as_uri())
    page.wait_for_timeout(8000)
    # Hide what marimo pins on top of the page (header bar, "made with marimo").
    page.evaluate(
        "for (const e of document.querySelectorAll('body *'))"
        "  if (getComputedStyle(e).position === 'fixed') e.style.visibility = 'hidden';"
    )
    kinds, shots = [], []
    for i, element in enumerate(page.locator(f"video, {CANVAS}").all()):
        if element.evaluate("e => e.tagName") == "VIDEO":
            kinds.append("title")
            shots.append(None)
            continue
        # A slide drawn inside another slide is captured with its parent.
        if element.evaluate(f"e => !!e.parentElement.closest('{CANVAS}')"):
            continue
        # ponytail: an anywidget (AnimatedGraph) needs the marimo kernel and shows
        # an error in a static export; that slide is left out.
        if element.evaluate("e => !!e.querySelector('marimo-anywidget')"):
            continue
        element.scroll_into_view_if_needed()
        # Animation players load their video once they are on screen.
        if element.evaluate("e => !!e.querySelector('iframe')"):
            page.wait_for_timeout(4000)
        path = out_dir / f"{prefix}-{i:03d}.png"
        element.screenshot(path=path)
        kinds.append("slide")
        shots.append(path)
    return kinds, shots


def gif_command(
    video: Path, out: Path, box: tuple[int, int, int, int], fps: int = 12, width: int = 800, start: float = 0.0
) -> list[str]:
    """Build the ffmpeg command that turns a screen recording into a GIF.

    The recording is cropped to the slide, resampled to `fps` and scaled to
    `width`; a palette computed from the clip keeps the colors clean.

    Args:
        video: The recording (WebM from Playwright).
        out: Path of the GIF to write.
        box: Area to keep, as (x, y, width, height) in video pixels.
        fps: Frames per second of the GIF.
        width: Width of the GIF in pixels; the height keeps the proportion.
        start: Seconds to skip at the beginning of the recording.

    Returns:
        The command, ready for `subprocess.run`.
    """
    x, y, w, h = box
    chain = f"crop={w}:{h}:{x}:{y},fps={fps},scale={width}:-1:flags=lanczos"
    graph = f"[0:v]{chain},split[a][b];[a]palettegen=stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4"
    return ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.2f}", "-i", str(video),
            "-filter_complex", graph, "-loop", "0", str(out)]


def record_player_gif(browser, html: Path, out: Path, title: str, clicks: int, step_ms: int) -> None:
    """Record a slide with a click-through animation while it advances, as a GIF.

    Args:
        browser: A Playwright browser.
        html: The exported notebook that holds the slide.
        out: Path of the GIF to write.
        title: Text that identifies the slide (its title).
        clicks: How many times to advance the animation.
        step_ms: Time each step stays on screen, in milliseconds.
    """
    import time

    size = {"width": 1600, "height": 1000}
    with tempfile.TemporaryDirectory() as videos:
        context = browser.new_context(viewport=size, record_video_dir=videos, record_video_size=size)
        opened = time.monotonic()
        page = context.new_page()
        page.goto(html.as_uri())
        page.wait_for_timeout(8000)
        page.evaluate(
            "for (const e of document.querySelectorAll('body *'))"
            "  if (getComputedStyle(e).position === 'fixed') e.style.visibility = 'hidden';"
        )
        slide = page.locator(CANVAS).filter(has_text=title).filter(has=page.locator("iframe")).first
        slide.scroll_into_view_if_needed()
        page.wait_for_timeout(4000)
        box = slide.bounding_box()
        player = slide.locator("iframe").bounding_box()
        start = time.monotonic() - opened
        page.wait_for_timeout(step_ms)
        for _ in range(clicks):
            page.mouse.click(player["x"] + player["width"] / 2, player["y"] + player["height"] / 2)
            page.wait_for_timeout(step_ms)
        video = page.video.path()
        context.close()
        crop = tuple(round(v) for v in (box["x"], box["y"], box["width"], box["height"]))
        subprocess.run(gif_command(Path(video), out, crop, start=start), check=True)


def main() -> None:
    """Write the template gallery PNGs and the showcase GIFs to `media/`."""
    from PIL import Image
    from playwright.sync_api import sync_playwright

    MEDIA.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        tmp = Path(tmp)
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1700, "height": 1100}, device_scale_factor=2)

        notebook = tmp / "gallery.py"
        notebook.write_text(GALLERY_NOTEBOOK + "".join(GALLERY_CELL.format(template=t) for t in TEMPLATES.values()))
        _, shots = shoot(page, export(notebook, tmp / "gallery.html"), tmp, "gallery")
        for name, path in zip(TEMPLATES, [s for s in shots if s is not None], strict=True):
            img = Image.open(path)
            img.resize((GALLERY_WIDTH, round(img.height * GALLERY_WIDTH / img.width)), Image.LANCZOS).save(
                MEDIA / f"template-{name}.png", optimize=True
            )

        kinds, shots = shoot(page, export(SHOWCASE, tmp / "showcase.html"), tmp, "showcase")
        parts = group_by_part(kinds)
        if len(parts) != len(PART_NAMES):
            raise SystemExit(f"expected {len(PART_NAMES)} showcase parts, found {len(parts)}: {parts}")
        for name, indexes in zip(PART_NAMES, parts):
            make_gif([shots[i] for i in indexes], MEDIA / f"{name}.gif")

        ondas = export(ONDAS, tmp / "ondas.html")
        record_player_gif(browser, ondas, MEDIA / "equations.gif", "Derivation — Step by Step", clicks=5, step_ms=3500)
        browser.close()


if __name__ == "__main__":
    main()
