import pandas as pd
import dash
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table
from dash import dcc
from app import app
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import html


battingData = pd.read_csv("../newBatData.csv")
bowlingData = pd.read_csv("../newBowlData.csv")

grouped_data = battingData.groupby(['fullName', 'current_innings']).agg({'runs': 'sum', 'ballsFaced': 'sum'}).reset_index()
dropdown_options = [{'label': team, 'value': team} for team in sorted(grouped_data['current_innings'].unique())]
def get_top_5_batsman(data, team):
    filtered_data = data[data['current_innings'] == team].sort_values(by='runs', ascending=False).head(5)
    return filtered_data


bowlGroupedData = bowlingData.groupby(['fullName','bowling_team']).agg({'wickets':'sum','overs':'sum'}).reset_index()
dropdown_optionsBowl = [{'label': team, 'value': team} for team in sorted(bowlGroupedData['bowling_team'].unique())]
def get_top_5_bowlers(data, team):
    filtered_data = data[data['bowling_team'] == team].sort_values(by='wickets', ascending=False).head(5)
    return filtered_data

# dropdown_optionsPie = [{'label': bowler, 'value': bowler} for bowler in sorted(bowlingData['fullName'].unique())]






container1 = html.Div([
                    dbc.Container([
                        dcc.Dropdown(
                        id='team-dropdown',
                        options=dropdown_options,
                        value=dropdown_options[0]['value']
                    ),
                    html.Hr(),
                        dbc.Row([
                            dbc.Col([html.Div([
                    dcc.Graph(id='bat-chart')
                ])], width=6),
            dbc.Col([

                html.Div([
                    dcc.Graph(id='top-5-bowlers-graph')

            ])
            ], width=6)
        ])
    ])
], className="firstContainer")


secondContainer = html.Div([
    dbc.Container([
       html.Div([
        dbc.Row([
            dbc.Col([                
    html.H4("Batsman Fours and Sixes Percentage"),
    dcc.Dropdown(
        id='batsman-dropdown',
        options=[{'label': name, 'value': name} for name in battingData['fullName'].unique()],
        value=battingData['fullName'].unique()[0]
    ),
    dcc.Graph(id='pie-chart')
            ], width=6),
            dbc.Col([
                html.H4("Bowlers Extras vs Dot Ball Percentage"),
    dcc.Dropdown(
        id='bowler-dropdown',
        options=[{'label': name, 'value': name} for name in bowlingData['fullName'].unique()],
        value=bowlingData['fullName'].unique()[0]
    ),
    dcc.Graph(id='Bowlerspie-chart')
], width=6)

        ]),

]) 
    ]),
], className="secondContainer")


thirdContainer = html.Div([
    dbc.Container([
        html.Div([
    html.H1('Top 10 Players Performance at Different Venues'),
    dcc.Dropdown(
        id='venue-dropdown',
        options=[{'label': v, 'value': v} for v in battingData['venue'].unique()],
        value=battingData['venue'].unique()[0]
    ),
    dcc.Graph(id='heatmap')
])
    ])
], className="thirdContainer")




@app.callback(
    Output('bat-chart', 'figure'),
    Input('team-dropdown', 'value')
)
def update_bar_chart(selected_team):
    # filter the data by selected team and get top 5 players based on total runs
    filtered_data = get_top_5_batsman(grouped_data, selected_team)
    
    # create the bar chart with the top 5 players based on total runs
    batfig = px.bar(filtered_data, x='fullName', y='runs', color='ballsFaced', title=f'Top 5 Batsmen for {selected_team}')
    batfig.update_layout(xaxis_title='Player', yaxis_title='Total Runs', legend_title='Total Balls Faced')
    
    return batfig




#bowling graph
@app.callback(
    Output('top-5-bowlers-graph', 'figure'),
    Input('team-dropdown', 'value')
)
def update_bar_chart(selected_team):
    # filter the data by selected team and get top 5 players based on total runs
    filtered_data = get_top_5_bowlers(bowlGroupedData, selected_team)
    
    # create the bar chart with the top 5 players based on total runs
    bowlfig = px.bar(filtered_data, x='fullName', y='wickets', color='overs', title=f'Top 5 Bowlers for {selected_team}')
    bowlfig.update_layout(xaxis_title='Player', yaxis_title='Total Wickets', legend_title='Total Wickets Taken')
    
    return bowlfig



#boundaries
@app.callback(Output('pie-chart', 'figure'),
              Input('batsman-dropdown', 'value'))
def update_pie_chart(selected_batsman):
    # Filter the data by the selected batsman
    batsman_data = battingData[battingData['fullName'] == selected_batsman]
    
    # Calculate the total number of fours and sixes
    total_fours = batsman_data['fours'].sum()
    total_sixes = batsman_data['sixes'].sum()
    
    # Calculate the percentage of fours and sixes
    fours_percentage = total_fours / (total_fours + total_sixes) * 100
    sixes_percentage = total_sixes / (total_fours + total_sixes) * 100
    
    # Create the pie chart
    data = {'Percentage': [fours_percentage, sixes_percentage],
            'Type': ['Fours', 'Sixes']}
    boundariesfig = px.pie(data, values='Percentage', names='Type', title=f"{selected_batsman}'s Fours and Sixes Percentage")
    
    return boundariesfig



@app.callback(
    Output(component_id='Bowlerspie-chart', component_property='figure'),
    Input(component_id='bowler-dropdown', component_property='value')
)
def update_pie_chart(selected_bowler):
    # Filter the data by selected bowler
    bowler_data = bowlingData[bowlingData['fullName'] == selected_bowler]

    # Calculate total wides and noballs and dots
    total_wides_noballs = bowler_data['wides'].sum() + bowler_data['noballs'].sum()
    total_dots = bowler_data['dots'].sum()

    # Calculate percentage of extras against dots
    pct_extras_vs_dots = total_wides_noballs / total_dots * 100

    # Create pie chart with percentages
    ballfig = px.pie(
        values=[pct_extras_vs_dots, 100 - pct_extras_vs_dots],
        names=['Extras (Wides/Noballs)', 'Dots'],
        title=f'Percentage of Extras Given by {selected_bowler}'
    )

    return ballfig





@app.callback(
    Output('heatmap', 'figure'),
    Input('venue-dropdown', 'value')
)
def update_heatmap(selected_venue):
    # Filter the data by selected venue and top 10 players
    venue_data = battingData[battingData['venue'] == selected_venue]
    top_players = venue_data.groupby('fullName')['runs'].sum().sort_values(ascending=False)[:10].index
    player_data = venue_data[venue_data['fullName'].isin(top_players)]
    
    # Create the heatmap
    heatmap_fig = px.density_heatmap(
        data_frame=player_data,
        x='fullName',
        y='venue',
        z='runs',
        color_continuous_scale='Viridis',
        nbinsx=len(top_players),
        nbinsy=len(battingData['venue'].unique())
    )
    
    # Set the axis labels
    heatmap_fig.update_xaxes(title='Batsman')
    heatmap_fig.update_yaxes(title='Venue')
    
    # Set the title
    heatmap_fig.update_layout(title=f'Top 10 Batsman Performance at {selected_venue}')
    
    return heatmap_fig


layout = [
    container1,
    secondContainer,
    thirdContainer
]
