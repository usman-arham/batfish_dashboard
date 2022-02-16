from app import app
from components.batfish import Batfish
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash
from components.functions import get_traceroute_details
from components.functions import delete_old_files


# write batfish interface of a snapshot to memory
@app.callback(
    Output("memory", "data"),
    [Input("select-snapshot-button", "value")],
    [State("batfish_host_input", "value"), State("select-network-button", "value")],
)
def get_src_dst_options(snapshot_value, host_value, network_value):
    if not snapshot_value:
        raise PreventUpdate
    # time.sleep(0.10)
    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    batfish.set_snapshot(snapshot_value)
    batfish_df = batfish.get_interfaces
    interfaces = [
        {
            "label": row["Node"] + "-" + row["Interface"] + "-" + row["IP"],
            "value": row["Node"] + "[" + row["Interface"] + "]",
        }
        for index, row in batfish_df.iterrows()
    ]

    data = {"interfaces": interfaces}

    return data


@app.callback(
    [
        Output("traceroute_src_interface", "options"),
        Output("traceroute_dst", "options"),
    ],
    [Input("memory", "modified_timestamp")],
    [State("memory", "data")],
)
def get_src_dst_options(ts, data):
    if ts is None:
        raise PreventUpdate

    data = data or {}
    return data.get("interfaces", 0), data.get("interfaces", 0)


@app.callback(
    Output("traceroute_dst_input", "children"),
    [Input("traceroute_dst_type_dropdown", "value")],
    [State("memory", "data")],
)
def set_dst_type_input(dst_type, data):
    if not dst_type:
        raise PreventUpdate

    data = data or {}

    if dst_type == "Interface":
        interfaces = data.get("interfaces", [])
        children = dcc.Dropdown(
            id="traceroute_dst",
            placeholder="Select Destination",
            options=interfaces,
        )
    else:
        children = (
            dcc.Input(
                id="traceroute_dst",
                type="text",
                placeholder="Input IP Address",
                className="form-control",
            ),
        )

    return children


@app.callback(
    Output("main_page_traceroute_submit", "disabled"),
    [Input("traceroute_src_interface", "value"), Input("traceroute_dst", "value")],
)
def set_dst_type_input(src, dst):
    if src is None or dst is None:
        return True
    return False


