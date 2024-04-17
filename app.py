# %%
# import libraries
from espn_api.basketball import League
import pandas as pd
import dash
from dash import dcc, html, dash_table, State
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from raceplotly.plots import barplot
import plotly.graph_objs as go

# Import functions from data folder
from data.espn_api_functions import *

# %%
# fill in your ESPN credentials
espn_s2 = f"AEBxlh0p0NHPbu6WIY0O0TNX6B7oQkhT1bCnR12c5SvsUf5Dnap49bkneUfyt9h1Y5m1MBalds2N47X5i%2FE6YhYUJDbxumf3HrW1iFK%2BPWOGnTpl%2F0wbLLy7C19hr50jNoma59zfYY5iOKxOvK6yT9cn689C4OoQ%2BTiVm%2FG7TjfaGLFIKIJ8OkuSJBye7xYCgnLh%2BvD5Fbbwgz8pLX6htmu%2BEyilZCOrqQ81zDXUrRQgWhIOOXEx1Uy5d1SOQOPkdfqV%2F6Nsr2jUTvgr2T%2FS9yxs"
swid = "{5C675DD8-073A-4E00-AD7A-B926A3F2800B}"
team_id = 2
league_id = 1267411756
year = 2024

# call functions
cleaned_df, team_name, team_logo = get_league_info(espn_s2, swid, team_id, league_id, year)
team_url = get_league_url(league_id, team_id, year)

# copy needed for other graphs to work
df = cleaned_df.copy()

# %%
# initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions = True, external_stylesheets=[dbc.themes.SANDSTONE])
server = app.server

# define app layout
app.layout = html.Div([
    dbc.Navbar(
        children=[
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=team_logo, height="50px", style={"border-radius": "50%"}), width="auto"),  # logo
                        dbc.Col(dbc.NavbarBrand(f"{team_name}'s Fantasy Basketball Dashboard", className="ms-2"), width="auto"),  # brand
                    ],
                    align="center",
                ),
                href=team_url, # set the url to the team's ESPN page
            ),
            dbc.Nav(
                [   # navbar items
                    dbc.NavItem(dbc.NavLink("About", href="/About")),
                    dbc.NavItem(dbc.NavLink("View Table", href="/Table")),
                    dbc.NavItem(dbc.NavLink("Bar Charts", href="/Home")),
                    dbc.NavItem(dbc.NavLink("Polar Chart", href="/Polar-Chart")), 
                ],
                navbar=True,
                className="ms-auto flex-nowrap mt-3 mt-md-0",  # adjusted class
            ),
            dbc.Button("Refresh Data", id="refresh-button", color="primary", className="ml-3"),  # moved to the right
        ],
        color="primary",
        dark=True
    ),
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content", children=[
        html.Label("Select Stats:"),
        dcc.Dropdown(
        id="stat-dropdown",
        options=[ # add options for different stats
            {"label": "Fantasy Points", "value": "Fantasy Points"},
            {"label": "Points (PTS)", "value": "PTS"},
            {"label": "Assists (AST)", "value": "AST"},
            {"label": "Rebounds (REB)", "value": "REB"},
            {"label": "Blocks (BLK)", "value": "BLK"},
            {"label": "Steals (STL)", "value": "STL"},
            {"label": "3-Pointers Made (3PTM)", "value": "3PTM"},
            {"label": "Field Goals Made (FGM)", "value": "FGM"},
            {"label": "Free Throws Made (FTM)", "value": "FTM"}
        ],
        value="Fantasy Points"  # default value
    ),
    dcc.Graph(id="race-plot"),
    html.Hr(), 
    dcc.Graph(id="fantasy-points-bar-chart"),
        html.Label("Select Stats:"),
        dcc.Dropdown(
        id="bar-chart-dropdown",
        options=[ # add options for different stats
            {"label": "Fantasy Points", "value": "Fantasy Points"},
            {"label": "Points (PTS)", "value": "PTS"},
            {"label": "Assists (AST)", "value": "AST"},
            {"label": "Rebounds (REB)", "value": "REB"},
            {"label": "Blocks (BLK)", "value": "BLK"},
            {"label": "Steals (STL)", "value": "STL"},
            {"label": "3-Pointers Made (3PTM)", "value": "3PTM"},
            {"label": "Field Goals Made (FGM)", "value": "FGM"},
            {"label": "Free Throws Made (FTM)", "value": "FTM"}
        ],
        value="Fantasy Points"  # default value
    ),
        html.Label("Select Weeks to Display:"),
        dcc.RangeSlider(
            id="week-slider",
            min=0,
            max=len(cleaned_df["Week"].unique()) - 1,
            marks={i: f"Week{week}" for i, week in enumerate(cleaned_df["Week"].unique())},
            value=[len(cleaned_df["Week"].unique()) - 5, len(cleaned_df["Week"].unique()) - 1],
            allowCross=False,  # prevent crossing over
            step=1,  # allow only integer steps
        ),
        dcc.Dropdown(
            id="player-dropdown",
            options=[{"label": player, "value": player} for player in cleaned_df["Player"].unique()],
            value=list(cleaned_df["Player"].unique()),  # select all players by default
            multi=True  # allow multiple selections
        ),
    ]),
    dbc.Modal(
        [
            dbc.ModalHeader("Data Refreshed"),
            dbc.ModalBody("The data has been successfully refreshed."),
            dbc.ModalFooter(),
        ],
        id="modal",
        centered=True,
    )
])

