import dash
from dash import dcc,html, Input, Output, callback, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
from get_goals_data import get_goals_by_minute, get_goals_by_type

dash.register_page(__name__, name='Goals',order=6)

goals_by_mins = get_goals_by_minute()
goals_by_types = get_goals_by_type()

fig=px.line(goals_by_mins, x=goals_by_mins.index, y='Date', title="Goals per minute",template="custom_ronaldo", labels={"Date":"Goals"})
fig.update_yaxes(title_text='', showticklabels=True)
fig.update_layout(annotations=[dict(text="Goals", x=2, y=19, showarrow=False, font=dict(size=16))])

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Goals", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='graph-fig',
                            figure=fig,
                            )
                    ],width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Goals Per Minute", id="minute-btn",color='info', className="me-md-2"),
                        dbc.Button("Goal Types", id="type-btn", color='primary'),
                    ],width=12, className="d-grid gap-2 d-md-flex justify-content-md-center mt-2 "
                )
            ]
        )
    ]
)

@callback(
    [Output("graph-fig", "figure"),
     Output("minute-btn", "color"),
     Output("type-btn", "color")],
    Input("minute-btn", "n_clicks"),
    Input("type-btn", "n_clicks"),
    prevent_initial_call=True,
)
def switch_figure(_, __):
    button_clicked = ctx.triggered_id
    if button_clicked == 'minute-btn':
        fig = px.line(goals_by_mins, x=goals_by_mins.index, y='Date', title="Goals per minute", labels={ "Date": "Goals" }, template="custom_ronaldo")
        fig.update_yaxes(title_text='', showticklabels=True)
        fig.update_layout(annotations=[dict(text="Goals", x=2, y=19, showarrow=False, font=dict(size=16))])
        return fig, 'info', 'primary'
    elif button_clicked == 'type-btn':
        fig = px.line(goals_by_types, x="Date", y="Count", color='Type', title='Type of goals per year',template="custom_ronaldo")
        fig.update_yaxes(title_text='', showticklabels=True)
        fig.update_layout(annotations=[dict(text="Total goals", x=1, y=28, showarrow=False, font=dict(size=16))])
        return fig, 'primary', 'info'