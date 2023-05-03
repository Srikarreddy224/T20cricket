import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html
from app import app
import dash


t20Data = pd.read_csv(r"D:\Srikar\finalSummary.csv")

totalMatches = t20Data['id'].nunique()

firstInnTotal = t20Data['first_inn_score'].sum()
secondInnTotal = t20Data['second_inn_score'].sum()
totalRuns = firstInnTotal + secondInnTotal


H_Boundaries = t20Data['home_boundaries'].sum()
A_Boundaries = t20Data['away_boundaries'].sum()
HA_Boundaries = int(H_Boundaries + A_Boundaries)

H_wickets = int(t20Data['home_wickets'].sum())
A_wickets = int(t20Data['away_wickets'].sum())
totalWickets = H_wickets + A_wickets

home_team_avg_score = t20Data.groupby('home_team')['first_inn_score'].mean()
away_team_avg_score = t20Data.groupby('away_team')['first_inn_score'].mean()
avgMatchScore = int((home_team_avg_score + away_team_avg_score).mean())




wins_df = t20Data.groupby('winner')['id'].nunique().reset_index().rename(columns={'id': 'wins'})
wins_df = wins_df.sort_values('wins', ascending=False)

winsFig = px.bar(wins_df, x='winner', y='wins', title='Number of Wins by Team')
avgFirstInnScore = int(t20Data['first_inn_score'].mean()) 
avgSecondInnScore = int(t20Data['second_inn_score'].mean())



grouped = t20Data.groupby(['venue_name', 'winner']).size().reset_index(name='wins')

pivot = grouped.pivot(index='venue_name', columns='winner', values='wins')

heatmap = go.Heatmap(
    x=pivot.columns,
    y=pivot.index,
    z=pivot.values,
    colorscale='Viridis',
    zmin=0,
    zmax=pivot.values.max()
)

heatmapL = go.Layout(
    title='Number of wins by team at each venue',
    xaxis=dict(title='Team'),
    yaxis=dict(title='Venue')
)

fig = go.Figure(data=[heatmap], layout=heatmapL)


team_options = [{'label': team, 'value': team} for team in t20Data['home_team'].unique()]


container1 = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([    
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Number of Matches Played", className="firstHeader card-title text-center"),
                        html.H2(f'{totalMatches}', className="text-center"),
                    ]),
                ]),
            ], width=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Runs Scored", className="firstHeader card-title text-center"),
                        html.H2(f'{totalRuns}', className="text-center"),
                    ]),
                ]),
            ], width=3),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Wickets Taken", className="firstHeader card-title text-center"),
                        html.H2(f'{totalWickets}', className="text-center"),
                    ]),
                ]),
            ], width=3),   

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Boundaries", className="firstHeader card-title text-center"),
                        html.H2(f'{HA_Boundaries}', className="text-center"),
                    ]),
                ]),
            ], width=3),
        ]),

    html.Div([
        html.H4('Matches won by each team', className="text-center"),
        dcc.Graph(figure=winsFig)
    ])

    ], className="firstContainer")
])



secondContainer = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5('Average Match score', className="text-center"),
                        html.H2(f'{avgMatchScore}', className="text-center"),
                        html.Hr(),
                        html.H5('Average 1st Inn Score',className="text-center"),
                        html.H2(f'{avgFirstInnScore}', className="text-center"),
                        html.Hr(),
                        html.H5('Average 2nd Inn Score',className="text-center"),
                        html.H2(f'{avgSecondInnScore}', className="text-center"),
                    ])
                ])
            ], width=4),
            dbc.Col([

                dcc.Graph(figure=fig)

              ], width=8)
        ])
    ])
], className="secondContainer")


thirdContainer = html.Div([
    dbc.Container([
         dcc.Dropdown(
        id='team-dropdown',
        options=team_options,
        value=team_options[0]['value']
    ),
    dash_table.DataTable(
        id='team-score-table',
        columns=[
            {'name': 'Match', 'id': 'short_name'},
            {'name': 'Home Team', 'id': 'home_team'},
            {'name': 'Away Team', 'id': 'away_team'},
            {'name': 'Winner', 'id': 'winner'},
            {'name': 'First Inn Score', 'id': 'first_inn_score'},
            {'name': 'Second Inn Score', 'id': 'second_inn_score'}
        ]
    )
    ])
], className="thirdContainer")



fourthContaier = html.Div([
    html.Div([
    dcc.Graph(
        id='bubble-chart',
        figure={
            'data': [{
                'x': t20Data['first_inn_score'],
                'y': t20Data['second_inn_score'],
                'mode': 'markers',
                'marker': {
                    'size': t20Data['home_boundaries'] + t20Data['away_boundaries'],
                    'color': t20Data['home_team'],
                    'opacity': 0.7,
                    'colorscale': 'Viridis'
                },
                'text': t20Data['home_team'] + ' vs ' + t20Data['away_team']
            }],
            'layout': {
                'title': 'Bubble Chart: Innings Scores',
                'xaxis': {'title': 'First Inning Score'},
                'yaxis': {'title': 'Second Inning Score'}
            }
        }
    )
])
], className="fourthContaier")




@app.callback(
    dash.dependencies.Output('team-score-table', 'data'),
    [dash.dependencies.Input('team-dropdown', 'value')])
def update_output(selected_team):
    filtered_df = t20Data[(t20Data['home_team'] == selected_team) | (t20Data['away_team'] == selected_team)]
    return filtered_df.to_dict('records')


layout = [
    container1,
    secondContainer,
    thirdContainer,
    fourthContaier
]

