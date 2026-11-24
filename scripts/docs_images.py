"""Generate the pictures of the documentation site in `site/images/`.

Each picture comes from a short snippet of banners code (`SHOTS` for still
slides, `GIFS` for slides with an animation). The script writes a temporary
marimo notebook with one cell per snippet, exports it with the slides drawn,
screenshots each slide in headless Chromium and records the animated ones
while they advance. It also copies the README media from `media/`, which the
home page uses.

Run it with `make docs-images` (needs the dev extra and manim). It overwrites
the files in `site/images/`; commit them with the change that altered the look.
"""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGES = ROOT / "site" / "images"
WIDTH = 1200

_spec = importlib.util.spec_from_file_location("readme_images", ROOT / "scripts" / "readme_images.py")
readme_images = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(readme_images)

EARTH = "https://commons.wikimedia.org/wiki/Special:FilePath/The_Earth_seen_from_Apollo_17.jpg?width=1600"
CANYON = "https://commons.wikimedia.org/wiki/Special:FilePath/Grand_Canyon_National_Park_GRCA9857.jpg?width=1600"
PILLARS = (
    "https://commons.wikimedia.org/wiki/Special:FilePath/"
    "Pillars_of_creation_2014_HST_WFC3-UVIS_full-res_denoised.jpg?width=1600"
)

