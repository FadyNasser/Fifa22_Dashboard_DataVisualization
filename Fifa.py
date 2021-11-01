########################################################################################################################
# Library Import:
##################
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

########################################################################################################################
################################################## Date PreProcessing ##################################################
########################################################################################################################
# Teams Data:
#################
Team_data = pd.read_csv("data/teams_fifa22.csv", low_memory=False)
Team_data = Team_data.replace(to_replace='[ (0-9*)]', value='', regex=True)
Team_data = Team_data.replace(to_replace='[\xa0]', value='', regex=True)
Columns = ['Name', 'League', 'Overall', 'Attack', 'Midfield', 'Defence', 'Players', 'AllTeamAverageAge']
Team_df = Team_data.copy()[Columns]

Leagues = []
for i in Team_df['League'].unique():
    Leagues.append({"label": i, "value": i})

Teams = []
for i in Team_df.index:
    Teams.append({"label": Team_df["Name"][i], "value": Team_df["Name"][i]})

# Players Data:
#################
player_data = pd.read_csv("data/players_fifa22.csv", low_memory=False)
player_df = player_data.copy()

player_data2 = pd.read_csv("data/players_22.csv", low_memory=False)
player_df2 = player_data2.copy()

options = [
    {"label": "Overall", "value": "overall"},
    {"label": "Potential", "value": "potential"},
    {"label": "Value", "value": "value_eur"},
    {"label": "Wage", "value": "wage_eur"},
    {"label": "Height", "value": "height_cm"},
    {"label": "Weight", "value": "weight_kg"},
    {"label": "Pace", "value": "pace"},
    {"label": "Shooting", "value": "shooting"},
    {"label": "Passing", "value": "passing"},
    {"label": "Dribbling", "value": "dribbling"},
    {"label": "Defending", "value": "defending"},
    {"label": "Physic", "value": "physic"},
]

########################################################################################################################
####################################################### Dash App #######################################################
########################################################################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

########################################################################################################################
# Launch Server:
#################
server = app.server

########################################################################################################################
# Team Tab Content:
###################
Team1 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label("Choose A Team:"),
                html.Br(),
                dcc.Dropdown(
                    id="team1",
                    options=Teams,
                    value="Arsenal",
                    clearable=False
                ),
            ]
        ),
    ],
    body=True,
    className="controls_players",
)

Team2 = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Label("Choose A Team:"),
                html.Br(),
                dcc.Dropdown(
                    id="team2",
                    options=Teams,
                    value="Arsenal",
                    clearable=False
                ),
            ]
        ),
    ],
    body=True,
    className="controls_players",
)

teamTab_content = (
    html.Div(
        [
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H1("Team Comparison", style={'textAlign': 'center'}),
                        html.Hr(),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(Team1),
                                        html.Div("Overall Rating", className="card-title1",
                                                 style={'textAlign': 'center'}),
                                        dcc.Graph(id="Overall_1"),
                                    ],
                                    sm=3,
                                ),
                                dbc.Col(
                                    dcc.Graph(id="Teams_graph"), sm=5, align="center"
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(Team2),
                                        html.Div("Overall Rating", className="card-title1",
                                                 style={'textAlign': 'center'}),
                                        dcc.Graph(id="Overall_2"),
                                    ],
                                    sm=3,
                                ),
                            ],
                            justify="between",
                        ),

                    ]
                )
            )
        ]
    ),
)

#########################################################################################################################
# League Tab Content :
######################
age_slider = dcc.RangeSlider(
    id="age_slider",
    min=player_df["Age"].min(),
    max=player_df["Age"].max(),
    value=[player_df["Age"].min(), player_df["Age"].max()],
    step=1,
    marks={
        16: "16",
        20: "20",
        24: "24",
        28: "28",
        32: "32",
        36: "36",
        40: "40",
        44: "44",
        48: "48",
        52: "52",
    },
)

chosen_league = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.Br(),
                dcc.Dropdown(
                    id="choose league",
                    options=Leagues,
                    value="English Premier League",
                    clearable=False
                ),
            ]
        ),
    ],
    body=True,
    className="controls_league",
)