# define callback to update page content based on URL
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/Table":
        return generate_table_view()
    if pathname == "/About":
        return generate_about_view()
    if pathname == "/Polar-Chart":  
        return generate_polar_chart_view()
    else:
        return generate_home_view()


# function to generate about view
def generate_about_view():
    return html.Div([
        html.H1("About"),
        html.P([
            "Welcome to the Fantasy Basketball Dashboard! This dashboard provides insights and analysis for fantasy basketball enthusiasts. You can explore player statistics, track performance over time with interactive charts, and visualize fantasy point breakdowns. Navigate through different views using the navbar above to explore various features. This dashboard was created using Dash and hosted on Render, providing a user-friendly experience for analyzing a Fantasy Team's basketball data. The data visualized is from my ESPN Fantasy Basketball League from 2023-2024."
        ]),
        html.H2("Why this API was chosen"),
        html.P([
            "I wanted to use a dataset that updates weekly as the fantasy basketball season progresses. I decided to use the API to collect the data for the UVA Fantasy Basketball league I am in as I was curious to see how the players I drafted performed and wanted further details on how their stats on the court contributed to my team's fantasy performance."
        ]),
        html.H2("Data Provenance"),
        html.P([
            "This data was gathered through accessing ",
            html.A("ESPN", href="https://www.espn.com/"),
            " fantasy league information from the ",
            html.A("ESPN API", href="https://github.com/cwendt94/espn-api"),
            ". The API was created for users to gather personal insights into their fantasy leagues. The player stats and information themselves were gathered by ESPN who received this information from the ",
            html.A("NBA", href="https://www.nba.com/"),
            ".",
        ]),
        html.Br(),
        html.P("Check out the GitHub repository for more details"), # add a link to the GitHub repository
        html.A(
            html.Img(
                src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
                style={"width": "50px", "height": "auto"}
            ),
            href="https://github.com/kevindangkhoama/Fantasy-Basketball-Dashboard",
            target="_blank"
        ),
    ], style={"margin": "20px"})
    
# function to generate table view
def generate_table_view():
    return html.Div([
        html.H1(f"{team_name}'s Player Data Table"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in cleaned_df.columns], # Define columns
            page_size=20,
            data=cleaned_df.to_dict("records"), # Convert the DataFrame to a dictionary
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},  # apply style to odd rows
                    "backgroundColor": "rgb(240, 240, 240)"  # alternate row color
                }
            ],
        )
    ])

def generate_polar_chart_view():
    return html.Div([
        # player and UI components section
        html.Div([
            html.Img(id="player-image", style={"width": "100%", "height": "auto"}),
            html.Label("Select Player:"),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{"label": player, "value": player} for player in df["Player"].unique()], # add options for players
                value=df["Player"].iloc[9]
            ),
            html.Label("Select Weeks:"),
            dcc.Checklist(
                id="week-checklist",
                options=[{"label": week, "value": week} for week in df["Week"].unique()], # add options for weeks
                inline=True,
                value = list(df["Week"].unique()[:5]),
                className="form-check"
            ),
            html.Div([
                html.Button("Deselect ALL Weeks", id="deselect-all-button", n_clicks=0, className="btn btn-primary", style={'width': '65%', 'marginRight': '5px'}),
                html.Button("Select All Weeks", id="select-all-button", n_clicks=1, className="btn btn-primary", style={"width": "65%", "marginLeft": '5px'}),
            ], style={'display': 'flex'}),
        ], style={'width': '18%', 'display': 'inline-block', 'vertical-align': 'top'}),

        # Polar chart section
        html.Div([
            dcc.Graph(id='polar-chart', style={'width': '100%', 'height': '100vh'})
        ], style={'width': '70%', 'display': 'inline-block'}),
    ], style={'width': '100%'})



