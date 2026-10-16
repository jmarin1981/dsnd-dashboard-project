"""Reusable functionality for SQL-backed model data."""

import pandas as pd


class ModelDataFrameMixin:
    """Convert rows returned by the SQL decorator to model-ready data."""

    model_columns = ['positive_events', 'negative_events']

    def model_dataframe(self, rows):
        return pd.DataFrame(rows, columns=self.model_columns)
