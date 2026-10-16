
from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Database path
db_path = Path(__file__).resolve().parent / 'employee_events.db'


# SQL execution decorator
def query(func):
    """
    Executes a SQL query and returns a list of tuples.
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)

        connection = connect(db_path)

        try:
            cursor = connection.cursor()
            result = cursor.execute(query_string).fetchall()
            return result
        finally:
            connection.close()

    return run_query

