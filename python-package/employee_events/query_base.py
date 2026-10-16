
# Import dependencies needed to execute SQL queries
import pandas as pd
from .sql_execution import query


# Define a class called QueryBase
class QueryBase:

    # Class attribute
    name = ''

    # Define names method
    def names(self):
        return []

    # SQL query for event counts
    @query
    def _event_counts_rows(self, id):
        table = self.name

        return f"""
            SELECT
                event_date,
                SUM(positive_events) AS positive_events,
                SUM(negative_events) AS negative_events
            FROM {table}
            JOIN employee_events
                USING({table}_id)
            WHERE {table}.{table}_id = {int(id)}
            GROUP BY event_date
            ORDER BY event_date
        """

    # Return event counts as pandas DataFrame
    def event_counts(self, id):
        result = self._event_counts_rows(id)

        return pd.DataFrame(
            result,
            columns=[
                'event_date',
                'positive_events',
                'negative_events'
            ]
        )

    # SQL query for notes
    @query
    def _notes_rows(self, id):
        table = self.name

        return f"""
            SELECT
                note_date,
                note
            FROM {table}
            JOIN notes
                USING({table}_id)
            WHERE {table}.{table}_id = {int(id)}
            ORDER BY note_date
        """

    # Return notes as pandas DataFrame
    def notes(self, id):
        result = self._notes_rows(id)

        return pd.DataFrame(
            result,
            columns=[
                'note_date',
                'note'
            ]
        )
