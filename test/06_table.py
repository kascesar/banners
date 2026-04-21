"""
06_table.py — Table content element: pandas DataFrames inside slides.
Run with: uv run marimo edit test/06_table.py
"""

import marimo

__generated_with = "0.23.1"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    from banners import configure
    from banners.slides import Section
    from banners.content import Table, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return Section, Table, Text, configure, mo, pd


@app.cell
def _(mo):
    mo.md(r"""
    # Table element

    `Table(df)` wraps a pandas DataFrame and renders it as an interactive table
    inside a slide.

    ```python
    import pandas as pd
    from banners.content import Table

    df = pd.DataFrame({
        "Model": ["Churn v1", "Churn v2", "LTV"],
        "AUC": [0.84, 0.91, 0.88],
        "Latency (ms)": [42, 28, 35],
    })

    Section(title="Model comparison", content=Table(df)).render()
    ```

    The table is sortable and searchable — powered by `mo.as_html(df)`.
    """)
    return


@app.cell
def _(mo):
    mo.md("## Basic DataFrame — full width")
    return


@app.cell
def _(Section, Table, pd):
    df_models = pd.DataFrame({
        "Model":        ["Churn v1", "Churn v2", "LTV",    "Propensity"],
        "AUC":          [0.84,       0.91,       0.88,     0.79],
        "Latency (ms)": [42,         28,         35,       61],
        "Status":       ["prod",     "prod",     "staging","dev"],
        "Owner":        ["team-a",   "team-a",   "team-b", "team-b"],
    })
    Section(
        title="Model registry",
        subtitle="All models tracked in the platform.",
        content=Table(df_models),
    ).render()
    return df_models


@app.cell
def _(mo):
    mo.md("## Table alongside Text")
    return


@app.cell
def _(Section, Table, Text, df_models):
    Section(
        title="Results",
        content=[
            Text("""
**Summary**

- 2 models in production
- 1 in staging, 1 in development
- Average AUC across prod models: **0.875**
- Churn v2 achieved a 16% latency improvement over v1
"""),
            Table(df_models),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Comparison table")
    return


@app.cell
def _(Section, Table, pd):
    df_compare = pd.DataFrame({
        "Approach":     ["Old (manual)", "New (banners)"],
        "Deploy time":  ["2-3 days",     "< 5 min"],
        "Versioning":   ["None",         "Automatic"],
        "Rollback":     ["Manual",       "One command"],
        "Docs":         ["None",         "Auto-generated"],
        "Traceability": ["No",           "End-to-end"],
    })
    Section(
        title="Before vs after",
        subtitle="Impact of the new deployment framework.",
        content=Table(df_compare),
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## Metrics table with styled text")
    return


@app.cell
def _(Section, Table, Text, pd):
    df_kpis = pd.DataFrame({
        "KPI":          ["Deployment frequency", "Lead time", "MTTR",     "Change failure rate"],
        "Before":       ["1x / quarter",         "3 days",    "2 days",   "25%"],
        "After":        ["Daily",                "4 hours",   "30 min",   "5%"],
        "Delta":        ["+12x",                 "-94%",      "-94%",     "-80%"],
    })
    Section(
        title="DORA metrics",
        content=[
            Text("""
**Four key DevOps metrics** measuring delivery performance
after migrating to the banners deployment framework.
"""),
            Table(df_kpis),
        ],
    ).render()
    return


if __name__ == "__main__":
    app.run()