league_value = [
    dbc.CardHeader("Total League Value"),
    dbc.CardBody(
        [
            html.P("This is some card content that we'll reuse", id='league_value',
                   style={'textAlign': 'center', 'font-family': 'cursive', 'font-size': '32px', 'font-Color': 'blue'}),
        ],
    ),
]

num_players = [
    dbc.CardHeader("Number of Players"),
    dbc.CardBody(
        [
            html.P("This is some card content that we'll reuse", id='num_players',
                   style={'textAlign': 'center', 'font-family': 'cursive', 'font-size': '32px',
                          'font-Color': 'green.'}),
        ],
    ),
]

num_clubs = [
    dbc.CardHeader("Number of Teams"),
    dbc.CardBody(
        [
            html.P("This is some card content that we'll reuse", id='num_teams',
                   style={'textAlign': 'center', 'font-family': 'cursive', 'font-size': '32px', 'font-Color': 'Red'}),
        ],
    ),
]

league_bans = dbc.Row(
    [
        dbc.FormGroup(
            [dbc.Card(league_value, color="primary", outline=True)]
        ),

        dbc.FormGroup(
            [dbc.Card(num_players, color="secondary", outline=True)]
        ),

        dbc.FormGroup(
            [dbc.Card(num_clubs, color="info", outline=True)]
        ),

    ],

    justify="around"
)

metric1_dropdown = dcc.Dropdown(id="drop1", options=options, value="overall")
metric2_dropdown = dcc.Dropdown(id="drop2", options=options, value="potential")
# metric3_dropdown = dcc.Dropdown(id="drop3", options=options, value="value_eur")

controls = dbc.Card(
    [
        chosen_league,
        dbc.FormGroup(
            [html.Label("Choose an Attribute:"), html.Br(), metric1_dropdown]
        ),
        dbc.FormGroup(
            [html.Label("Choose an Attribute:"), html.Br(), metric2_dropdown]
        ),
        # dbc.FormGroup(
        #     [html.Label("Choose an Attribute:"), html.Br(), metric3_dropdown]
        # ),
    ],
    body=True,
    className="controls",
)

main33 = dbc.Card([league_bans,
                   html.Br(),
                   dbc.Row(
                       [dbc.Col(
                           dcc.Graph(
                               id="league-graph1", className="LeagueBarPlot"
                           ),
                           sm=5,
                       ),
                           dbc.Col(
                               dcc.Graph(
                                   id="league-graph2", className="LeagueBarPlot"
                               ),
                               sm=5,
                           ),
                           # dbc.Col(
                           #     dcc.Graph(
                           #         id="league-graph3", className="LeagueBarPlot"
                           #     ),
                           #     sm=3,
                           # ),
                       ],
                       justify="center"
                   )
                   ],

                  )

leagueTab_content = html.Div(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H1("League Analysis"),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(controls, sm=3),
                            dbc.Col(main33),
                        ],
                    ),
                    dbc.Row(
                        [
                            dbc.Label(
                                "Select Age:",
                                style={"margin-left": "5%", "font-size": "20px"},
                            ),
                            dbc.Col(age_slider, align='center'),
                        ]
                    ),
                ]
            ),

        )

    ]
)

########################################################################################################################
##################################################### Layout Setup #####################################################
########################################################################################################################
app.layout = dbc.Container(
    [
        # html.H1("Fifa Players Analysis", style={'textAlign': 'center'}),
        html.H1(
            html.Img(src=app.get_asset_url("logo_white3.png"), height="130px"), style={'textAlign': 'center'}
        ),
        dbc.Navbar(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("FIFA 22 Dashboard", id="label1"),
                                    html.Br(),
                                    html.Label(
                                        "Explore Fifa 22 Teams and Players",
                                        className="label2",
                                    ),
                                    html.Br(),
                                    html.Label(
                                        "Dashboard created by: Fady Nasser & Basem Mahmoud",
                                        className="label2",
                                        style={"margin-bottom": ".34rem"},
                                    ),
                                ],
                            ),
                        ],
                        align="between",
                        no_gutters=True,
                    ),
                ),
            ],
        ),
        dbc.Tabs(
            [
                dbc.Tab(teamTab_content, label="Teams Analysis"),
                # dbc.Tab(teamTab_content, label="Teams Analysis"),
                dbc.Tab(leagueTab_content, label="Leagues Analysis"),
            ],
        ),
    ],
    fluid=True,
)


