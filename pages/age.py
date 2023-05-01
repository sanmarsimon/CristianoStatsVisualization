import dash
from dash import dcc, html, callback
import plotly.express as px
import dash_bootstrap_components as dbc
from get_age_data import get_data
import plotly.graph_objects as go


dash.register_page(__name__, name='Age', order=2)

data = get_data()
figure = go.Figure(data=[go.Bar(x=data['Age'], y=data['Goals per game'], hovertemplate='Age: %{x} years<br>Goals per game: %{y} <extra></extra>')])
figure.update_layout(title='Goals ratio ', xaxis_title='Age', template='custom_ronaldo',annotations=[dict(text="Number of goals per match", x=18, y=1.8, showarrow=False, font=dict(size=16))])

layout = dbc.Row(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Age", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Col(
            dcc.Graph(
                id='goals-graph',
                figure = figure
            ),
            className="col-12"
        ),
        dbc.Col(
            dcc.RadioItems(
                id='mode-radio',
                options=[
                    {'label': 'Goals per game', 'value': 'Goals per game'},
                    {'label': 'Total goals', 'value': 'Total goals'},
                ],
                value='Goals per game',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'},
                inputStyle={'margin-right': '5px'}
            ),
            className="d-flex col-12 justify-content-center m-3 fs-4 text-white",
        )
    ]
)

@callback(
    dash.dependencies.Output('goals-graph', 'figure'),
    [dash.dependencies.Input('mode-radio', 'value')]
)
def update_goals_graph(mode):
    ages = data['Age']
    goals = data['Total goals']
    goals_per_game = data['Goals per game']
    if mode == 'Goals per game':
        fig = go.Figure(data=[go.Bar(x=ages, y=goals_per_game, hovertemplate='Age: %{x} years<br>Goals per game: %{y} <extra></extra>')])
        fig.update_layout(title='Goals ratio ', xaxis_title='Age', template='custom_ronaldo',
                          annotations=[dict(text="Number of goals per match", x=18, y=1.8, showarrow=False, font=dict(size=16))])
        return fig
    else:
        fig = go.Figure(data=[go.Bar(x=ages, y=goals, hovertemplate='Age: %{x} years<br>Goals: %{y} <extra></extra>')])
        fig.update_layout(title='Goals scored by Ronaldo over his career', xaxis_title='Age', template='custom_ronaldo',
                          annotations=[dict(text="Number of goals", x=18, y=65, showarrow=False, font=dict(size=16))])
        return fig
