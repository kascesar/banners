"""
05_animated_graph.py — AnimatedGraph element: interactive Mermaid with click-to-highlight.
Run with: uv run marimo edit test/05_animated_graph.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Section
    from banners.content import AnimatedGraph, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return AnimatedGraph, Section, Text, configure, mo


@app.cell
def _(mo):
    mo.md(r"""
    # AnimatedGraph element

    `AnimatedGraph(diagram)` renders a Mermaid `graph LR` / `graph TD` diagram
    where **nodes highlight on click**. No external JS libraries — works offline.

    ```python
    from banners.content import AnimatedGraph

    AnimatedGraph("""
    graph LR
    A[Ingest] --> B[Validate]
    B --> C[Transform]
    C --> D[Load]
    """)
    ```

    | Parameter | Default | Description |
    |-----------|---------|-------------|
    | `diagram` | — | Mermaid `graph LR` or `graph TD` source |
    | `highlight_color` | `"#ea580c"` | Color applied when a node is clicked |

    Click any node to highlight it. Click again to deselect.
    """)
    return


@app.cell
def _(mo):
    mo.md("## Linear pipeline — graph LR")
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="ETL pipeline — click nodes to highlight",
        content=AnimatedGraph("""
graph LR
A[S3 Raw] --> B[Glue Job]
B --> C[Athena Table]
C --> D[SageMaker]
D --> E[Predictions]
"""),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## With bifurcation and merge")
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Parallel transforms — click nodes to highlight",
        content=AnimatedGraph("""
graph LR
A[Ingest] --> B[Validate]
B --> C[Transform A]
B --> D[Transform B]
C --> E[Join]
D --> E
E --> F[Load]
"""),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## With cycle — retry loop")
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Retry loop — click nodes to highlight",
        content=AnimatedGraph("""
graph LR
A[Fetch] --> B[Validate]
B -->|ok| C[Process]
B -->|fail| A
C --> D[Store]
"""),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Top-down layout")
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Model lifecycle — top down",
        content=AnimatedGraph("""
graph TD
A[Data Ingestion] --> B[Feature Engineering]
B --> C[Training]
C --> D{Evaluation}
D -->|pass| E[Staging]
D -->|fail| B
E --> F[Production]
"""),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## AnimatedGraph alongside Text")
    return


@app.cell
def _(AnimatedGraph, Section, Text):
    Section(
        title="Pipeline — click to explore",
        content=[
            Text("""
**Click any node** to highlight it and trace the data path.

The pipeline has two parallel transform branches that merge
before loading into the data warehouse.
"""),
            AnimatedGraph("""
graph LR
A[Ingest] --> B[Validate]
B --> C[Transform A]
B --> D[Transform B]
C --> E[Join]
D --> E
E --> F[Load]
"""),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Custom highlight color")
    return


@app.cell
def _(AnimatedGraph, Section):
    Section(
        title="Custom highlight — green",
        content=AnimatedGraph("""
graph LR
A[Start] --> B[Process]
B --> C[End]
""", highlight_color="#22c55e"),
    ).render()
    return


if __name__ == "__main__":
    app.run()