########################################################################################################################
############################################### Callbacks And Functions ################################################
########################################################################################################################

########################################################################################################################
# Team Tab Callback:
####################
@app.callback(
    Output("Teams_graph", "figure"),
    Output("Overall_1", "figure"),
    Output("Overall_2", "figure"),
    Input("team1", "value"), Input("team2", "value")
)
########################################################################################################################
# Team Tab Function:
####################
def teamTab_function(team1, team2):
    Skills = ['Attack', 'Midfield', 'Defence']
    df1_for_plot = pd.DataFrame(Team_df[Team_df["Name"] == team1][Skills].iloc[0])
    df1_for_plot.columns = ["score"]
    df2_for_plot = pd.DataFrame(Team_df[Team_df["Name"] == team2][Skills].iloc[0])
    df2_for_plot.columns = ["score"]

    list_scores = [
        df1_for_plot.index[i].capitalize() + " = " + str(df1_for_plot["score"][i])
        for i in range(len(df1_for_plot))
    ]
    text_scores_1 = team1
    for i in list_scores:
        text_scores_1 += "<br>" + i

    list_scores = [
        df2_for_plot.index[i].capitalize() + " = " + str(df2_for_plot["score"][i])
        for i in range(len(df2_for_plot))
    ]
    text_scores_2 = team2
    for i in list_scores:
        text_scores_2 += "<br>" + i

    fig = go.Figure(
        data=go.Scatterpolar(
            r=df1_for_plot["score"],
            theta=df1_for_plot.index,
            fill="toself",
            marker_color="rgb(45,0,198)",
            opacity=1,
            hoverinfo="text",
            name=text_scores_1,
            text=[
                df1_for_plot.index[i] + " = " + str(df1_for_plot["score"][i])
                for i in range(len(df1_for_plot))
            ],
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=df2_for_plot["score"],
            theta=df2_for_plot.index,
            fill="toself",
            marker_color="rgb(255,171,0)",
            hoverinfo="text",
            name=text_scores_2,
            text=[
                df2_for_plot.index[i] + " = " + str(df2_for_plot["score"][i])
                for i in range(len(df2_for_plot))
            ],
        )
    )

    fig.update_layout(
        polar=dict(
            hole=0.1,
            bgcolor="white",
            radialaxis=dict(
                visible=True,
                type="linear",
                autotypenumbers="strict",
                autorange=False,
                range=[30, 100],
                angle=90,
                showline=False,
                showticklabels=False,
                ticks="",
                gridcolor="black",
            ),
        ),
        width=550,
        height=550,
        margin=dict(l=80, r=80, t=20, b=20),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )

    # gauge plot 1
    df1_for_plot = pd.DataFrame(Team_df[Team_df["Name"] == team1]["Overall"])
    df1_for_plot["name"] = team1
    gauge1 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df1_for_plot.Overall.iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "#5000bf"}},
        )
    )
    gauge1.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )

    # gauge plot 2
    df2_for_plot = pd.DataFrame(Team_df[Team_df["Name"] == team2]["Overall"])
    df2_for_plot["name"] = team2
    gauge2 = go.Figure(
        go.Indicator(
            domain={"x": [0, 1], "y": [0, 1]},
            value=df2_for_plot.Overall.iloc[0],
            mode="gauge+number",
            gauge={"axis": {"range": [None, 100]}, "bar": {"color": "rgb(255,171,0)"}},
        )
    )
    gauge2.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font_color="black",
        font_size=15,
    )

    return fig, gauge1, gauge2