# Define callback to update player image
@app.callback(
    Output('player-image', 'src'),
    [Input('player-dropdown', 'value')],
)
def update_player_image(selected_player):
    if selected_player is None:
        return ""
    player_id = df[df['Player'] == selected_player]['Player ID'].iloc[0]
    return get_player_picture(player_id)


# Define callback to update weeks based on selected player
@app.callback(
    Output('week-checklist', 'options'),
    [Input('player-dropdown', 'value')]
)
def update_week_options(selected_player):
    if selected_player is None:
        return []
    weeks = df[df['Player'] == selected_player]['Week'].unique()
    return [{'label': week, 'value': week} for week in weeks]

# Define callback to handle deselecting/selecting all weeks
@app.callback(
    Output('week-checklist', 'value'),
    [Input('deselect-all-button', 'n_clicks'),
     Input('select-all-button', 'n_clicks')],
    [State('week-checklist', 'options')],
)
def handle_all_weeks(n_clicks_deselect, n_clicks_select, options):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]  # Get the ID of the clicked button
    if button_id == 'deselect-all-button':
        return []  # Deselect all weeks
    elif button_id == 'select-all-button':
        return [option['value'] for option in options]  # Select all weeks
    else:
        return dash.no_update  # Maintain the current value if neither button is clicked


# Define callback to update polar chart
@app.callback(
    Output('polar-chart', 'figure'),
    [Input('week-checklist', 'value'),
     Input('player-dropdown', 'value')]
)
def update_polar_chart(selected_weeks, selected_player):
    df = cleaned_df.copy()

    # Calculate percentage contribution for each stat
    for column in df.columns[4:-1]:  # Exclude the first four columns and the last one (Fantasy Points)
        df[f'{column} %'] = (df[column] / df['Fantasy Points']) * 100

    desired_columns = ['Player ID', 'Week', 'Player'] + [col for col in df.columns if col.endswith('%')]
    df_percentage = df[desired_columns]
    df_percentage = df_percentage.drop(columns=['FTA %', 'FGM %', 'TO %', 'FTM %', '3PTM %'], inplace=True) 

    # Check if selected weeks or player is None
    if not selected_weeks or selected_player is None: # If either is None, return an empty figure
        empty_fig = go.Figure(data=go.Scatterpolar())
        empty_fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, gridcolor="white")
            ),
            showlegend=False,
            title=f"Fantasy Point Breakdown by Stats for {selected_player}" if selected_player else "Fantasy Point Breakdown"
        )
        return empty_fig
    
    filtered_df = df[(df['Week'].isin(selected_weeks)) & (df['Player'] == selected_player)] # Filter the DataFrame based on selected weeks and player
    
    categories = ['BLK %', 'REB %', 'STL %', 'AST %', 'PTS %']
    
    # Calculate the mean of selected weeks' percentages
    averaged_values = filtered_df[categories].mean().tolist()
    
    # Ensure a closed loop by appending the first category at the end
    categories.append(categories[0])
    averaged_values.append(averaged_values[0])
    
    fig = go.Figure(data=go.Scatterpolar(
        r=averaged_values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(8, 81, 156, 0.5)',  # semi-transparent fill color
        line=dict(color='rgb(50,93,136)')
    ))
    fig.update_layout(
        polar=dict(
                   radialaxis=dict(visible=True,
                                   gridcolor = "white",)),
        showlegend=False,
        title=f"Fantasy Point Breakdown by Stats for {selected_player}"  # adding a dynamic title
    )
    return fig

