import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_daq as daq


main_page_graph_tab_selected = dict(borderTop="2px solid #3c8dbc")

main_page_layout = html.Div(
    id="main-page",
    children=[
        html.Div(
            id="title-bar-div",
            children=[
                html.Header(
                    id="title-bar",
                    children=[
                        html.H1(
                            "Dashboard",
                            id="title-bar-text",
                        )
                    ],
                )
            ],
        ),
        html.Br(),
        html.Div(
            style={"position": "relative", "left": "7px"},
            children=[
                html.Div(
                    [
                        html.Button(
                            "Set Host",
                            id="set-batfish-host-button",
                            className="main_page_button ",
                        ),
                    ],
                    className="main_page_button_div d-none",
                ),
                html.Div(
                    [
                        html.Button(
                            "Create/Delete Network",
                            id="create-network-button",
                            className="main_page_button",
                        ),
                    ],
                    className="main_page_button_div d-none",
                ),
                html.Div(
                    [
                        html.Button(
                            "Create/Delete Snapshot",
                            id="create-snapshot-button",
                            className="main_page_button",
                        ),
                    ],
                    className="main_page_button_div d-none",
                ),
                html.Div(
                    [],
                    className="main_page_button_div",
                    id="select-network-div",
                ),
                html.Div(
                    [],
                    className="main_page_button_div",
                    id="select-snapshot-div",
                ),
                html.Div(
                    [
                        html.Button(
                            "Ask a Question",
                            id="ask-question-button",
                            className="main_page_button",
                        ),
                    ],
                    className="main_page_button_div",
                ),
                html.Div(
                    style=dict(width="1000px"),
                    children=[
                        dbc.Collapse(
                            dbc.Card(
                                className="main_page_card",
                                children=[
                                    dbc.CardBody(
                                        children=[
                                            dbc.Form(
                                                [
                                                    dbc.FormGroup(
                                                        [
                                                            dbc.Input(
                                                                id="batfish_host_input",
                                                                value="host.docker.internal",
                                                                placeholder="",
                                                                persistence=True,
                                                            ),
                                                        ],
                                                        className="mr-3",
                                                    ),
                                                    dbc.Button(
                                                        "Submit",
                                                        id="set_batfish_host_submit_button",
                                                        color="dark",
                                                        outline=True,
                                                        size="sm",
                                                        style=dict(
                                                            height="25px",
                                                        ),
                                                    ),
                                                ],
                                                inline=True,
                                            )
                                        ]
                                    )
                                ],
                            ),
                            id="batfishhost-collapse",
                        ),
                        dbc.Collapse(
                            dbc.Card(
                                className="main_page_card",
                                children=[dbc.CardBody(children=[])],
                            ),
                            id="create-network-collapse",
                        ),
                    ],
                ),
                dcc.Store(id="memory-output"),
            ],
        ),
        html.Div(
            style={"position": "relative", "left": "10px", "display": "flex"},
            children=[
                html.Div(
                    style=dict(
                        width="100%",
                        flex="1",
                    ),
                    children=[
                        dcc.Tabs(
                            id="main-page-tabs",
                            value="layer3",
                            children=[
                                dcc.Tab(
                                    selected_style=main_page_graph_tab_selected,
                                    className="main-page-graph-tab",
                                    id={"type": "main_tabs", "index": 0},
                                    label="Layer 3",
                                    value="layer3",
                                ),
                                dcc.Tab(
                                    selected_style=main_page_graph_tab_selected,
                                    className="main-page-graph-tab",
                                    id={"type": "main_tabs", "index": 1},
                                    label="OSPF",
                                    value="ospf",
                                ),
                                dcc.Tab(
                                    selected_style=main_page_graph_tab_selected,
                                    className="main-page-graph-tab",
                                    id={"type": "main_tabs", "index": 2},
                                    label="BGP",
                                    value="bgp",
                                ),
                                dcc.Tab(
                                    selected_style=main_page_graph_tab_selected,
                                    className="main-page-graph-tab",
                                    id={"type": "main_tabs", "index": 3},
                                    label="Trace Route",
                                    value="traceroute",
                                ),
                                dcc.Tab(
                                    selected_style=main_page_graph_tab_selected,
                                    className="main-page-graph-tab",
                                    id={"type": "main_tabs", "index": 4},
                                    label="All Things ACL",
                                    value="all_things_acl",
                                ),
                            ],
                        ),
                        html.Div(
                            id="main-page-tabs-content",
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            id="graph_layout_options",
            style={"position": "relative", "left": "10px", "display": "none"},
            children=[
                html.Div(
                    dcc.Dropdown(
                        id="dropdown-update-layout",
                        value=None,
                        clearable=False,
                        style=dict(flex="1", verticalAlign="middle", width="200px"),
                        placeholder="Choose Graph Layout",
                        options=[
                            {"label": name.capitalize(), "value": name}
                            for name in [
                                "grid",
                                "random",
                                "circle",
                                "cose",
                                "concentric",
                                "breadthfirst",
                            ]
                        ],
                    )
                ),
                html.Div(id="breadthfirst-roots", children=[]),
            ],
        ),
        html.Div(
            style={"position": "relative", "left": "10px"},
            children=[
                html.P(
                    id="cytoscape-mouseoverNodeData-output", style={"display": "none"}
                ),
                html.P(
                    id="cytoscape-mouseoverEdgeData-output", style={"display": "none"}
                ),
                html.P(id="batfish-host-output", style={"display": "none"}),
                html.P(id="batfish-network-output", style={"display": "none"}),
                html.P(id="num_of_traces", style={"display": "none"}),
            ],
        ),
        # Create Snapshot Modal
        html.Div(
            children=[
                dbc.Modal(
                    id="create_snapshot_modal",
                    size="lg",
                    children=[
                        dbc.ModalHeader("Create Snapshot!"),
                        dbc.ModalBody(
                            children=[
                                html.Div(style=dict(display="flex")),
                                html.Div(
                                    [],
                                    id="select-network-snapshot-modal",
                                    style=dict(flex="1"),
                                ),
                                html.Div(
                                    [],
                                    id="delete-snapshot-dropdown-div",
                                    style=dict(flex="1"),
                                ),
                                html.Div(
                                    [
                                        dcc.Upload(
                                            className="Snapshot_Upload",
                                            id="device-configs-upload-data",
                                            children=html.Div(
                                                className="inside_drag_and_drop",
                                                children=[
                                                    html.P(
                                                        className="upload_p",
                                                        children=[
                                                            html.H3(
                                                                "Device Configurations"
                                                            ),
                                                            "Drag and Drop or ",
                                                            html.A("Select Files"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Allow multiple files to be uploaded
                                            multiple=True,
                                        ),
                                        dcc.Upload(
                                            className="Snapshot_Upload",
                                            id="host-configs-upload-data",
                                            children=html.Div(
                                                className="inside_drag_and_drop",
                                                children=[
                                                    html.P(
                                                        className="upload_p",
                                                        children=[
                                                            html.H3(
                                                                "Host Configurations"
                                                            ),
                                                            "Drag and Drop or ",
                                                            html.A("Select Files"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Allow multiple files to be uploaded
                                            multiple=True,
                                        ),
                                        dcc.Upload(
                                            className="Snapshot_Upload",
                                            id="iptables-configs-upload-data",
                                            children=html.Div(
                                                className="inside_drag_and_drop",
                                                children=[
                                                    html.P(
                                                        className="upload_p",
                                                        children=[
                                                            html.H3(
                                                                "IP Table Configurations"
                                                            ),
                                                            "Drag and Drop or ",
                                                            html.A("Select Files"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Allow multiple files to be uploaded
                                            multiple=True,
                                        ),
                                        dcc.Upload(
                                            className="Snapshot_Upload",
                                            id="aws-configs-upload-data",
                                            children=html.Div(
                                                className="inside_drag_and_drop",
                                                children=[
                                                    html.P(
                                                        className="upload_p",
                                                        children=[
                                                            html.H3(
                                                                "AWS Configurations"
                                                            ),
                                                            "Drag and Drop or ",
                                                            html.A("Select Files"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Allow multiple files to be uploaded
                                            multiple=True,
                                        ),
                                        dcc.Upload(
                                            className="Snapshot_Upload",
                                            id="misc-configs-upload-data",
                                            children=html.Div(
                                                className="inside_drag_and_drop",
                                                children=[
                                                    html.P(
                                                        className="upload_p",
                                                        children=[
                                                            html.H3(
                                                                "Miscellaneous Configurations"
                                                            ),
                                                            "Drag and Drop or ",
                                                            html.A("Select Files"),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            # Allow multiple files to be uploaded
                                            multiple=True,
                                        ),
                                        html.Div(id="output-data-upload"),
                                    ]
                                ),
                            ],
                        ),
                        dbc.ModalFooter(
                            children=[
                                html.A(
                                    "How to format your configurations!",
                                    href="https://pybatfish.readthedocs.io/en/latest/formats.html",
                                ),
                                dbc.FormGroup(
                                    [
                                        dbc.Input(
                                            id="create-snapshot-name",
                                            value="",
                                            placeholder="New Snapshot Name",
                                        ),
                                        dbc.FormFeedback(
                                            "Please enter a name for the snapshot",
                                            valid=False,
                                        ),
                                    ],
                                    className="mr-3",
                                ),
                                dbc.Button(
                                    "Submit",
                                    id="create_snapshot_submit_button",
                                    color="dark",
                                    outline=True,
                                    style=dict(
                                        height="25px",
                                    ),
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        # Ask a Question Modal
        html.Div(
            children=[
                dbc.Modal(
                    id="ask-a-question-modal",
                    size="xl",
                    scrollable=True,
                    children=[
                        dbc.ModalHeader("Ask a Question!"),
                        dbc.ModalBody(
                            children=[
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="select-question-button",
                                            placeholder="Select Question",
                                            style={"margin": "5px", "width": "150px"},
                                            options=[],
                                            value=None,
                                        ),
                                    ],
                                    id="ask-a-question-dropdown-modal",
                                    style=dict(
                                        position="relative",
                                        height="100px",
                                        margin_top="10px",
                                    ),
                                ),
                                html.Div(id="question-info"),
                                html.Div(id="ask-a-question-table"),
                            ],
                        ),
                    ],
                )
            ],
        ),
        # Change Configuration Modal
        html.Div(
            children=[
                dbc.Modal(
                    id="change_configuration_modal",
                    size="xl",
                    scrollable=True,
                    children=[
                        dbc.ModalHeader("Change Configuration!"),
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
                                html.Button("Submit", id="change_configuration_submit"),
                            ],
                        ),
                    ],
                )
            ],
        ),
        # ACL Configuration Modal
        html.Div(
            children=[
                dbc.Modal(
                    id="acl_configuration_modal",
                    size="xl",
                    scrollable=True,
                    children=[
                        dbc.ModalHeader("Get Configuration!"),
                        dbc.ModalBody(
                            children=[
                                dbc.InputGroup(
                                    [
                                        dbc.Select(
                                            id="acl_choose_node",
                                            options="",
                                            value="",
                                        ),
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Textarea(
                                            id="acl_configuration_textarea",
                                            value="",
                                            style={"width": "100%", "height": "500px"},
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
)
