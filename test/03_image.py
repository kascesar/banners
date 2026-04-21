"""
03_image.py — Image content element: paths, width control, grid layouts.
Run with: uv run marimo edit test/03_image.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Section
    from banners.content import Image, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return Image, Section, Text, configure, mo


@app.cell
def _(mo):
    mo.md(r"""
    # Image element

    `Image(src, width)` accepts a file path, raw bytes, or URL.
    The `width` parameter accepts any CSS value.

    ```python
    from banners.content import Image

    Image("img/logo.png")                # file path
    Image("img/logo.png", width="60%")   # with width constraint
    Image(bytes_data)                    # raw bytes
    Image("https://example.com/img.png") # URL
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md("## Single image — full width")
    return


@app.cell
def _(Image, Section):
    Section(
        title="Full-width image",
        content=Image("img/test.jpeg"),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Image with width constraint")
    return


@app.cell
def _(Image, Section):
    Section(
        title="Constrained width — 50%",
        content=Image("img/test.jpeg", width="50%"),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Image + Text — CSS grid")
    return


@app.cell
def _(Image, Section, Text):
    Section(
        title="Architecture overview",
        content=[
            Text("""
**System description**

Each stage runs independently with automatic end-to-end traceability.

- Raw data lands in S3 every 15 minutes
- Glue job normalizes and validates the schema
- Athena exposes a SQL layer for ad-hoc queries
- SageMaker pipeline retrains weekly
"""),
            Image("img/test.jpeg", width="100%"),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Two images side by side")
    return


@app.cell
def _(Image, Section):
    Section(
        title="Before and after",
        content=[
            Image("img/test.jpeg", width="100%"),
            Image("img/test.jpeg", width="100%"),
        ],
    ).render()
    return


if __name__ == "__main__":
    app.run()