@app.callback(
    [
        Output("main_page_forward_traceroute_graph", "children"),
        Output("forward_traceroute_tabs", "children"),
        Output(component_id="forward_trace_container", component_property="style"),
        Output("main_page_reverse_traceroute_graph", "children"),
        Output("reverse_traceroute_tabs", "children"),
        Output(component_id="reverse_trace_container", component_property="style"),
        Output(component_id="chaos_filter_container", component_property="style"),
    ],
    [
        Input("traceroute_src_interface", "value"),
        Input("traceroute_dst", "value"),
        Input("main_page_traceroute_submit", "n_clicks"),
        Input("main_page_traceroute_bidir_switch", "on"),
        # Input("traceroute_src_ports", "value"),
        # Input("traceroute_dst_ports", "value"),
        # Input("traceroute_applications", "value"),
        # Input("traceroute_ip_protocols", "value"),
    ],
    [
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def set_update_trace_graph(
    source,
    destination,
    submit,
    bidir,
    # src_ports,
    # dst_ports,
    # applications,
    # ip_protocols,
    host_value,
    network_value,
    snapshot_value,
):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id != "main_page_traceroute_submit":
        raise PreventUpdate

    src_ports = None
    dst_ports = None
    applications = None
    ip_protocols = None

    batfish = Batfish(host_value)
    batfish.set_network(network_value)
    result = batfish.traceroute(
        source,
        destination,
        bidir,
        snapshot_value,
        src_ports,
        dst_ports,
        applications,
        ip_protocols,
    )
    reverse_flow_graph = []
    reverse_flow_traces = []
    forward_trace_style = {"display": "none"}
    reverse_trace_style = {"display": "none"}
    if bidir:
        forward_flow_details = get_traceroute_details("forward", result, True)
        forward_flow_graph = forward_flow_details[0]
        forward_flow_traces = forward_flow_details[1]
        forward_trace_style = {"display": "block"}
        reverse_flow_details = get_traceroute_details("reverse", result, True)
        reverse_flow_graph = reverse_flow_details[0]
        reverse_flow_traces = reverse_flow_details[1]
        reverse_trace_style = {"display": "block"}

    else:
        forward_flow_details = get_traceroute_details("forward", result, False)
        forward_flow_graph = forward_flow_details[0]
        forward_flow_traces = forward_flow_details[1]
        forward_trace_style = {"display": "block"}

    return (
        forward_flow_graph,
        forward_flow_traces,
        forward_trace_style,
        reverse_flow_graph,
        reverse_flow_traces,
        reverse_trace_style,
        {"display": "block"},
    )


# ************************* Chaos Callbacks *************************
@app.callback(
    [
        Output("deactivate_node_switch", "disabled"),
        Output("traceroute_deactivate_interface", "disabled"),
        Output("chaos_traceroute_change_config_button", "disabled"),
    ],
    [
        Input("traceroute_choose_node", "value"),
    ],
)
def enable_buttons(
    node,
):
    if not node:
        return True, True, True
    return False, False, False


@app.callback(
    Output("traceroute_choose_node", "options"),
    [
        Input(component_id="chaos_filter_container", component_property="style"),
        Input("traceroute-cytoscape", "elements"),
    ],
    [
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def get_chaos_nodes_options(
    style, graph_elements, batfish_host, batfish_network, original_snapshot
):
    if style["display"] == "none":
        raise PreventUpdate
    # ctx = dash.callback_context
    # button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    # if button_id in ["chaos_traceroute_submit"]:
    #     raise PreventUpdate
    traceroute_nodes = []
    try:
        for traceroute_node in graph_elements:
            traceroute_nodes.append(traceroute_node["data"]["label"])
    except KeyError:
        pass

    batfish = Batfish(batfish_host)
    batfish.set_network(batfish_network)
    batfish.set_snapshot(original_snapshot)

    batfish_df = batfish.get_info("nodeProperties")
    batfish_df = batfish_df.set_index("Node")

    nodes_dict = [{"label": node, "value": node} for node in set(traceroute_nodes)]
    node = nodes_dict[0]["value"]
    interfaces = batfish_df.loc[node].at["Interfaces"]

    interfaces_dict = [{"label": "", "value": ""}]

    interfaces_dict += [
        {"label": interface, "value": interface} for interface in interfaces
    ]
    return nodes_dict


@app.callback(
    [
        Output(component_id="select_interface_container", component_property="style"),
        Output(
            component_id="chaos_traceroute_change_config_button",
            component_property="style",
        ),
    ],
    [Input("deactivate_node_switch", "on")],
)
def display_interfaces_dropdown(deactivate_node_switch_on):
    style = {"display": "block"}
    if deactivate_node_switch_on:
        style = {"display": "none"}

    return style, style


@app.callback(
    Output("traceroute_deactivate_interface", "options"),
    [Input("traceroute_choose_node", "value")],
    [
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def display_interfaces_for_node(
    choosen_node, batfish_host, batfish_network, original_snapshot
):
    # ctx = dash.callback_context
    # button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if not choosen_node:
        raise PreventUpdate

    batfish = Batfish(batfish_host)
    batfish.set_network(batfish_network)
    batfish.set_snapshot(original_snapshot)

    batfish_df = batfish.get_info("nodeProperties")
    batfish_df = batfish_df.set_index("Node")

    interfaces = batfish_df.loc[choosen_node].at["Interfaces"]

    interfaces_dict = [{"label": "", "value": ""}]

    interfaces_dict += [
        {"label": interface, "value": interface} for interface in interfaces
    ]
    options = interfaces_dict
    return options


@app.callback(
    [
        Output(component_id="chaos_trace_container", component_property="style"),
        Output("chaos_traceroute_graph", "children"),
        Output("chaos_traceroute_tabs", "children"),
    ],
    [
        Input("traceroute_src_interface", "value"),
        Input("traceroute_dst", "value"),
        Input("chaos_traceroute_submit", "n_clicks"),
        Input("traceroute_choose_node", "value"),
        Input("deactivate_node_switch", "on"),
        Input("traceroute_deactivate_interface", "value"),
        # Input("traceroute_src_ports", "value"),
        # Input("traceroute_dst_ports", "value"),
        # Input("traceroute_applications", "value"),
        # Input("traceroute_ip_protocols", "value"),
    ],
    [
        State("change_configuration_switch", "on"),
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def set_chaos_trace_graph(
    source,
    destination,
    submit,
    choose_node,
    deactivate_node,
    deactivated_interface,
    # src_ports,
    # dst_ports,
    # applications,
    # ip_protocols,
    change_configuration_switch,
    host_value,
    network_value,
    snapshot_value,
):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    deactivated_nodes = []
    deactivated_interfaces = []

    if button_id not in ["chaos_traceroute_submit"]:
        raise PreventUpdate

    src_ports = None
    dst_ports = None
    applications = None
    ip_protocols = None
    batfish = Batfish(host_value)
    batfish.set_network(network_value)

    bidir = False
    if change_configuration_switch:
        reference_snapshot = snapshot_value + "_CHANGED"
        batfish.init_snapshot(reference_snapshot)
    else:
        reference_snapshot = snapshot_value + "_FAIL"
        deactivated_nodes.append(choose_node)
        if not deactivate_node:
            deactivated_interfaces.append(deactivated_interface)
        batfish.network_failure(
            snapshot_value,
            reference_snapshot,
            deactivated_nodes,
            deactivated_interfaces,
        )

    result = batfish.traceroute(
        source,
        destination,
        bidir,
        reference_snapshot,
        src_ports,
        dst_ports,
        applications,
        ip_protocols,
    )
    chaos_flow_details = get_traceroute_details("forward", result, False, True)
    chaos_flow_graph = chaos_flow_details[0]
    chaos_flow_traces = chaos_flow_details[1]
    delete_old_files()
    style = {"display": "block"}
    return style, chaos_flow_graph, chaos_flow_traces


@app.callback(
    Output("change_configuration_textarea", "value"),
    [Input("chaos_traceroute_change_config_button", "n_clicks")],
    [
        State("traceroute_choose_node", "value"),
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def get_change_configuration(
    n, choose_node, batfish_host, batfish_network, batfish_snapshot
):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id != "chaos_traceroute_change_config_button":
        raise PreventUpdate

    batfish = Batfish(batfish_host)
    batfish.set_network(batfish_network)
    batfish.set_snapshot(batfish_snapshot)
    nodes_df = batfish.get_info("fileParseStatus")
    for key, value in nodes_df.iterrows():
        if choose_node.lower() in value["Nodes"]:
            return batfish.get_configuration(value["File_Name"], batfish_snapshot)


@app.callback(
    Output("change_configuration_modal", "is_open"),
    [
        Input("chaos_traceroute_change_config_button", "n_clicks"),
        Input("close1", "n_clicks"),
        Input("close2", "n_clicks"),
        Input("change_configuration_submit", "n_clicks"),
    ],
    [State("change_configuration_modal", "is_open")],
)
def open_change_configuration_modal(n1, n2, n3, n4, is_open):
    if n1 or n2 or n3:
        return not is_open
    if n4:
        return False
    return is_open


@app.callback(
    Output("change_configuration_switch", "on"),
    [
        Input("change_configuration_textarea", "value"),
        Input("change_configuration_submit", "n_clicks"),
    ],
    [
        State("traceroute_choose_node", "value"),
        State("batfish_host_input", "value"),
        State("select-network-button", "value"),
        State("select-snapshot-button", "value"),
    ],
)
def set_change_configuration(
    changed_configuration,
    changed_configuration_submit,
    choose_node,
    batfish_host,
    batfish_network,
    batfish_snapshot,
):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id not in ["change_configuration_submit"]:
        raise PreventUpdate

    batfish = Batfish(batfish_host)
    batfish.set_network(batfish_network)
    batfish.set_snapshot(batfish_snapshot)

    with open(r"snapshot_holder/configs/" + choose_node + ".txt", "w") as f:
        f.write(changed_configuration)

    nodes_df = batfish.get_info("fileParseStatus")
    for key, value in nodes_df.iterrows():
        if choose_node.lower() not in value["Nodes"]:
            with open(
                r"snapshot_holder/configs/" + value["Nodes"][0] + ".txt", "w"
            ) as f:
                f.write(batfish.get_configuration(value["File_Name"], batfish_snapshot))
    return True