########################################################################################################################
# League Tab Callback:
######################
@app.callback(
    [
        Output(component_id="league_value", component_property="children"),
        Output(component_id="num_players", component_property="children"),
        Output(component_id="num_teams", component_property="children"),
        Output(component_id="league-graph1", component_property="figure"),
        Output(component_id="league-graph2", component_property="figure"),
        # Output(component_id="league-graph3", component_property="figure"),
    ],
    [
        Input(component_id="drop1", component_property="value"),
        Input(component_id="drop2", component_property="value"),
        # Input(component_id="drop3", component_property="value"),
        Input(component_id="choose league", component_property="value"),
        Input(component_id="age_slider", component_property="value"),
    ],
)
########################################################################################################################
# League Tab Function:
######################
def league_tab_function(input_value1, input_value2, selection, age):
    league_value = Team_data[Team_data['League'] == selection]['TransferBudget'].sum()
    players = Team_data[Team_data['League'] == selection]['Players'].sum()
    teams = Team_data[Team_data['League'] == selection]['League'].count()

    filtered_by_age_data = player_df2[(player_df2["age"] >= age[0]) & (player_df2["age"] <= age[1])]

    data_bar1 = dict(
        type="bar",
        y=filtered_by_age_data.groupby("league_name")
            .median()[input_value1]
            .sort_values(ascending=False)
            .head(5),
        x=filtered_by_age_data["league_name"].unique(),
    )

    data_bar2 = dict(
        type="bar",
        y=filtered_by_age_data.groupby("league_name")
            .median()[input_value2]
            .sort_values(ascending=False)
            .head(5),
        x=filtered_by_age_data["league_name"].unique(),
    )

    # data_bar3 = (
    #     dict(
    #         type="bar",
    #         y=filtered_by_age_data.groupby("league_name")
    #             .median()[input_value3]
    #             .sort_values(ascending=False)
    #             .head(5),
    #         x=filtered_by_age_data["league_name"].unique(),
    #     ),
    # )

    layout_bar1 = dict(xaxis=dict(title="League", tickangle=45), )
    layout_bar2 = dict(xaxis=dict(title="League", tickangle=45), )
    # layout_bar3 = dict(xaxis=dict(title="League", tickangle=45), )

    fig1 = go.Figure(data=data_bar1, layout=layout_bar1)
    fig1.update_traces(
        marker_color="rgb(133,61,246)",
        marker_line_color="rgb(133,61,246)",
        marker_line_width=0.8,
        opacity=0.9,
    )
    fig1.update_layout(
        title_text=input_value1.capitalize(),
        title_x=0.5,
        margin=dict(l=70, r=40, t=60, b=40),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(gridcolor="#e5e6dc", gridwidth=0.5),
        yaxis=dict(
            tickcolor="#e5e6dc", tickwidth=5, gridcolor="#e5e6dc", gridwidth=0.5
        ),
    )

    fig2 = go.Figure(data=data_bar2, layout=layout_bar2)
    fig2.update_traces(
        marker_color="rgb(158,50,249)",
        marker_line_color="rgb(133,61,246)",
        marker_line_width=0.8,
        opacity=0.9,
    )
    fig2.update_layout(
        title_text=input_value2.capitalize(),
        title_x=0.5,
        margin=dict(l=70, r=40, t=60, b=40),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(gridcolor="#e5e6dc", gridwidth=0.5),
        yaxis=dict(
            tickcolor="#e5e6dc", tickwidth=5, gridcolor="#e5e6dc", gridwidth=0.5
        ),
    )
    # fig3 = go.Figure(data=data_bar3, layout=layout_bar3)
    # fig3.update_traces(
    #     marker_color="rgb(189,34,250)",
    #     marker_line_color="rgb(133,61,246)",
    #     marker_line_width=0.8,
    #     opacity=0.9,
    # )
    # fig3.update_layout(
    #     title_text=input_value3.capitalize(),
    #     title_x=0.5,
    #     margin=dict(l=70, r=40, t=60, b=40),
    #     plot_bgcolor="rgba(0, 0, 0, 0)",
    #     paper_bgcolor="rgba(0, 0, 0, 0)",
    #     xaxis=dict(gridcolor="#e5e6dc", gridwidth=0.5),
    #     yaxis=dict(
    #         tickcolor="#e5e6dc", tickwidth=5, gridcolor="#e5e6dc", gridwidth=0.5
    #     ),
    # )
    return str(league_value), str(players), str(teams), fig1, fig2


########################################################################################################################
################################################### Main Server Run ####################################################
########################################################################################################################
if __name__ == "__main__":
    app.run_server(debug=True)
