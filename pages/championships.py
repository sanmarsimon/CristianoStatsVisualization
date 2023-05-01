import dash
from dash import dcc, html, callback, Input, Output, ctx
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from get_goals_data import get_goals_visualization, get_goals_by_team_category

dash.register_page(__name__, name='Championships', order=3)

df1 = get_goals_visualization()
df2 = get_goals_by_team_category()

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Championships", style={'fontSize': 24, 'color': '#ffffff'})
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='bar-chart',
                                  figure=go.Figure(data=[go.Bar(x=df1['Comp_Category'], y=df1['Goals'], text=df1['Goals'],
                                                                textposition='auto',
                                                                hovertemplate="<b>Teams: </b>%{customdata}<br><extra></extra>",
                                                                customdata=df1['Teams'].tolist())],
                                                   layout=go.Layout(title='Goals by Competition Category',
                                                                    template="custom_ronaldo")))
                    ], width=12
                ),
            ]
        ),
        
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Competition Category", id="comp-btn", color='info',className="me-md-2"),
                        dbc.Button("Team Category", id="team-btn", color='primary')
                    ],width=12, className="d-grid gap-2 d-md-flex justify-content-md-center mt-2"
                )
            ]
        )
    ]
)

@callback(
    [Output("bar-chart", "figure"),
     Output("comp-btn", "color"),
     Output("team-btn", "color")],
    Input("comp-btn", "n_clicks"),
    Input("team-btn", "n_clicks"),
    prevent_initial_call=True,
)
def switch_figure(_, __):
    button_clicked = ctx.triggered_id
    if button_clicked == 'comp-btn':
        return (go.Figure(data=[go.Bar(x=df1['Comp_Category'], y=df1['Goals'], text=df1['Goals'],
                                                                textposition='auto',
                                                                hovertemplate="Teams: %{customdata}<br>",
                                                                customdata=df1['Teams'].tolist())],
                                                   layout=go.Layout(title='Goals by Competition Category',
                                                                    template="custom_ronaldo")), 'info', 'primary')
    elif button_clicked == 'team-btn':
        return (go.Figure(data=[go.Bar(x=df2['Team_Category'], y=df2['Goals'], text=df2['Goals'],
                                                                textposition='auto', hoverinfo='skip')],
                                                   layout=go.Layout(title='Goals by Team Category',
                                                                    template="custom_ronaldo")), 'primary', 'info')
