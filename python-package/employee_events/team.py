
# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies for SQL execution
from .sql_execution import query
import pandas as pd
from functools import wraps


# Decorator to return SQL results as a DataFrame
def pandas_query(func):
    execute_query = query(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = execute_query(*args, **kwargs)
        return pd.DataFrame(
            result,
            columns=['positive_events', 'negative_events']
        )

    return wrapper


# Create a subclass of QueryBase called Team
class Team(QueryBase):

    # Set the class attribute name
    name = "team"

    # Define the names method
    @query
    def names(self):

        # Query 5: Select all teams
        return """
            SELECT team_name, team_id
            FROM team
        """

    # Define the username method
    @query
    def username(self, id):

        # Query 6: Select team name by ID
        return f"""
            SELECT team_name
            FROM team
            WHERE team_id = {int(id)}
        """

    # Return model data as a pandas DataFrame
    @pandas_query
    def model_data(self, id):

        return f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
