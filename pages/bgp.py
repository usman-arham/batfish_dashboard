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
                        "BGP Topology",
                        html.Small(
                            className="content-header",
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            className="content",
            id="nonetworksnapshotalert",
            children=[
                html.Div(
                    className="alert alert-info alert-dismissible",
                    children=[
                        html.Button(
                            className="close",
                            **{"data-dismiss": "alert"},
                            **{"aria-hidden": "true"},
                            children=["×"]
                        ),
                        html.H4(
                            className="",
                            children=[
                                html.I(className="icon fa fa-info", children=[]),
                                "Info!",
                            ],
                        ),
                        "Select Network and Snapshot!!!",
                    ],
                )
            ],
        ),
        html.Div(
            className="content",
            id="contentid",
            style={"display": "none"},
            children=[
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            className="col-md-4 col-sm-6 col-xs-12",
                            children=[
                                html.Div(
                                    className="info-box",
                                    children=[
                                        html.Span(
                                            className="info-box-icon bg-green",
                                            children=[
                                                html.I(
                                                    className="fa fa-network-wired",
                                                    children=[],
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="info-box-content",
                                            children=[
                                                html.Span(
                                                    className="info-box-text",
                                                    children=["Network"],
                                                ),
                                                html.Span(
                                                    className="info-box-number",
                                                    id="selectedNetwork",
                                                    children=["Selected Network"],
                                                ),
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        ),
                        html.Div(
                            className="col-md-4 col-sm-6 col-xs-12",
                            children=[
                                html.Div(
                                    className="info-box",
                                    children=[
                                        html.Span(
                                            className="info-box-icon bg-aqua",
                                            children=[
                                                html.I(
                                                    className="fa fa-camera",
                                                    children=[],
                                                )
                                            ],
                                        ),
                                        html.Div(
                                            className="info-box-content",
                                            children=[
                                                html.Span(
                                                    className="info-box-text",
                                                    children=["Snapshot"],
                                                ),
                                                html.Span(
                                                    className="info-box-number",
                                                    id="selectedSnapshot",
                                                    children=["Selected snapshot"],
                                                ),
                                            ],
                                        ),
                                    ],
                                )
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="row",
                    id="bgp_graph_container",
                    children=[
                        html.Div(
                            className="col-md-12",
                            children=[
                                html.H1(
                                    children=[
                                        html.Div(
                                            className="box box-danger",
                                            children=[
                                                html.Div(
                                                    className="box-header with-border",
                                                    children=[
                                                        html.H3(
                                                            className="box-title",
                                                            children=["BGP"],
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
                                                                            id="bgp_topology"
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
    Output("bgp_topology", "children"),
    [Input("select-snapshot-button", "value")],
    [State("batfish_host_input", "value"), State("select-network-button", "value")],
)
def set_update_tab_content(snapshot_value, host_value, network_value):
    if not snapshot_value:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    batfish.set_snapshot(snapshot_value)

    return get_bgp_graph(batfish.get_bgp_edges)


# @app.callback(
#     Output(component_id="bgp_graph_container", component_property="style"),
#     [Input("select-snapshot-button", "value")],
# )
# def show_hide_element(snapshot_value):
#     style = {"display": "block"}
#     if not snapshot_value:
#         style = {"display": "none"}
#     return style
