import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from components.batfish import Batfish
from components.functions import get_layer3_graph
from components.functions import get_ospf_graph
from components.functions import get_bgp_graph

layout = dcc.Loading(
    id="loading-1",
    type="default",
    children=[
        html.Div(
            className="content-header",
            children=[
                html.H1(
                    children=[
                        "L3VPN Topology",
                        html.Small(
                            className="content-header",
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            className="content",
            children=[
                html.Div(
                    className="row",
                    id="l3_graph_container",
                    style={"display": "none"},
                    children=[
                        html.Div(
                            className="col-md-12",
                            children=[
                                html.H1(
                                    children=[
                                        html.Div(
                                            className="box box-success",
                                            children=[
                                                html.Div(
                                                    className="box-header with-border",
                                                    children=[
                                                        html.H3(
                                                            className="box-title",
                                                            children=["Topology"],
                                                        ),
                                                        html.Div(
                                                            className="box-tools pull-right",
                                                            children=[
                                                                html.H3(
                                                                    className="box-title",
                                                                )
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="box-body",
                                                    children=[
                                                        html.Div(
                                                            className="row",
                                                            children=[
                                                                html.Div(
                                                                    className="col-md-12",
                                                                    children=[
                                                                        html.Div(
                                                                            className="text-center",
                                                                            children=[
                                                                                html.Strong(
                                                                                    style={
                                                                                        "fontSize": "14px",
                                                                                    },
                                                                                    children=[],
                                                                                )
                                                                            ],
                                                                        ),
                                                                        html.Div(
                                                                            id="l3_topology"
                                                                        ),
                                                                    ],
                                                                ),
                                                            ],
                                                        )
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


@app.callback(
    Output("l3_topology", "children"),
    [Input("select-snapshot-button", "value")],
    [State("batfish_host_input", "value"), State("select-network-button", "value")],
)
def set_update_tab_content(snapshot_value, host_value, network_value):
    if not snapshot_value:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    batfish.set_snapshot(snapshot_value)
    return get_layer3_graph(batfish.get_layer3_edges)


@app.callback(
    Output(component_id="l3_graph_container", component_property="style"),
    [Input("select-snapshot-button", "value")],
)
def show_hide_element(snapshot_value):
    style = {"display": "block"}
    if not snapshot_value:
        style = {"display": "none"}
    return style
