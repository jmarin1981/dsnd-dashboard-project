from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent
# Run this script from the root of the repository; no changes to unrelated paths.
if not (root / 'python-package' / 'employee_events' / 'employee_events.db').is_file():
    raise SystemExit('ERROR: coloca este script en la raíz dsnd-dashboard-project antes de ejecutarlo.')

pkg = root / 'python-package'
source = pkg / 'employee_events'

(pkg / 'setup.py').write_text('''from pathlib import Path
from setuptools import setup, find_packages

cwd = Path(__file__).resolve().parent
requirements = [
    line.strip()
    for line in (cwd / 'employee_events' / 'requirements.txt').read_text().splitlines()
    if line.strip() and not line.startswith('#')
]

setup_args = dict(
    name='employee_events',
    version='0.0',
    description='SQL Query API',
    packages=find_packages(),
    package_data={'employee_events': ['employee_events.db', 'requirements.txt']},
    include_package_data=True,
    install_requires=requirements,
)

if __name__ == '__main__':
    setup(**setup_args)
''', encoding='utf-8')

(source / 'mixins.py').write_text('''"""Reusable functionality for SQL-backed model data."""

import pandas as pd


class ModelDataFrameMixin:
    """Convert rows returned by the SQL decorator to model-ready data."""

    model_columns = ['positive_events', 'negative_events']

    def model_dataframe(self, rows):
        return pd.DataFrame(rows, columns=self.model_columns)
''', encoding='utf-8')

(source / 'employee.py').write_text('''"""SQL query interface for employees."""

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
''', encoding='utf-8')

(source / 'team.py').write_text('''"""SQL query interface for teams."""

from .query_base import QueryBase
from .sql_execution import query
from .mixins import ModelDataFrameMixin


class Team(ModelDataFrameMixin, QueryBase):
    name = 'team'

    @query
    def names(self):
        return """
            SELECT team_name, team_id
            FROM team
        """

    @query
    def username(self, id):
        return f"""
            SELECT team_name
            FROM team
            WHERE team_id = {int(id)}
        """

    @query
    def _model_rows(self, id):
        return f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {int(id)}
                    GROUP BY employee_id
                   )
                """

    def model_data(self, id):
        return self.model_dataframe(self._model_rows(id))
''', encoding='utf-8')

(root / 'README.md').write_text('''# Employee Performance and Recruitment Risk Dashboard

Final project for Udacity's Software Engineering for Data Scientists course.
The application lets managers select an employee or team, explore cumulative
positive and negative performance events, review dated notes, and display
recruitment risk estimated using a pre-trained logistic regression model.

## Repository contents

- `python-package/employee_events/`: SQLite-backed Python API. `QueryBase` contains
  shared queries, `Employee` and `Team` contain entity-specific queries, and
  `ModelDataFrameMixin` converts SQL results to model-ready Pandas DataFrames.
- `python-package/employee_events/employee_events.db`: sample SQLite database.
- `python-package/dist/employee_events-0.0.tar.gz`: source distribution.
- `assets/model.pkl`: pre-trained scikit-learn model supplied with the project.
- `report/dashboard.py`: interactive FastHTML dashboard and routes.
- `report/utils.py`: model loading helper.
- `tests/test_employee_events.py`: automated database tests.
- `.github/workflows/`: GitHub Actions for testing and lint checks.

## Setup

Requires Python 3.10 or later. From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell activate with `.venv\\Scripts\\Activate.ps1` instead.
`requirements.txt` installs the `employee_events` package in editable mode.

## Run the dashboard

Run from the `report/` directory, so its component imports resolve:

```bash
cd report
python dashboard.py
```

Open the URL shown by FastHTML (typically `http://localhost:5001`). In the
Udacity workspace open the forwarded port 5001 from the Ports tab.
The included dashboard contains compatibility adjustments for the course's
FastHTML 0.8.0 environment; run with the pinned versions in `requirements.txt`.

## Run tests

From the repository root:

```bash
python -m pytest tests/test_employee_events.py -v
```

The test module includes a path fixture and four tests that verify the database
and required tables exist. GitHub Actions runs these checks on pushes to `main`.

## Build the distributable package

From the repository root:

```bash
cd python-package
python setup.py sdist
```

Expected output: `python-package/dist/employee_events-0.0.tar.gz`.
This source distribution includes the SQLite database and package requirements.

## Data and model

The demonstration database contains `employee`, `team`, `employee_events`, and
`notes` tables. The model estimates recruitment risk from positive and negative
event totals. This is a course demonstration, not a validated personnel decision
system. Avoid using the predictions as the sole basis of employment decisions.

## Source and attribution

Based on the starter project from
[Udacity's dsnd-dashboard-project](https://github.com/udacity/dsnd-dashboard-project).
Project implementations were developed with AI-assisted coding support.
''', encoding='utf-8')

print('Archivos actualizados: setup.py, mixins.py, employee.py, team.py, README.md')
subprocess.run([sys.executable, 'setup.py', 'sdist'], cwd=pkg, check=True)
artifact = pkg / 'dist' / 'employee_events-0.0.tar.gz'
if not artifact.is_file():
    raise SystemExit('ERROR: no se encontró el paquete distribuible')
print(f'Paquete creado: {artifact} ({artifact.stat().st_size} bytes)')
subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_employee_events.py', '-q'], cwd=root, check=True)
print('Revisión de datos y paquete:')
cmd = "from employee_events.employee import Employee; from employee_events.team import Team; import pandas as pd; assert isinstance(Employee().model_data(1),pd.DataFrame); assert isinstance(Team().model_data(1),pd.DataFrame); print('Model data Employee y Team: OK')"
subprocess.run([sys.executable, '-c', cmd], cwd=root, check=True)
print('LISTO. Revisa cambios y sube el .tar.gz con git add -f.')
