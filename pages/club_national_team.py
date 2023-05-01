import dash
from dash import dcc,html, Input, Output, State, callback, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
from get_ranking_trophies_data import get_ranking_data, get_trophies_data
from hover_template import get_hover_template

dash.register_page(__name__, name='Clubs Ranking/Trophies',order=5)

ranking_df = get_ranking_data()
trophies_df = get_trophies_data()
teams_name = ranking_df.columns[:-1]
figure=px.line(ranking_df, x=ranking_df.index, y=ranking_df.columns[:-1], title="Club Ranking per Season", custom_data=['Team'], markers=True, template="custom_ronaldo")
figure.update_traces(hovertemplate=get_hover_template('ranking-btn'), line=dict(width=3))
figure.update_yaxes(title_text='', showticklabels=True)
figure.update_layout(xaxis=dict(title='Season'), annotations=[dict(text="Rank",x=-0.75,y=6.5,showarrow=False,font=dict(size=16))])

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Clubs Ranking/Trophies", style={'fontSize': 24, 'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id='line-fig',
                            figure=figure,
                        )
                    ],width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Button("Club Ranking", id="ranking-btn", color='info', className="me-md-2"),
                        dbc.Button("Club Trophies", id="trophies-btn", color='primary'),
                    ],width=12, className="d-grid gap-2 d-md-flex justify-content-md-center mt-2 "
                )
            ]
        )
        
    ]
)

@callback(
    [Output("line-fig", "figure"),
     Output("ranking-btn", "color"),
     Output("trophies-btn", "color")],
    [Input("ranking-btn", "n_clicks"),
    Input("trophies-btn", "n_clicks")],
    prevent_initial_call=True,
)
def switch_figure(_, __):
    button_clicked = ctx.triggered_id
    if button_clicked == 'ranking-btn':
        figure = px.line(ranking_df, x=ranking_df.index, y=ranking_df.columns[:-1], title="Club Ranking per Season",custom_data=['Team'], markers=True, template="custom_ronaldo")
        figure.update_traces(hovertemplate=get_hover_template('ranking-btn'), line=dict(width=3))
        figure.update_yaxes(title_text='', showticklabels=True)
        figure.update_layout(xaxis=dict(title='Season'),annotations=[dict(text="Rank", x=-0.75, y=6.5, showarrow=False, font=dict(size=16))])
        return (figure, 'info', 'primary')
    elif button_clicked == 'trophies-btn':
        figure = px.bar(trophies_df, x='Saison', y='Comp_count', title="Number of Trophies Won per Season", custom_data=['Comp', 'Équipe'], color='Équipe', template="custom_ronaldo")
        figure.update_traces(hovertemplate=get_hover_template('trophies-btn'))
        figure.update_yaxes(title_text='', showticklabels=True)
        figure.update_layout(xaxis=dict(title='Season'),annotations=[dict(text="Number of trophies", x=0, y=3.2, showarrow=False, font=dict(size=16))])
        return (figure, 'primary', 'info')
