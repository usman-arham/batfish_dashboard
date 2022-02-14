import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from components.batfish import Batfish
from components.functions import get_isis_graph
import pandas as pd
import dash_table


layout = dcc.Loading(
    id="loading-1",
    type="default",
    children=[
        html.Div(
            className="content-header",
            children=[
                html.H1(
                    children=[
                        "Questions",
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
                            children=["×"],
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
                    children=[
                        html.Div(
                            className="col-md-12",
                            children=[
                                html.H1(
                                    children=[
                                        html.Div(
                                            className="box box-solid bg-warning box-warning",
                                            children=[
                                                html.Div(
                                                    className="box-header with-border",
                                                    children=[
                                                        html.H3(
                                                            className="box-title",
                                                            children=["Filters"],
                                                        ),
                                                        html.Div(
                                                            className="box-tools pull-right",
                                                            children=[
                                                                html.H3(
                                                                    className="box-title",
                                                                    children=[
                                                                        html.Button(
                                                                            className="btn btn-box-tool",
                                                                            **{
                                                                                "data-widget": "collapse"
                                                                            },
                                                                            children=[
                                                                                html.I(
                                                                                    className="fa fa-minus",
                                                                                )
                                                                            ],
                                                                        ),
                                                                    ],
                                                                )
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="box-body",
                                                    children=[
                                                        dbc.Row(
                                                            children=[
                                                                html.Div(
                                                                    className="col-md-4",
                                                                    children=[
                                                                        html.Div(
                                                                            className="form-group",
                                                                            children=[
                                                                                html.Label(
                                                                                    htmlFor="question",
                                                                                    children=[
                                                                                        "Question"
                                                                                    ],
                                                                                ),
                                                                                dcc.Dropdown(
                                                                                    id="question",
                                                                                    placeholder="Select Question",
                                                                                ),
                                                                            ],
                                                                        )
                                                                    ],
                                                                ),
                                                            ],
                                                        ),
                                                        dbc.Row(
                                                            children=[
                                                                html.Div(
                                                                    className="col-md-12",
                                                                    children=[
                                                                        html.Div(
                                                                            className="box-footer",
                                                                            children=[
                                                                                dbc.Button(
                                                                                    "Submit!!!",
                                                                                    id="questionsSubmit",
                                                                                    className="btn btn-primary pull-right",
                                                                                    disabled=True,
                                                                                )
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
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="row",
                    id="reslultsContainer",
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
                                                            id="resultHeading",
                                                            className="box-title",
                                                            children=["Results"],
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
                                                                            id="results",
                                                                            className="col-md-12",
                                                                            children=[],
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


# @app.callback(
#     Output("isis_topology", "children"),
#     [Input("select-snapshot-button", "value")],
#     [State("batfish_host_input", "value"), State("select-network-button", "value")],
# )
# def set_update_tab_content(snapshot_value, host_value, network_value):
#     if not snapshot_value:
#         raise PreventUpdate
#     batfish = Batfish(host_value)
#     batfish.set_network(network_value)
#     batfish.set_snapshot(snapshot_value)
#     return get_isis_graph(batfish.get_isis_edges)


@app.callback(
    Output("question", "options"),
    [Input("select-snapshot-button", "value")],
    [State("batfish_host_input", "value")],
)
def get_questions(n, host_value):
    batfish = Batfish(host_value)
    result = [
        {"label": question["name"], "value": question["name"]}
        for question in batfish.list_questions
    ]
    return result


@app.callback(
    Output("questionsSubmit", "disabled"),
    [
        Input("question", "value"),
    ],
)
def enable_submit_button(question):
    if question is None:
        return True
    return False


@app.callback(
    [
        Output(component_id="reslultsContainer", component_property="style"),
        Output("resultHeading", "children"),
    ],
    [Input("questionsSubmit", "n_clicks")],
    [
        State("question", "value"),
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def question_descriptors(
    questionsSubmit, question, host_value, network_value, snapshot_value
):
    if not question:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    batfish.set_snapshot(snapshot_value)
    children = [html.P(batfish.get_question_description(question))]
    return {"display": "block"}, children


@app.callback(
    Output("results", "children"),
    [Input("questionsSubmit", "n_clicks")],
    [
        State("question", "value"),
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def ask_a_question_modal_table(
    questionsSubmit, question, host_value, network_value, snapshot_value
):
    if question is None:
        raise PreventUpdate
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    batfish.set_snapshot(snapshot_value)
    batfish_df = batfish.get_info(question)
    batfish_df.to_csv("test.csv", index=False)
    new_df = pd.read_csv("test.csv")
    children = dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "deletable": True} for i in batfish_df.columns],
        data=new_df.to_dict("records"),
        filter_action="native",
        export_format="csv",
    )
    return children
