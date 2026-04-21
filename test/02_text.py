"""
02_text.py — Text content element: markdown, layouts and content_kind styles.
Run with: uv run marimo edit test/02_text.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Section
    from banners.content import Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return Section, Text, configure, mo


@app.cell
def _(mo):
    mo.md(r"""
    # Text element

    `Text(body)` wraps a markdown string. It supports the full CommonMark spec:
    bold, italics, lists, tables, code blocks, and more.

    ```python
    from banners.content import Text

    Text("**Bold**, *italic*, `code`")
    Text("- Item 1\n- Item 2")
    ```

    `Text` objects are passed in `content=` lists alongside other elements.
    When a slide receives a list of only `Text` items, it applies `content_kind`
    to all of them as styled boxes.
    """)
    return


@app.cell
def _(mo):
    mo.md("## Single Text — full width")
    return


@app.cell
def _(Section, Text):
    Section(
        title="Single text item",
        subtitle="Rendered full-width when passed alone.",
        content=Text("""
**banners** is a marimo presentation library.

Each slide calls `.render()` which returns a marimo component displayed
directly in the notebook cell. No server required — everything runs locally.

Features:
- Auto-numbered sections
- Global palette system
- CSS grid layout for multiple content items
"""),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Multiple Text items — CSS grid")
    return


@app.cell
def _(Section, Text):
    Section(
        title="Three columns",
        subtitle="Each Text becomes one equal-width column.",
        content=[
            Text("**Ingest** — Raw data arrives from S3 and Kafka streams every 15 minutes."),
            Text("**Transform** — Spark job normalizes schema and fills missing values."),
            Text("**Load** — Final dataset written to Athena and Redshift for queries."),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## `content_kind` — styled boxes")
    return


@app.cell
def _(Section, Text):
    Section(
        title="content_kind = neutral",
        content=[
            Text("**Point A** — Neutral box, default style."),
            Text("**Point B** — Same style as A."),
            Text("**Point C** — All items share the same kind."),
        ],
        content_kind="neutral",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="content_kind = warn",
        content=[
            Text("**Risk 1** — Models stop producing predictions."),
            Text("**Risk 2** — No record of which version is active."),
            Text("**Risk 3** — Manual and undocumented process."),
        ],
        content_kind="warn",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="content_kind = success",
        content=[
            Text("**Result 1** — Deployment time reduced from days to minutes."),
            Text("**Result 2** — Full end-to-end traceability."),
            Text("**Result 3** — Single parameterized framework."),
        ],
        content_kind="success",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="content_kind = info",
        content=[
            Text("**Note 1** — Any model can be deployed with one command."),
            Text("**Note 2** — Documentation is generated automatically."),
        ],
        content_kind="info",
    ).render()
    return


@app.cell
def _(Section, Text):
    Section(
        title="content_kind = danger",
        content=[
            Text("**Critical 1** — Servers shut down on March 15."),
            Text("**Critical 2** — Zero fallback strategy in place."),
        ],
        content_kind="danger",
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Markdown table inside Text")
    return


@app.cell
def _(Section, Text):
    Section(
        title="Before vs after",
        content=Text("""
| Before | After |
|--------|-------|
| Hardcoded per model  | Parameterized for any model |
| n models = n projects | n models = 1 framework |
| Manual deploy | Single command |
| No versioning | Full traceability |
"""),
    ).render()
    return


if __name__ == "__main__":
    app.run()