# Function to generate home view
def generate_home_view():
    return html.Div([
        html.Label("Select Stats:"),
        dcc.Dropdown(
        id='stat-dropdown',
        options=[ # add options for different stats
            {'label': 'Fantasy Points', 'value': 'Fantasy Points'},
            {'label': 'Points (PTS)', 'value': 'PTS'},
            {'label': 'Assists (AST)', 'value': 'AST'},
            {'label': 'Rebounds (REB)', 'value': 'REB'},
            {'label': 'Blocks (BLK)', 'value': 'BLK'},
            {'label': 'Steals (STL)', 'value': 'STL'},
            {'label': '3-Pointers Made (3PTM)', 'value': '3PTM'},
            {'label': 'Field Goals Made (FGM)', 'value': 'FGM'},
            {'label': 'Free Throws Made (FTM)', 'value': 'FTM'}
        ],
        value='Fantasy Points'  # Default value
    ),
    dcc.Graph(id='race-plot'),
    html.Hr(),
    dcc.Graph(id='fantasy-points-bar-chart'),
            html.Label("Select Stats:"),
            dcc.Dropdown(
            id='bar-chart-dropdown',
            options=[ # add options for different stats
                {'label': 'Fantasy Points', 'value': 'Fantasy Points'},
                {'label': 'Points (PTS)', 'value': 'PTS'},
                {'label': 'Assists (AST)', 'value': 'AST'},
                {'label': 'Rebounds (REB)', 'value': 'REB'},
                {'label': 'Blocks (BLK)', 'value': 'BLK'},
                {'label': 'Steals (STL)', 'value': 'STL'},
                {'label': '3-Pointers Made (3PTM)', 'value': '3PTM'},
                {'label': 'Field Goals Made (FGM)', 'value': 'FGM'},
                {'label': 'Free Throws Made (FTM)', 'value': 'FTM'}
            ],
            value='Fantasy Points'  # Default value
        ),
        html.Br(),
            html.Label("Select Weeks to Display:"),
            dcc.RangeSlider(
                id='week-slider',
                min=0,
                max=len(cleaned_df['Week'].unique()) - 1,
                marks={i: f'Week{week}' for i, week in enumerate(cleaned_df['Week'].unique())},
                value=[len(cleaned_df['Week'].unique()) - 5, len(cleaned_df['Week'].unique()) - 1],
                allowCross=False,  # Prevent crossing over
                step=1,  # Allow only integer steps
            ),
            html.Label("Select Players:"),
            dcc.Dropdown(
                id='player-dropdown',
                options=[{'label': player, 'value': player} for player in cleaned_df['Player'].unique()],
                value=list(cleaned_df['Player'].unique()),  # Select all players by default
                multi=True  # Allow multiple selections
            )
    ])