# Image name -> snippet whose last expression is a slide. The site pages show
# the same code, so a snippet reads like an example, with its own imports.
SHOTS: dict[str, str] = {
    # Get started
    "gs-cover": """
from banners import Cover
Cover(title="Churn Prediction v2", subtitle="Model migration and deployment.")
""",
    "gs-section": """
from banners import Section, Text
Section(
    title="Results",
    content=[
        Text("**Accuracy** — 91% AUC on the test set."),
        Text("**Latency** — p99 under 30 ms."),
    ],
)
""",
    "gs-closing": """
from banners import Closing
Closing(title="One framework for all models.")
""",
    # Look and feel: palettes
    **{
        f"palette-{name.lower()}": f"""
from banners import {name}, Section, Text
Section(
    title="Quarterly results",
    subtitle="palette={name}",
    content=[Text("- Revenue up **90%**\\n- Churn down to **2.1%**")],
    palette={name},
)
"""
        for name in ("ORANGE", "BLUE", "GREEN", "PURPLE", "GRAY")
    },
    "palette-custom": """
from banners import Cover, Palette
brand = Palette(primary="#a78bfa", secondary="#f472b6", dark="#1a0533")
Cover(title="Custom palette", subtitle="Three colors change the whole slide.", palette=brand)
""",
    "palette-sections": """
from banners import Palette, Section
rainbow = Palette(section_colors=("#e4572e", "#2a6fdb", "#2e9e5b"))
Section(title="Each section takes the next color", number="02", palette=rainbow)
""",
    # Look and feel: themes
    "theme-default": """
from banners import Section, Text
Section(title="Default theme", content=[Text("Century Gothic, bold titles.")])
""",
    "theme-serif": """
from banners import Section, Template, Text, Theme, configure
configure(template=Template(theme=Theme(heading_font="Georgia, serif", title_weight=600)))
Section(title="Serif titles", content=[Text("`heading_font` and `title_weight` change the titles only.")])
""",
    "theme-scale": """
from banners import Section, Template, Text, Theme, configure
configure(template=Template(theme=Theme(scale=1.25)))
Section(title="Larger text", content=[Text("`scale=1.25` makes every font 25% larger.")])
""",
    # Look and feel: layouts
    "layout-divider": """
from banners import Section
Section(title="Pipeline architecture", subtitle="How the data moves.")
""",
    "layout-columns": """
from banners import Section, Text
Section(
    title="Three findings",
    content=[
        Text("**Data** — Two sources disagree on 4% of rows."),
        Text("**Model** — Recall improves by 6 points."),
        Text("**Cost** — Training time drops by half."),
    ],
)
""",
    "layout-visual-text": """
from banners import Graph, Section, Text
Section(
    title="Pipeline",
    content=[
        Graph("graph LR\\n  A[Ingest] --> B[Transform] --> C[Serve]"),
        Text("Each stage is versioned and monitored on its own."),
    ],
)
""",
    "layout-photo": f"""
from banners import Section, Text
Section(
    title="Field work",
    content=[Text("A photo fills the left half; the content sits on the right.")],
    image="{CANYON}",
)
""",
    # Look and feel: backgrounds
    "bg-color": """
from banners import Background, Section, Text
Section(title="Solid color", content=[Text("The text turns white on a dark color.")],
        background=Background.color("#0f172a"))
""",
    "bg-gradient": """
from banners import Background, Section, Text
Section(title="Gradient", content=[Text("Two or three stops at any angle.")],
        background=Background.gradient("#1e3a5f", "#6d28d9", angle=135))
""",
    "bg-image": f"""
from banners import Background, Section, Text
Section(title="Photo", content=[Text("A dark overlay keeps the text readable.")],
        background=Background.image("{PILLARS}"))
""",
    # Slides
    "cover-basic": """
from banners import Cover, configure
configure(team="Analytics Team", date="2026")
Cover(title="Churn Prediction v2", subtitle="Model migration and deployment.")
""",
    "cover-photo": f"""
from banners import Cover
Cover(title="Earth observation", subtitle="Ten years of satellite data.", image="{EARTH}")
""",
    "intro-basic": """
from banners import Intro, Text
Intro(
    title="Why we're here",
    tag="Context",
    summary="Models ran on servers with a confirmed shutdown date.",
    content=[Text("**Risk** — No fallback."), Text("**Process** — Manual and undocumented.")],
    footer="Source: platform team, 2026.",
)
""",
    "section-divider-icon": """
from banners import Section, Template, configure
configure(template=Template(divider_icon="flow"))
Section(title="Pipeline architecture", subtitle="How the data moves.")
""",
    "closing-basic": """
from banners import Closing
Closing(title="One framework for all models.", subtitle="Questions welcome.")
""",
    "closing-stats": """
from banners import Closing
Closing(
    title="One framework for all models.",
    stats=[
        ("100%", "Traceability", "End to end"),
        ("3×", "Faster releases", "Since January"),
        ("1", "Shared codebase", "Everyone contributes"),
    ],
)
""",
    # Content
    "content-text": """
from banners import Section, Text
Section(
    title="Text",
    content=[
        Text("**Bold**, *italic* and `code`.\\n\\n- Lists\\n- With items"),
        Text("Formulas with LaTeX:\\n\\n$$E = mc^2$$"),
    ],
)
""",
    "content-image": f"""
from banners import Image, Section, Text
Section(
    title="Image",
    content=[Image("{EARTH}"), Text("A path, a URL or raw bytes.")],
)
""",
    "content-table": """
import pandas as pd
from banners import Section, Table
df = pd.DataFrame({"Model": ["XGBoost", "LightGBM", "Logistic"], "AUC": [0.91, 0.89, 0.84]})
Section(title="Table", content=[Table(df)])
""",
    "content-plot": """
import matplotlib.pyplot as plt
from banners import Plot, Section, Text
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot([1, 2, 3, 4], [3.1, 3.8, 4.6, 5.9], marker="o", label="Revenue")
ax.plot([1, 2, 3, 4], [2.0, 2.4, 2.5, 3.1], marker="o", label="Cost")
ax.legend()
Section(title="Plot", content=[Plot(fig), Text("The lines take the palette colors.")])
""",
    "content-plot-blue": """
import matplotlib.pyplot as plt
from banners import BLUE, Plot, Section, Text
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot([1, 2, 3, 4], [3.1, 3.8, 4.6, 5.9], marker="o", label="Revenue")
ax.plot([1, 2, 3, 4], [2.0, 2.4, 2.5, 3.1], marker="o", label="Cost")
ax.legend()
Section(title="Plot", content=[Plot(fig), Text("Same figure, BLUE palette.")], palette=BLUE)
""",
    "content-graph": """
from banners import Graph, Section
Section(
    title="Graph",
    content=[Graph("graph LR\\n  A[Raw data] --> B[Validate]\\n  B --> C[Train]\\n  B --> D[Report]")],
)
""",
    "org-template": """
from banners import Cover, Palette, Template, configure, icon
corp = Template(
    palette=Palette(primary="#0f766e", secondary="#f59e0b", dark="#0b2e2b"),
    logo_on_dark=icon("building", color="#ffffff"),
    mark=icon("building", color="#0f766e"),
)
configure(template=corp, team="Data Office", date="2026")
Cover(title="Quarterly review", subtitle="Your logo, your colors.")
""",
}

