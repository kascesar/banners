"""
09_flow_animation.py — FlowAnimation element: animated pipeline diagrams.
Run with: uv run marimo edit test/09_flow_animation.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    from banners import configure
    from banners.slides import Section
    from banners.content import FlowAnimation, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return FlowAnimation, Section, Text, mo


@app.cell
def _(mo):
    mo.md(r"""
    # FlowAnimation element

    `FlowAnimation` builds an animated step-by-step pipeline diagram.
    Each node appears on click, with arrows connecting to the previous ones.

    Requires the optional dependency:
    ```bash
    uv pip install "banners[manim]"
    ```

    ## Three input formats

    ### 1. Flat list
    ```python
    FlowAnimation(["S3", "Glue", "Athena"])
    ```

    ### 2. Nested list — layered topology
    ```python
    FlowAnimation([
        ["Ingest"],
        ["Transform A", "Transform B"],
        ["Load"],
    ])
    ```

    ### 3. Explicit graph — arbitrary connections
    ```python
    FlowAnimation(
        nodes=["Ingest A", "Ingest B", "Transform", "Load"],
        edges=[
            ("Ingest A", "Transform"),
            ("Ingest B", "Transform"),
            ("Transform", "Load"),
        ],
    )
    ```

    | Parameter | Default | Description |
    |-----------|---------|-------------|
    | `direction` | `"LR"` / `"TD"` | Flow direction — left-right or top-down |
    | `quality` | `"low"` | Render quality: `"low"`, `"medium"`, `"high"` |
    | `width` | `"100%"` | Player width — any CSS value |

    Default direction: `"LR"` for flat lists and graphs, `"TD"` for nested lists.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Flat list — left to right (default)
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="ETL pipeline",
        subtitle="Click to reveal each stage.",
        content=FlowAnimation(["S3", "Glue", "Athena", "SageMaker", "Redshift"]),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Flat list — top down
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="ETL pipeline — top down",
        content=FlowAnimation(
            ["S3", "Glue", "Athena", "SageMaker", "Redshift"],
            direction="TD",
        ),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## With detail text
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="Pipeline with details",
        content=FlowAnimation([
            {"name": "S3",       "detail": "raw parquet / CSV"},
            {"name": "Glue",     "detail": "spark ETL job"},
            {"name": "Athena",   "detail": "SQL query layer"},
            {"name": "Redshift", "detail": "data warehouse"},
        ]),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Nested list — layered topology (TD)
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="Multi-layer pipeline",
        content=FlowAnimation([
            ["Ingest"],
            [
                {"name": "Transform A", "detail": "feature engineering"},
                {"name": "Transform B", "detail": "outlier filter"},
            ],
            ["Join"],
            [
                {"name": "Train",  "detail": "SageMaker"},
                {"name": "Serve",  "detail": "endpoint"},
            ],
        ]),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Nested list — LR direction
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="Multi-layer pipeline — LR",
        content=FlowAnimation([
            ["Ingest"],
            [
                {"name": "Transform A", "detail": "feature engineering"},
                {"name": "Transform B", "detail": "outlier filter"},
            ],
            ["Join"],
            [
                {"name": "Train",  "detail": "SageMaker"},
                {"name": "Serve",  "detail": "endpoint"},
            ],
        ], direction="LR"),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Explicit graph — parallel branches
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="Parallel ingestion paths",
        subtitle="Two independent sources merge into a single model.",
        content=FlowAnimation(
            nodes=[
                {"name": "Ingest A",   "detail": "S3 bucket"},
                {"name": "Ingest B",   "detail": "Kafka stream"},
                {"name": "Clean A"},
                {"name": "Clean B"},
                {"name": "Validate"},
                {"name": "Train",      "detail": "SageMaker"},
                {"name": "Deploy",     "detail": "REST endpoint"},
            ],
            edges=[
                ("Ingest A",  "Clean A"),
                ("Ingest B",  "Clean B"),
                ("Clean A",   "Train"),
                ("Clean B",   "Validate"),
                ("Validate",  "Train"),
                ("Train",     "Deploy"),
            ],
        ),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Explicit graph — top down
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="Parallel branches — TD",
        content=FlowAnimation(
            nodes=[
                "Ingest A",
                {"name": "Ingest B", "detail": "Kafka"},
                {"name": "Validate"},
                {"name": "Train", "detail": "SageMaker"},
            ],
            edges=[
                ("Ingest A", "Validate"),
                ("Ingest B", "Validate"),
                ("Validate", "Train"),
            ],
            direction="TD",
        ),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## FlowAnimation alongside Text
    """)
    return


@app.cell
def _(FlowAnimation, Section, Text):
    Section(
        title="Pipeline overview",
        content=[
            Text("""
    **Three ingestion sources** feed into a shared validation layer.

    Each source is cleaned independently before joining in the
    training stage, allowing partial failures without blocking the pipeline.
    """),
            FlowAnimation(
                nodes=["Source A", "Source B", "Source C",
                       "Validate", "Train", "Deploy"],
                edges=[
                    ("Source A", "Validate"),
                    ("Source B", "Validate"),
                    ("Source C", "Validate"),
                    ("Validate", "Train"),
                    ("Train",    "Deploy"),
                ],
                width="600px",
            ),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md("""
    ## Width control
    """)
    return


@app.cell
def _(FlowAnimation, Section):
    Section(
        title="Width = 700px",
        content=FlowAnimation(
            ["S3", "Glue", "Athena", "Redshift"],
            width="700px",
        ),
    ).render()
    return


if __name__ == "__main__":
    app.run()
