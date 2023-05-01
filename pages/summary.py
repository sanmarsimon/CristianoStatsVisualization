import dash
from dash import dcc,html
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Home', path='/',order=1)

table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Samia"), html.Td("Safaa")])
row2 = html.Tr([html.Td("Abderrahmane"), html.Td("Grou")])
row3 = html.Tr([html.Td("Ayman"), html.Td("Atmani")])
row4 = html.Tr([html.Td("Sanmar"), html.Td("Simon")])
row5 = html.Tr([html.Td("Hugo"), html.Td("Juillet")])

table_body = [html.Tbody([row1, row2, row3, row4, row5])]

table = dbc.Table(
    # using the same table as in the above example
    table_header + table_body,
    bordered=True,
    dark=True,
    hover=True,
    responsive=True,
    striped=True,
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Home", style={'color': '#ffffff'})
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P("As part of our project to analyze Ronaldo's impact on the sport, we are using data visualization to explore some of the key moments and achievements of his career. By graphically representing Ronaldo's goals, assists, and other statistics, we are able to better understand his style of play, his strengths and weaknesses, and the impact he has had on his teams and on the sport as a whole.", style={'color': '#ffffff'}),
                        html.H2("Team 3 - SportsAI", style={'fontSize': 20, 'color': '#ffffff'}),
                        table
                    ], className='p-3',xs=10, sm=10, md=8, lg=6, xl=6, xxl=6
                ),
                dbc.Col(
                    [
                        html.Img(src='./assets/cristiano_pic.png', height='700')
                    ],xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
            ]
        )
        
    ]
)