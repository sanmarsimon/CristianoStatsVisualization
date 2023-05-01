import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from get_opponents_data import get_opponents

dash.register_page(__name__, name='Opponents',order=4)

team_stats = get_opponents()

# Define the data
teams = team_stats['Adversaire']
goals = team_stats['Buts']
assists = team_stats['PD']
matches = team_stats['Matches']

# Create the figure and the bar chart
fig = go.Figure(data=[
    go.Bar(name='Goals', x=teams, y=goals, hovertemplate='Team: %{x} <br>Goals: %{y} <extra></extra>'),
    go.Bar(name='Assists', x=teams, y=assists, hovertemplate='Team: %{x} <br>Assists: %{y} <extra></extra>'),
    go.Bar(name='Matches', x=teams, y=matches, hovertemplate='Team: %{x} <br>Number of Matches: %{y} <extra></extra>')
])


# Set the layout of the chart
fig.update_layout(
    title='Cristiano Ronaldo goals, and assists against 10 teams he faced the most during his career',
    xaxis_title='Opponent Teams',
    barmode='group',
    template='custom_ronaldo'
)

# Define the layout of the app
layout = html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Opponents", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=fig)
                    ],width=12
                )
            ]
        )
])
