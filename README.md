# Employee Performance and Recruitment Risk Dashboard

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

On Windows PowerShell activate with `.venv\Scripts\Activate.ps1` instead.
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
