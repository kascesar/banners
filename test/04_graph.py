"""
04_graph.py — Graph content element: static Mermaid diagrams.
Run with: uv run marimo edit test/04_graph.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Section
    from banners.content import Graph, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return Graph, Section, Text, configure, mo


@app.cell
def _(mo):
    mo.md(r"""
    # Graph element

    `Graph(diagram)` renders a static [Mermaid](https://mermaid.js.org/) diagram.

    ```python
    from banners.content import Graph

    Graph("""
    graph LR
    A[Node A] --> B[Node B]
    B --> C[Node C]
    """)
    ```

    Supported Mermaid syntax: `graph LR`, `graph TD`, node shapes, edge labels.
    For interactive click-to-highlight, use `AnimatedGraph` instead.
    """)
    return


@app.cell
def _(mo):
    mo.md("## Linear pipeline — graph LR")
    return


@app.cell
def _(Graph, Section):
    Section(
        title="ETL pipeline",
        content=Graph("""
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
    mo.md("## Top-down — graph TD")
    return


@app.cell
def _(Graph, Section):
    Section(
        title="Model lifecycle",
        content=Graph("""
graph TD
A[Data Ingestion] --> B[Feature Engineering]
B --> C[Model Training]
C --> D{Evaluation}
D -->|pass| E[Deploy to Staging]
D -->|fail| B
E --> F[Deploy to Production]
"""),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## With bifurcation and merge")
    return


@app.cell
def _(Graph, Section):
    Section(
        title="Parallel transforms",
        content=Graph("""
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
    mo.md("## Graph alongside Text")
    return


@app.cell
def _(Graph, Section, Text):
    Section(
        title="Pipeline flow",
        content=[
            Text("""
**Five stages**, each isolated and independently deployable.

Data flows left to right through validation,
transformation, model training, and finally
lands in Redshift for reporting.
"""),
            Graph("""
graph LR
A[S3] --> B[Validate]
B --> C[Transform]
C --> D[Train]
D --> E[Redshift]
"""),
        ],
    ).render()
    return


if __name__ == "__main__":
    app.run()
