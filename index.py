import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from pages import index, l3vpn, questions, trace, ospf, bgp, isis

app.title = "Dashboard"
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport">
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        <script>
                FontAwesomeConfig = { autoReplaceSvg: false }
        </script>
        {%css%}
        <!-- Google Font -->
        <link rel="stylesheet"
            href="https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,600,700,300italic,400italic,600italic">
    </head>
    <body class="fixed sidebar-mini skin-blue-light">
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
            
        </footer>
    </body>
</html>
"""
app.layout = index.layout


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == None or pathname == "/":
        return l3vpn.layout
    elif pathname == "/questions":
        return questions.layout
    elif pathname == "/ospf":
        return ospf.layout
    elif pathname == "/bgp":
        return bgp.layout
    elif pathname == "/isis":
        return isis.layout
    elif pathname == "/trace":
        return trace.layout
    else:
        return dashboard.layout


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
