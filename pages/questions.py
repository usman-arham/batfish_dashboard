import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app

layout = html.Div(
    [
        html.H3("Page 2"),
        html.Div(id="page-2-display-value"),
        dcc.Link("Go to Page 1", href="/page2"),
    ]
)
