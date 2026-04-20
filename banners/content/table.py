"""Table content element — wraps a pandas DataFrame."""

import marimo as mo


class Table:
    """Renders a pandas DataFrame as an HTML table inside a slide.

    Args:
        df: A pandas DataFrame to display.

    Example:
        ```python
        import pandas as pd
        from banners.content import Table

        df = pd.DataFrame({"Model": ["A", "B"], "AUC": [0.91, 0.87]})
        Table(df)
        ```
    """

    def __init__(self, df) -> None:
        self.df = df

    def render(self) -> mo.Html:
        """Render the DataFrame as a marimo HTML component.

        Returns:
            A `mo.Html` component ready to display in a marimo cell.
        """
        return mo.as_html(self.df)
