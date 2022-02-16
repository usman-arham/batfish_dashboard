import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from callbacks_folder import trace_callback


# main_page_graph_tab_selected = dict(borderTop="2px solid #3c8dbc")

layout = (
    dcc.Loading(
        id="loading-1",
        type="default",
        children=[
            html.Div(
                className="content-header",
                children=[
                    html.H1(
                        children=[
                            "Trace Routes",
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
            # html.Div(
            #     className="col-md-2",
            #     children=[
            #         html.Div(
            #             dbc.Button(
            #                 "Change Configuration?",
            #                 id="chaos_traceroute_change_config_button",
            #                 className="btn btn-info mt-20",
            #             )
            #         ),
            #     ],
            # ),
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
                                                                    dbc.Col(
                                                                        md=1,
                                                                        children=[
                                                                            html.Div(
                                                                                className="bidir_switch",
                                                                                children=[
                                                                                    daq.BooleanSwitch(
                                                                                        id="main_page_traceroute_bidir_switch",
                                                                                        on=False,
                                                                                        label="Bidirectional",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        md=1,
                                                                        children=[
                                                                            html.Div(
                                                                                className="bidir_switch",
                                                                                children=[
                                                                                    daq.BooleanSwitch(
                                                                                        id="traceroute_advanced_options_switch",
                                                                                        on=False,
                                                                                        label="Advanced",
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="col-md-4",
                                                                        children=[
                                                                            html.Div(
                                                                                className="form-group",
                                                                                children=[
                                                                                    html.Label(
                                                                                        htmlFor="traceroute_src_interface",
                                                                                        children=[
                                                                                            "Source"
                                                                                        ],
                                                                                    ),
                                                                                    dcc.Dropdown(
                                                                                        id="traceroute_src_interface",
                                                                                        placeholder="Select Source",
                                                                                    ),
                                                                                ],
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="col-md-6",
                                                                        children=[
                                                                            html.Div(
                                                                                className="form-group",
                                                                                children=[
                                                                                    html.Label(
                                                                                        htmlFor="traceroute_dst_interface",
                                                                                        children=[
                                                                                            "Destination"
                                                                                        ],
                                                                                    ),
                                                                                    dbc.InputGroup(
                                                                                        [
                                                                                            html.Div(
                                                                                                id="traceroute_dst_type_dropdown_div",
                                                                                                children=[
                                                                                                    dcc.Dropdown(
                                                                                                        id="traceroute_dst_type_dropdown",
                                                                                                        options=[
                                                                                                            {
                                                                                                                "label": "IP",
                                                                                                                "value": "IP",
                                                                                                            },
                                                                                                            {
                                                                                                                "label": "Interface",
                                                                                                                "value": "Interface",
                                                                                                            },
                                                                                                        ],
                                                                                                        value="Interface",
                                                                                                    )
                                                                                                ],
                                                                                            ),
                                                                                            html.Div(
                                                                                                id="traceroute_dst_input",
                                                                                                children=[
                                                                                                    dcc.Dropdown(
                                                                                                        id="traceroute_dst",
                                                                                                        placeholder="Select Destination",
                                                                                                    )
                                                                                                ],
                                                                                            ),
                                                                                        ]
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
                                                                                        "Trace!!!",
                                                                                        id="main_page_traceroute_submit",
                                                                                        className="btn btn-primary pull-right",
                                                                                        disabled=True,
                                                                                    )
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    )
                                                                ],
                                                            ),
                                                            dbc.Row(
                                                                id="traceroute-advanced_options_row"
                                                            ),
                                                            dbc.Row(
                                                                id="traceroute-alter-node",
                                                                children=[],
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
                        id="forward_trace_container",
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
                                                                children=[
                                                                    "Forward Trace"
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="box-tools pull-right",
                                                                children=[
                                                                    html.H3(
                                                                        className="box-title",
                                                                        children=[],
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
                                                                                id="main_page_forward_traceroute_graph"
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            )
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="box-footer",
                                                        children=[
                                                            html.Div(
                                                                className="row",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-md-12",
                                                                        children=[
                                                                            dcc.Tabs(
                                                                                id="forward_traceroute_tabs",
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
                    html.Div(
                        className="row",
                        id="reverse_trace_container",
                        style={"display": "none"},
                        children=[
                            html.Div(
                                className="col-md-12",
                                children=[
                                    html.H1(
                                        children=[
                                            html.Div(
                                                className="box box-info",
                                                children=[
                                                    html.Div(
                                                        className="box-header with-border",
                                                        children=[
                                                            html.H3(
                                                                className="box-title",
                                                                children=[
                                                                    "Reverse Trace"
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="box-tools pull-right",
                                                                children=[
                                                                    html.H3(
                                                                        className="box-title",
                                                                        children=[],
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
                                                                                id="main_page_reverse_traceroute_graph"
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            )
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="box-footer",
                                                        children=[
                                                            html.Div(
                                                                className="row",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-md-12 nav-tabs-custom",
                                                                        children=[
                                                                            dcc.Tabs(
                                                                                id="reverse_traceroute_tabs",
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
                    html.Div(
                        className="row",
                        style={"display": "none"},
                        id="chaos_filter_container",
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
                                                                children=[
                                                                    "Chaos Filters"
                                                                ],
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
                                                                                        htmlFor="traceroute_choose_node",
                                                                                        children=[
                                                                                            "Chaos Node"
                                                                                        ],
                                                                                    ),
                                                                                    dcc.Dropdown(
                                                                                        id="traceroute_choose_node",
                                                                                        placeholder="Chaos Node",
                                                                                    ),
                                                                                ],
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="col-md-2",
                                                                        children=[
                                                                            html.Div(
                                                                                className="bidir_switch",
                                                                                children=[
                                                                                    daq.BooleanSwitch(
                                                                                        id="deactivate_node_switch",
                                                                                        on=False,
                                                                                        label="Deactivate Node",
                                                                                        disabled=True,
                                                                                    ),
                                                                                ],
                                                                            ),
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="col-md-4",
                                                                        id="select_interface_container",
                                                                        children=[
                                                                            html.Div(
                                                                                className="form-group",
                                                                                children=[
                                                                                    html.Label(
                                                                                        htmlFor="traceroute_dst_interface",
                                                                                        children=[
                                                                                            "Deactivate Interface"
                                                                                        ],
                                                                                    ),
                                                                                    dcc.Dropdown(
                                                                                        id="traceroute_deactivate_interface",
                                                                                        placeholder="Select Interface",
                                                                                        disabled=True,
                                                                                    ),
                                                                                ],
                                                                            )
                                                                        ],
                                                                    ),
                                                                    html.Div(
                                                                        className="col-md-2",
                                                                        children=[
                                                                            html.Div(
                                                                                dbc.Button(
                                                                                    "Change Configuration?",
                                                                                    id="chaos_traceroute_change_config_button",
                                                                                    className="btn btn-info mt-20",
                                                                                    disabled=True,
                                                                                )
                                                                            ),
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
                                                                                        "Chaos!!!",
                                                                                        id="chaos_traceroute_submit",
                                                                                        className="btn btn-primary pull-right",
                                                                                        disabled=False,
                                                                                    ),
                                                                                    daq.BooleanSwitch(
                                                                                        id="change_configuration_switch",
                                                                                        on=False,
                                                                                        style={
                                                                                            "display": "none"
                                                                                        },
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
                                        ]
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className="row",
                        id="chaos_trace_container",
                        style={"display": "none"},
                        children=[
                            html.Div(
                                className="col-md-12",
                                children=[
                                    html.H1(
                                        children=[
                                            html.Div(
                                                className="box box-info",
                                                children=[
                                                    html.Div(
                                                        className="box-header with-border",
                                                        children=[
                                                            html.H3(
                                                                className="box-title",
                                                                children=[
                                                                    "Chaos Trace"
                                                                ],
                                                            ),
                                                            html.Div(
                                                                className="box-tools pull-right",
                                                                children=[
                                                                    html.H3(
                                                                        className="box-title",
                                                                        children=[],
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
                                                                                id="chaos_traceroute_graph"
                                                                            ),
                                                                        ],
                                                                    ),
                                                                ],
                                                            )
                                                        ],
                                                    ),
                                                    html.Div(
                                                        className="box-footer",
                                                        children=[
                                                            html.Div(
                                                                className="row",
                                                                children=[
                                                                    html.Div(
                                                                        className="col-md-12 nav-tabs-custom",
                                                                        children=[
                                                                            dcc.Tabs(
                                                                                id="chaos_traceroute_tabs",
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
    ),
    # Change Configuration Modal
    dbc.Modal(
        id="change_configuration_modal",
        is_open=False,  # Open the modal at opening the webpage.
        size="lg",  # "sm", "lg", "xl" = small, large or extra large
        backdrop=True,  # Modal to not be closed by clicking on backdrop
        scrollable=True,  # Scrollable in case of large amount of text
        centered=False,  # Vertically center modal
        keyboard=True,  # Close modal when escape is pressed
        fade=True,  # Let the modal fade instead of appear.
        children=[
            html.Div(
                className="modal-header",
                children=[
                    html.H5(className="modal-title", children=["Change Configuration"]),
                    html.Button(
                        className="close",
                        id="close2",
                        children=[html.Span(children=["×"])],
                    ),
                ],
            ),
            dbc.ModalBody(
                children=[
                    html.Div(
                        [
                            dcc.Textarea(
                                id="change_configuration_textarea",
                                value="",
                                style={"width": "100%", "height": "500px"},
                            ),
                        ],
                    ),
                ],
            ),
            dbc.ModalFooter(
                [
                    dbc.Button(
                        "Close",
                        id="close1",
                        className="ms-auto btn-danger",
                        n_clicks=0,
                    ),
                    dbc.Button(
                        "Submit",
                        id="change_configuration_submit",
                        className="ms-auto btn-primary",
                    ),
                ]
            ),
        ],
    ),
)
