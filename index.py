import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table
from app import app
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html
from pages import matches, players


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H3("T20-CUP-2022", className="text-center navbar_header"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("MATCHES-STATS", href="/matches", active="exact"),
                html.Hr(),
                dbc.NavLink("PLAYER-STATS", href="/players", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div(id='page-content')
])



@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/players':
        return players.layout
    else:
        return matches.layout 



if __name__ == '__main__':
    app.run_server(debug=True)       