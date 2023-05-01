import dash
from dash import html,dcc, Input, Output
import dash_bootstrap_components as dbc
import os
import plotly.express as px
import json

import plotly.graph_objects as go
import plotly.io as pio

custom_template = open("assets/custom_template.json")
data = json.load(custom_template)
pio.templates["custom_ronaldo"] = go.layout.Template(data)

app = dash.Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.LUX],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])


sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2 text-white"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in dash.page_registry.values()
    ],
    vertical=True,
    pills=True,
    class_name="bg-dark",
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Cristiano Ronaldo Dataviz App", style={'fontSize':50, 'textAlign':'center', 'color': '#ffffff'}))
    ]),
    
    html.Hr(),
    
    dbc.Row([
        dbc.Col([sidebar], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2, className="bg-dark"),
        
        dbc.Col([dash.page_container], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10, className="bg-dark")
    ])
], fluid=True, class_name="bg-dark vh-100")


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('PORT','8050'), host='0.0.0.0', dev_tools_silence_routes_logging = False)

