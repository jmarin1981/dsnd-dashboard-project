
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


# Define a subclass of QueryBase called Employee
class Employee(QueryBase):

    # Set the class attribute name
    name = "employee"

    # Define the names method
    @query
    def names(self):

        # Query 3: Select all employee names and IDs
        return """
            SELECT
                first_name || ' ' || last_name AS full_name,
                employee_id
            FROM employee
        """

    # Define the username method
    @query
    def username(self, id):

        # Query 4: Select employee name by ID
        return f"""
            SELECT
                first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {int(id)}
        """

    # Return model data as a pandas DataFrame
    @pandas_query
    def model_data(self, id):

        return f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """
