from pathlib import Path
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
