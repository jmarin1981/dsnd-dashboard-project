"""SQL query interface for employees."""

from .query_base import QueryBase
from .sql_execution import query
from .mixins import ModelDataFrameMixin


class Employee(ModelDataFrameMixin, QueryBase):
    name = 'employee'

    @query
    def names(self):
        return """
            SELECT first_name || ' ' || last_name AS full_name,
                   employee_id
            FROM employee
        """

    @query
    def username(self, id):
        return f"""
            SELECT first_name || ' ' || last_name AS full_name
            FROM employee
            WHERE employee_id = {int(id)}
        """

    @query
    def _model_rows(self, id):
        return f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {int(id)}
                """

    def model_data(self, id):
        return self.model_dataframe(self._model_rows(id))
