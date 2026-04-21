"""
07_plot.py — Plot content element: matplotlib and plotly figures inside slides.
Run with: uv run marimo edit test/07_plot.py
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
    from banners.content import Plot, Text
    from banners.palette import BLUE
    configure(team="Analytics Team", date="April 2026", palette=BLUE)
    return Section, Plot, Text, configure, mo, pd


@app.cell
def _(mo):
    mo.md(r"""
    # Plot element

    `Plot(fig)` wraps a matplotlib or plotly figure.
    The figure type is detected automatically:

    - **matplotlib** `Figure` → `mo.as_html(fig)`
    - **plotly** `Figure` → `mo.ui.plotly(fig)` (interactive)

    ```python
    from banners.content import Plot

    # matplotlib
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [4, 5, 6])
    Section(title="Trend", content=Plot(fig)).render()

    # plotly
    import plotly.express as px
    fig = px.bar(df, x="Model", y="AUC")
    Section(title="Comparison", content=Plot(fig)).render()
    ```
    """)
    return


@app.cell
def _(mo):
    mo.md("## matplotlib — line chart")
    return


@app.cell
def _(Plot, Section):
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.rcParams.update({"figure.facecolor": "#0f172a", "axes.facecolor": "#1e293b",
                                 "text.color": "white", "axes.labelcolor": "white",
                                 "xtick.color": "white", "ytick.color": "white",
                                 "axes.edgecolor": "#334155", "grid.color": "#334155"})

    fig_line, ax = plt.subplots(figsize=(8, 3.5))
    weeks = list(range(1, 13))
    auc_v1 = [0.78, 0.79, 0.80, 0.81, 0.81, 0.82, 0.83, 0.83, 0.84, 0.84, 0.84, 0.84]
    auc_v2 = [None]*6 + [0.86, 0.87, 0.88, 0.89, 0.90, 0.91]
    ax.plot(weeks, auc_v1, marker="o", label="Churn v1", color="#3b82f6", linewidth=2)
    ax.plot(weeks[6:], auc_v2[6:], marker="o", label="Churn v2", color="#22c55e", linewidth=2)
    ax.set_xlabel("Week")
    ax.set_ylabel("AUC")
    ax.set_title("Model performance over time", color="white")
    ax.legend(facecolor="#1e293b", edgecolor="#334155", labelcolor="white")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    Section(
        title="Model performance",
        subtitle="AUC evolution across weekly retraining cycles.",
        content=Plot(fig_line),
    ).render()
    return fig_line


@app.cell
def _(mo):
    mo.md("## matplotlib — bar chart")
    return


@app.cell
def _(Plot, Section):
    import matplotlib.pyplot as plt

    fig_bar, ax2 = plt.subplots(figsize=(7, 3.5))
    fig_bar.patch.set_facecolor("#0f172a")
    ax2.set_facecolor("#1e293b")
    models = ["Churn v1", "Churn v2", "LTV", "Propensity"]
    latencies = [42, 28, 35, 61]
    colors = ["#3b82f6", "#22c55e", "#f59e0b", "#8b5cf6"]
    bars = ax2.bar(models, latencies, color=colors, edgecolor="#334155")
    ax2.bar_label(bars, fmt="%d ms", color="white", padding=3)
    ax2.set_ylabel("Latency (ms)", color="white")
    ax2.set_title("Inference latency by model", color="white")
    ax2.tick_params(colors="white")
    for spine in ax2.spines.values():
        spine.set_edgecolor("#334155")
    ax2.set_facecolor("#1e293b")
    plt.tight_layout()

    Section(
        title="Inference latency",
        content=Plot(fig_bar),
    ).render()
    return fig_bar


@app.cell
def _(mo):
    mo.md("## matplotlib — Plot alongside Text")
    return


@app.cell
def _(Plot, Section, Text, fig_bar):
    Section(
        title="Latency analysis",
        content=[
            Text("""
**Churn v2** is the fastest model at 28 ms — a 33% improvement over v1.

**Propensity** has the highest latency (61 ms) due to its larger feature set.
All models are within the 100 ms SLA threshold.
"""),
            Plot(fig_bar),
        ],
    ).render()
    return


@app.cell
def _(mo):
    mo.md("## plotly — interactive bar chart")
    return


@app.cell
def _(Plot, Section, pd):
    import plotly.express as px

    df_px = pd.DataFrame({
        "Model":   ["Churn v1", "Churn v2", "LTV", "Propensity"],
        "AUC":     [0.84,       0.91,       0.88,  0.79],
        "Status":  ["prod",     "prod",     "staging", "dev"],
    })
    fig_px = px.bar(
        df_px, x="Model", y="AUC", color="Status",
        color_discrete_map={"prod": "#3b82f6", "staging": "#f59e0b", "dev": "#6b7280"},
        template="plotly_dark",
        title="AUC by model and status",
    )
    fig_px.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#1e293b")

    Section(
        title="Model AUC comparison",
        subtitle="Interactive — hover for details.",
        content=Plot(fig_px),
    ).render()
    return df_px, fig_px


@app.cell
def _(mo):
    mo.md("## plotly — scatter plot alongside Text")
    return


@app.cell
def _(Plot, Section, Text, pd):
    import plotly.express as px

    df_scatter = pd.DataFrame({
        "Model":        ["Churn v1", "Churn v2", "LTV", "Propensity"],
        "AUC":          [0.84,       0.91,       0.88,  0.79],
        "Latency (ms)": [42,         28,         35,    61],
        "Status":       ["prod",     "prod",     "staging", "dev"],
    })
    fig_scatter = px.scatter(
        df_scatter, x="Latency (ms)", y="AUC",
        color="Status", text="Model", size_max=18,
        color_discrete_map={"prod": "#22c55e", "staging": "#f59e0b", "dev": "#6b7280"},
        template="plotly_dark",
        title="AUC vs latency trade-off",
    )
    fig_scatter.update_traces(textposition="top center")
    fig_scatter.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#1e293b")

    Section(
        title="AUC vs latency",
        content=[
            Text("""
**Ideal zone**: high AUC + low latency (top-left).

**Churn v2** sits in the ideal zone.
**Propensity** has room for optimization.
"""),
            Plot(fig_scatter),
        ],
    ).render()
    return


if __name__ == "__main__":
    app.run()
