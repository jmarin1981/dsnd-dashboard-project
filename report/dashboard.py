import builtins
from typing import Any
builtins.Any = Any

from fasthtml.common import *

# Temporary compatibility fix for FastHTML 0.8.0 and fastcore.
import fasthtml.core as fh_core
from fastcore.xml import to_xml as original_to_xml

fh_core.to_xml = lambda resp, indent=True: original_to_xml(resp, indent=indent)

import matplotlib.pyplot as plt
from employee_events.query_base import QueryBase
from employee_events.employee import Employee
from employee_events.team import Team
from utils import load_model
from base_components import Dropdown, BaseComponent, Radio, MatplotlibViz, DataTable
from combined_components import FormGroup, CombinedComponent

# The browser accesses Udacity's workspace through this reverse-proxy path.
# The server's FastHTML routes below remain unprefixed.
PUBLIC_PREFIX = '/proxy/5001'

class ReportDropdown(Dropdown):
    def build_component(self, entity_id, model):
        self.label = model.name
        return super().build_component(entity_id, model)

    def component_data(self, entity_id, model):
        return model.names()


class Header(BaseComponent):
    def build_component(self, entity_id, model):
        return H1(model.name.capitalize())


class LineChart(MatplotlibViz):
    def visualization(self, entity_id, model):
        data = model.event_counts(entity_id)
        data = data.fillna(0)
        data = data.set_index('event_date')
        data = data.sort_index()
        data = data.cumsum()
        data.columns = ['Positive', 'Negative']
        fig, ax = plt.subplots()
        data.plot(ax=ax)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        ax.set_title('Cumulative Employee Events')
        ax.set_xlabel('Date')
        ax.set_ylabel('Event Count')
        fig.autofmt_xdate()


class BarChart(MatplotlibViz):
    predictor = load_model()

    def visualization(self, entity_id, model):
        data = model.model_data(entity_id)
        predictions = self.predictor.predict_proba(data)
        probabilities = predictions[:, 1]
        if model.name == 'team':
            pred = probabilities.mean()
        else:
            pred = probabilities[0]
        fig, ax = plt.subplots()
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')


class Visualizations(CombinedComponent):
    children = [LineChart(), BarChart()]
    outer_div_type = Div(cls='grid')


class NotesTable(DataTable):
    def component_data(self, entity_id, model):
        return model.notes(entity_id)


class DashboardFilters(FormGroup):
    id = 'top-filters'
    action = f'{PUBLIC_PREFIX}/update_data'
    method = 'POST'
    children = [
        Radio(
            values=['Employee', 'Team'],
            name='profile_type',
            hx_get=f'{PUBLIC_PREFIX}/update_dropdown',
            hx_target='#selector'
        ),
        ReportDropdown(id='selector', name='user-selection')
    ]


class Report(CombinedComponent):
    children = [Header(), DashboardFilters(), Visualizations(), NotesTable()]


app, rt = fast_app(hdrs=(Link(rel='stylesheet', href=f'{PUBLIC_PREFIX}/assets/report.css'),))
report = Report()


@rt('/')
def index():
    return report(1, Employee())


@rt('/employee/{id}')
def employee(id: str):
    valid_ids = {str(value) for _, value in Employee().names()}
    if id not in valid_ids:
        return RedirectResponse('../employee/1', status_code=303)
    return report(id, Employee())


@rt('/team/{id}')
def team(id: str):
    valid_ids = {str(value) for _, value in Team().names()}
    if id not in valid_ids:
        return RedirectResponse('../team/1', status_code=303)
    return report(id, Team())


@app.get('/update_dropdown')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    profile_type = r.query_params.get('profile_type')
    if profile_type == 'Team':
        return dropdown(None, Team())
    if profile_type == 'Employee':
        return dropdown(None, Employee())
    return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data.get('profile_type', 'Employee')
    entity_id = data.get('user-selection', '1')
    # Avoid mixing an employee ID with the team selection.
    if profile_type == 'Team':
        valid_ids = [str(value) for _, value in Team().names()]
        if entity_id not in valid_ids:
            entity_id = valid_ids[0]
        return RedirectResponse(f'team/{entity_id}', status_code=303)

    valid_ids = [str(value) for _, value in Employee().names()]
    if entity_id not in valid_ids:
        entity_id = valid_ids[0]
    return RedirectResponse(f'employee/{entity_id}', status_code=303)


serve()