# Image name -> (snippet, slide title, clicks, milliseconds per step).
GIFS: dict[str, tuple[str, str, int, int]] = {
    "content-flow": ("""
from banners import FlowAnimation, Section
Section(
    title="FlowAnimation",
    content=[FlowAnimation([
        {"name": "S3", "detail": "raw files"},
        {"name": "Glue", "detail": "ETL job"},
        {"name": "Athena", "detail": "SQL"},
        {"name": "Dashboard", "detail": "BI"},
    ])],
)
""", "FlowAnimation", 3, 1200),
    "content-manim": ("""
from banners import ORANGE, Manim, Section
from manim import Circle, Create, Scene, Square, Transform

class ShapeScene(Scene):
    def construct(self):
        self.next_section("circle")
        shape = Circle(color=ORANGE.primary, fill_opacity=0.2)
        self.play(Create(shape), run_time=0.4)
        self.next_section("square")
        self.play(Transform(shape, Square(color=ORANGE.secondary, fill_opacity=0.2)), run_time=0.4)

Section(title="Manim", content=[Manim(ShapeScene, interactive=True)])
""", "Manim", 1, 1600),
}

SETUP = '''
import marimo

app = marimo.App(width="full")


@app.cell
def _():
    from banners import configure

    def reset_config():
        configure(team="Analytics Team", date="2026", template=None, palette=None, theme=None, background=None)

    return (reset_config,)
'''


def notebook_source(shots: dict[str, str]) -> str:
    """Write a marimo notebook with one cell per snippet.

    Each cell resets the configuration first, so a snippet that calls
    `configure()` does not change the slides of the next cells.

    Args:
        shots: Image name -> snippet whose last expression is a slide.

    Returns:
        The source of the notebook.
    """
    cells = []
    for snippet in shots.values():
        body = textwrap.indent(_returning(snippet), "        ")
        cells.append(
            "\n\n@app.cell\ndef _(reset_config):\n    def _shot():\n        reset_config()\n"
            f"{body}\n"
            "    _slide = _shot()\n    _slide\n    return\n"
        )
    return SETUP + "".join(cells)


def _returning(snippet: str) -> str:
    """Turn the last expression of a snippet into a `return` statement.

    Args:
        snippet: Code whose last statement is an expression.

    Returns:
        The same code, returning that expression.
    """
    import ast

    code = textwrap.dedent(snippet).strip()
    last = ast.parse(code).body[-1]
    lines = code.splitlines()
    start = last.lineno - 1
    lines[start] = "return " + lines[start]
    return "\n".join(lines)


def main() -> None:
    """Write every picture of the site to `site/images/`."""
    from PIL import Image
    from playwright.sync_api import sync_playwright

    IMAGES.mkdir(parents=True, exist_ok=True)
    for path in (ROOT / "media").iterdir():
        shutil.copy(path, IMAGES / path.name)

    snippets = dict(SHOTS) | {name: code for name, (code, *_rest) in GIFS.items()}
    with tempfile.TemporaryDirectory() as tmp, sync_playwright() as p:
        tmp = Path(tmp)
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1700, "height": 1100}, device_scale_factor=2)
        notebook = tmp / "shots.py"
        notebook.write_text(notebook_source(snippets))
        html = readme_images.export(notebook, tmp / "shots.html")
        _, shots = readme_images.shoot(page, html, tmp, "shot")
        pictures = [s for s in shots if s is not None]
        if len(pictures) != len(snippets):
            raise SystemExit(f"expected {len(snippets)} slides, found {len(pictures)}")
        for name, path in zip(snippets, pictures):
            if name in SHOTS:
                img = Image.open(path)
                img.resize((WIDTH, round(img.height * WIDTH / img.width)), Image.LANCZOS).save(
                    IMAGES / f"{name}.png", optimize=True
                )
        for name, (_code, title, clicks, step_ms) in GIFS.items():
            readme_images.record_player_gif(browser, html, IMAGES / f"{name}.gif", title, clicks, step_ms)
        browser.close()


if __name__ == "__main__":
    main()
