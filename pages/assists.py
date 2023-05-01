import dash
from dash import dcc, html
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from get_assists_data import get_top_assisting_players

dash.register_page(__name__, name='Assists', order=7)

df_assist = get_top_assisting_players()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Assists", style={'fontSize': 24, 'color': '#ffffff'})
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='assist-bar-chart',
                                  figure=go.Figure(data=[go.Bar(x=df_assist['Passe décisive'], y=df_assist['assists_count'], text=df_assist['assists_count'],
                                                                textposition='auto', hoverinfo='skip')],
                                                   layout=go.Layout(title='Top 10 players to assist Cristiano Ronaldo',
                                                                    template="custom_ronaldo")))
                    ], width=12
                )
            ]
        )
    ]
)
