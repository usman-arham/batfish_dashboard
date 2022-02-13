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


# main_page_graph_tab_selected = dict(borderTop="2px solid #3c8dbc")

layout = dcc.Loading(
    id="loading-1",
    type="default",
    children=[
        html.Div(
            className="content-header",
            children=[
                html.H1(
                    children=[
                        "OSPF Topology",
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
                    style={"display": "none"},
                    id="ospf_graph_container",
                    children=[
                        html.Div(
                            className="col-md-12",
                            children=[
                                html.H1(
                                    children=[
                                        html.Div(
                                            className="box box-warning",
                                            children=[
                                                html.Div(
                                                    className="box-header with-border",
                                                    children=[
                                                        html.H3(
                                                            className="box-title",
                                                            children=["OSPF"],
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
                                                                            id="ospf_topology"
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
    Output("ospf_topology", "children"),
    [Input("select-snapshot-button", "value")],
    [State("batfish_host_input", "value"), State("select-network-button", "value")],
)
def set_update_tab_content(snapshot_value, host_value, network_value):
    if not snapshot_value:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    batfish.set_snapshot(snapshot_value)
    return get_ospf_graph(batfish.get_ospf_edges)


@app.callback(
    Output(component_id="ospf_graph_container", component_property="style"),
    [Input("select-snapshot-button", "value")],
)
def show_hide_element(snapshot_value):
    style = {"display": "block"}
    if not snapshot_value:
        style = {"display": "none"}
    return style