# Define callback to update the graph
@app.callback(
    Output('race-plot', 'figure'),
    [Input('stat-dropdown', 'value')]
)
def update_race_plot(selected_stat):
    cumulative_df = cleaned_df.copy()
    cumulative_df['Week'] = cumulative_df['Week'].astype(int)
    # Calculate cumulative selected stat for each player up to each week
    cumulative_df = cumulative_df.groupby(['Player', 'Week'])[selected_stat].sum().groupby('Player').cumsum().reset_index()

    # Create a DataFrame to represent week 0 for each player
    players = cumulative_df['Player'].unique()
    week_0_df = pd.DataFrame({'Player': players, 'Week': 0, selected_stat: 0})
    
    # Concatenate the week 0 DataFrame with the cumulative DataFrame
    cumulative_df = pd.concat([week_0_df, cumulative_df])

    #Get the number of players
    # num_players = len(players)

    #Define a color scheme for the categories
    # colors_list = list(reversed(px.colors.sequential.Blues))

    #Create a dictionary mapping each player to a color
    # colors= {players[i]: colors_list[i % len(colors_list)] for i in range(num_players)}

    # Hardcoded because the library does not allow you to set that many color parameters ideally we would use the code above
    # This is what the code would look like if we could use the code above
    # commented out Lonnie Walker IV because he was not in the data as much as the other players
    colors = {
        "Aaron Gordon": "rgb(8,48,107)",
        "Ausar Thompson": "rgb(8,81,156)",
        "Austin Reaves": "rgb(33,113,181)",
        "Chris Paul": "rgb(66,146,198)",
        "Coby White": "rgb(107,174,214)",
        "Damian Lillard": "rgb(158,202,225)",
        "Darius Garland": "rgb(198,219,239)",
        "Dejounte Murray": "rgb(222,235,247)",
        "Deni Avdija": "rgb(247,251,255)",
        "Dereck Lively II": "rgb(8,48,107)",
        "Devin Booker": "rgb(8,81,156)",
        "Donte DiVincenzo": "rgb(33,113,181)",
        "Franz Wagner": "rgb(66,146,198)",
        "Grayson Allen": "rgb(107,174,214)",
        "Jalen Duren": "rgb(158,202,225)",
        "Jalen Johnson": "rgb(198,219,239)",
        "Jamal Murray": "rgb(222,235,247)",
        "Jarrett Allen": "rgb(247,251,255)",
        "Jonas Valanciunas": "rgb(8,48,107)",
        "Josh Okogie": "rgb(8,81,156)",
        "Kawhi Leonard": "rgb(33,113,181)",
        "Keldon Johnson": "rgb(66,146,198)",
        "Khris Middleton": "rgb(107,174,214)",
        #"Lonnie Walker IV": "rgb(158,202,225)",
        "Marvin Bagley III": "rgb(198,219,239)",
        "Michael Porter Jr.": "rgb(222,235,247)",
        "Mike Conley": "rgb(247,251,255)",
        "Onyeka Okongwu": "rgb(8,48,107)",
        "Tyrese Haliburton": "rgb(8,81,156)",
        "Vince Williams Jr.": "rgb(33,113,181)",
        "Walker Kessler": "rgb(66,146,198)",
        "Wendell Carter Jr.": "rgb(107,174,214)",
        "Xavier Tillman": "rgb(158,202,225)"
    }


    #Create a dictionary mapping each player to a color
    # colors= {players[i]: colors_list[i % len(colors_list)] for i in range(num_players)}
    cumulative_df['color'] = cumulative_df['Player'].map(colors)

    # Plot the race plot with specified item_color
    my_raceplot = barplot(cumulative_df,
                          item_column='Player',
                          value_column=selected_stat,
                          top_entries=15,
                          item_color=colors, # add the color dictionary
                          time_column='Week')

    # Get the updated race plot
    fig = my_raceplot.plot(title=f'Bar Chart Race by Top 15 {selected_stat}', # add a title
                           item_label='Players',
                           value_label=selected_stat, # add a label for the value
                           time_label='Week: ', # add a label for the time
                           frame_duration=800)  # adjust frame duration here
    
    fig.update_layout(
        height = 650, # custom height
        xaxis=dict(showgrid=True, gridcolor='lightgrey'), # show only vertical gridlines
    )
    
    return fig

# Define callback to update the graph
@app.callback(
    Output('fantasy-points-bar-chart', 'figure'),
    [Input('week-slider', 'value'),
     Input('player-dropdown', 'value'),
     Input('bar-chart-dropdown', 'value')]  # Add dropdown input
)
def update_bar_chart(selected_weeks_index, selected_players, selected_stat):  # Add selected_stat argument
    cleaned_df['Week'] = cleaned_df['Week'].astype(str)
    # Get the selected weeks based on their index
    selected_weeks = cleaned_df['Week'].unique()[selected_weeks_index[0]:selected_weeks_index[1] + 1]

    # Filter data for the selected weeks and players
    selected_data = cleaned_df[(cleaned_df['Week'].isin(selected_weeks)) & (cleaned_df['Player'].isin(selected_players))]

    # Plotly Express bar chart
    fig = px.bar(selected_data,
                 x='Player', y=selected_stat, color="Week", 
                 title=f'{selected_stat} Bar Chart for Selected Players and Weeks',  # dynamic title based on selected stat
                 barmode='group', # set the bar mode to group
                 height=500, # custom height
                 color_discrete_sequence=list(reversed(px.colors.sequential.Blues))) # set colors

    fig.update_layout(
        xaxis_tickangle=45, # rotate 45 degrees
        plot_bgcolor='white', # set plot background to white
        xaxis=dict(showgrid=False), # turn off horizontal gridlines 
        yaxis=dict(showgrid=True, gridcolor='lightgrey'), # show only vertical gridlines
    )

    return fig

# call back for popup
@app.callback(
    Output("modal", "is_open"),
    [Input("refresh-button", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n_clicks, is_open): # check when the button is clicked if so...
    if n_clicks:
        cleaned_df, team_name, team_logo = get_league_info(espn_s2, swid, team_id, league_id, year) # refresh api
        return not is_open
    return is_open

# Run the app
if __name__ == '__main__':
    app.run_server(jupyter_mode='tab', debug=True)



