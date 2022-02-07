import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from layouts import main_page_layout
import callbacks

app.title = "Dashboard"
app.layout = main_page_layout


external_css = [
    "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ["https://code.jquery.com/jquery-3.2.1.min.js"]


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
