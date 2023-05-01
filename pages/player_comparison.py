import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from get_players_data import get_players_statistics

dash.register_page(__name__, name='Player comparison',order=8)

players = get_players_statistics()

# Create traces for each player
traces = []
for player in players:
    for i, year_data in enumerate(player['values']):
        name = f"{player['name']} ({year_data['year']})"
        trace = go.Scatterpolar(
            r=year_data['data'],
            theta=['Goals per 90 min', 'Assists per 90 min', 'Shot creation per 90 min','Pass completion per 90 min', 'Shots on target', 'Goals per 90 min',],
            name=name,
            meta=[name],
            visible=(i==0), # Show only the first year by default
            hovertemplate='<b>%{meta}</b><br>%{theta}: %{r:.2f} <extra></extra>'
        )
        traces.append(trace)

# Create figure
fig = go.Figure(data=traces)

# Format the figure
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1],
            showticklabels=False
        )
    ),
    showlegend=True,
    height=700,
    title='Performance comparison of players through their 5 last years in the European scene with Cristiano Ronaldo ', 
    template='custom_ronaldo'
)

# Create a slider to change the year
years = [1, 2, 3, 4, 5]
steps = []

for year in years:
    visible = [trace.name.endswith(f'({year})') for trace in traces]
    year_label = 'Year ' + str(year)
    if (year == 1):
        year_label += ' (oldest)'
    if (year == 5):
        year_label += ' (latest)'
    step = dict(
        method="update",
        args=[{"visible": visible}],
        label=year_label
    )
    steps.append(step)

sliders = [dict(
    active=0,
    pad={"t": 50},
    steps=steps,
    name="Year"
)]

fig.update_layout(sliders=sliders)


# Show the figure
# Define the layout of the app
layout = html.Div([
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div("Performance comparison", style={'fontSize': 24, 'color': '#ffffff'})
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
