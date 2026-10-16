import pytest
from pathlib import Path

# Define the absolute path to the project root
project_root = Path(__file__).resolve().parent.parent

# Define a fixture for the database path
@pytest.fixture
def db_path():
    return project_root / 'python-package' / 'employee_events' / 'employee_events.db'

# Test that the database file exists
def test_db_exists(db_path):
    assert db_path.is_file()


# Leave this fixture unchanged
@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)


# Leave this fixture unchanged
@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()
    return [x[0] for x in name_tuples]

# Test that the employee table exists
def test_employee_table_exists(table_names):
    assert 'employee' in table_names

# Test that the team table exists
def test_team_table_exists(table_names):
    assert 'team' in table_names

# Test that the employee_events table exists
def test_employee_events_table_exists(table_names):
    assert 'employee_events' in table_names
