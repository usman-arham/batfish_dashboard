import dash_daq as daq
import json
import time
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from components.batfish import Batfish


layout = html.Div(
    className="wrapper",
    children=[
        dcc.Store(id="memory"),
        dcc.Location(id="url", refresh=False),
        html.Header(
            className="main-header",
            children=[
                html.A(
                    className="logo",
                    children=[
                        html.Span(
                            className="logo-mini",
                            children=[
                                html.B("A"),
                                "LT",
                            ],
                        ),
                        html.Span(
                            className="logo-lg",
                            children=[
                                html.B("Admin"),
                                "LTE",
                            ],
                        ),
                    ],
                ),
                html.Ul(
                    className="navbar navbar-static-top",
                    children=[
                        html.A(
                            className="sidebar-toggle",
                            **{"data-toggle": "push-menu"},
                            role="button",
                            children=[
                                html.Span(
                                    className="sr-only",
                                    children=[
                                        "Toggle navigation",
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="navbar-custom-menu",
                            children=[
                                html.Ul(
                                    className="nav navbar-nav",
                                    children=[
                                        html.Li(
                                            className="dropdown user user-menu",
                                            children=[
                                                html.A(
                                                    className="dropdown-toggle",
                                                    **{"data-toggle": "dropdown"},
                                                    **{"aria-expanded": "false"},
                                                    children=[
                                                        html.Img(
                                                            className="user-image",
                                                            alt="User Image",
                                                            src="assets/img/user2-160x160.jpg",
                                                        ),
                                                        html.Span(
                                                            className="hidden-xs",
                                                            children=["Muhammad Usman"],
                                                        ),
                                                    ],
                                                ),
                                                html.Ul(
                                                    className="dropdown-menu",
                                                    children=[
                                                        html.Li(
                                                            className="user-header",
                                                            children=[
                                                                html.Img(
                                                                    className="img-circle",
                                                                    alt="User Image",
                                                                    src="assets/img/user2-160x160.jpg",
                                                                ),
                                                                html.P(
                                                                    children=[
                                                                        "Muhammad Usman"
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        html.Li(
                                                            className="user-footer",
                                                            children=[
                                                                html.Div(
                                                                    className="pull-right",
                                                                    children=[
                                                                        html.A(
                                                                            className="btn btn-default btn-flat",
                                                                            children=[
                                                                                "Sign out"
                                                                            ],
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
        html.Aside(
            className="main-sidebar",
            children=[
                html.Section(
                    className="sidebar",
                    children=[
                        html.Div(
                            className="user-panel",
                            children=[
                                html.Div(
                                    className="pull-left image",
                                    children=[
                                        html.Img(
                                            className="img-circle",
                                            src="assets/img/user2-160x160.jpg",
                                            alt="User Image",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="pull-left info",
                                    children=[
                                        html.P(children=["Muhammad Usman"]),
                                        html.A(
                                            children=[
                                                html.I(
                                                    className="fa fa-circle text-success",
                                                ),
                                                " Online",
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Form(
                            className="sidebar-form",
                            children=[
                                dbc.Label("Network"),
                                dcc.Dropdown(
                                    id="select-network-button",
                                    placeholder="Select a Network",
                                    value=None,
                                ),
                                dbc.Input(
                                    className="hidden",
                                    id="batfish_host_input",
                                    value="host.docker.internal",
                                    placeholder="",
                                    persistence=True,
                                ),
                            ],
                        ),
                        html.Form(
                            className="sidebar-form",
                            children=[
                                dbc.Label("Snapshot"),
                                dcc.Dropdown(
                                    id="select-snapshot-button",
                                    placeholder="Select Snapshot",
                                    value=None,
                                ),
                            ],
                        ),
                        html.Ul(
                            className="sidebar-menu",
                            **{"data-widget": "tree"},
                            children=[
                                html.Li(
                                    className="active treeview menu-open",
                                    children=[
                                        html.A(
                                            children=[
                                                html.I(
                                                    className="fa fa-line-chart",
                                                ),
                                                html.Span(children=["Graphs"]),
                                                html.Span(
                                                    className="pull-right-container",
                                                    children=[
                                                        html.I(
                                                            className="fa fa-angle-left pull-right",
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                        html.Ul(
                                            className="treeview-menu",
                                            children=[
                                                html.Li(
                                                    className="",
                                                    children=[
                                                        dcc.Link(
                                                            href="/",
                                                            children=[
                                                                html.I(
                                                                    className="fa fa-circle-o",
                                                                ),
                                                                html.Span(
                                                                    children=["L3VPN"]
                                                                ),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Li(
                                                    children=[
                                                        dcc.Link(
                                                            href="/bgp",
                                                            children=[
                                                                html.I(
                                                                    className="fa fa-circle-o",
                                                                ),
                                                                html.Span(
                                                                    children=["BGP"]
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                                html.Li(
                                                    children=[
                                                        dcc.Link(
                                                            href="/ospf",
                                                            children=[
                                                                html.I(
                                                                    className="fa fa-circle-o",
                                                                ),
                                                                html.Span(
                                                                    children=["OSPF"]
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                                html.Li(
                                                    children=[
                                                        dcc.Link(
                                                            href="/isis",
                                                            children=[
                                                                html.I(
                                                                    className="fa fa-circle-o",
                                                                ),
                                                                html.Span(
                                                                    children=["ISIS"]
                                                                ),
                                                            ],
                                                        ),
                                                    ]
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                html.Li(
                                    children=[
                                        dcc.Link(
                                            href="/trace",
                                            children=[
                                                html.I(
                                                    className="fa fa-share",
                                                ),
                                                html.Span(children=["Trace Route"]),
                                            ],
                                        )
                                    ]
                                ),
                                html.Li(
                                    children=[
                                        dcc.Link(
                                            href="/questions",
                                            children=[
                                                html.I(
                                                    className="fa fa-question",
                                                ),
                                                html.Span(children=["Questions"]),
                                            ],
                                        )
                                    ]
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            className="content-wrapper",
            id="page-content",
            children=[],
        ),
        html.Div(
            className="main-footer",
            children=[
                html.Div(
                    className="pull-right hidden-xs",
                    children=[html.B(children=["Version "]), " 1.1.0"],
                ),
                html.Strong(
                    children=[
                        "Copyright © 2022-2023 ",
                        html.A(children=[" Cisco CMS "]),
                    ]
                ),
                " All rights reserved.",
            ],
        ),
    ],
)


# batfish network dropdown callback on page load
@app.callback(
    Output("select-network-button", "options"),
    [
        Input("batfish_host_input", "value"),
    ],
    [
        State("batfish_host_input", "value"),
    ],
)
def get_batfish_networks(n, value):
    ctx = dash.callback_context
    batfish = Batfish(value)
    options = [
        {"label": network, "value": network}
        for network in batfish.get_existing_networks
    ]

    return options


# batfish snapshot dropdown callback on select network
@app.callback(
    Output("select-snapshot-button", "options"),
    [Input("batfish_host_input", "value"), Input("select-network-button", "value")],
)
def set_batfish_snapshot(host_value, network_value):
    if not network_value:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    options = [
        {"label": snapshot, "value": snapshot}
        for snapshot in batfish.get_existing_snapshots()
    ]
    return options
