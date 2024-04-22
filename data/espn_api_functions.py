# Import libraries
from espn_api.basketball import League
import pandas as pd

def get_league_info(espn_s2, swid, team_id, league_id, year):
    # Create a league object
    league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

    # Create a list to store the data
    data = []
    lineup_points_breakdown = []
    id = 1

    # team id is 2 but team index starts at 0
    team_logo = league.teams[1].logo_url
    
    # Iterate over weeks 1 to 20
    for week in range(1, 21):
        # Assign the box_score variable
        box_scores = league.box_scores(matchup_period=week)
        
        # Iterate through the box_scores list
        for box in box_scores:
            # If the team you are analyizing is the home team, record information regarding team score, name and lineup
            if box.home_team.team_id == team_id:
                team_score = box.home_score
                lineup = box.home_lineup
                team_name = box.home_team.team_name
                # Append the team's weekly data to the list
                data.append({
                    'Week': week,
                    'Team Name': team_name,
                    'Team Score': team_score,
                    'Lineup': lineup,
                })

                # Extracting points breakdown for each player in the lineup
                for player in lineup:
                    player_name = player.name
                    player_id = player.playerId
                    player_points_breakdown = player.points_breakdown
                    lineup_points_breakdown.append({
                        'Unique ID': id,
                        'Week': week,
                        'Player': player_name,
                        'Player ID': player_id,
                        'Points Breakdown': player_points_breakdown
                    })
                    id += 1
                    
            # If the team you are analyzing is the away team, record information regarding team score, name and lineup
            elif box.away_team.team_id == team_id:
                team_score = box.away_score
                lineup = box.away_lineup
                team_name = box.away_team.team_name
                
                # Append the team's weekly data to the list
                data.append({
                    'Week': week,
                    'Team Name': team_name,
                    'Team Score': team_score,
                    'Lineup': lineup,
                })
            
                # Extracting points breakdown for each player in the lineup
                for player in lineup:
                    player_name = player.name
                    playr_id = player.playerId
                    player_points_breakdown = player.points_breakdown
                    lineup_points_breakdown.append({
                        'Unique ID': id,
                        'Week': week,
                        'Player': player_name,
                        'Player ID': playr_id,
                        'Points Breakdown': player_points_breakdown
                    })
                    id += 1
            
        # Print the scores for the specified team to ensure that you are analyzing the correct team and are accessing the correct data
        # print(f"Week {week}: {team_name} scored {team_score} points with lineup {lineup}")

    # Create a pandas dataframe from the data list
    df_player = pd.DataFrame(data)
    points_breakdown = pd.DataFrame(lineup_points_breakdown)

    # We use the explode function to separate the lineup column into individual rows by the comma to split the players
    df_player = df_player.explode('Lineup')

    # Add an ID column to the dataframe
    df_player['Unique ID'] = range(1, len(df_player) + 1)

    # Convert the lineup column to a string to split the column into two columns
    df_player['Lineup'] = df_player['Lineup'].astype(str)

    # Split the lineup column into two columns: Player and Points
    df_player[['Player', 'Fantasy Points']] = df_player['Lineup'].str.split(', ', expand=True)

    # Remove the 'Player(' and ')' from the Player column
    df_player['Player'] = df_player['Player'].str.replace(r'Player\(', '', regex=True).astype(str)

    # Remove the 'points(' and ')' from the Points column
    df_player['Fantasy Points'] = df_player['Fantasy Points'].str.replace(r'.*points:([\d.]+)\)', r'\1', regex=True).astype(float)

    # Create a new column for the weekly contribution percentage
    # df_player['Weekly Contribution Percentage'] = round(df_player['Fantasy Points'] / df_player['Team Score'] * 100, 2)

    # Drop the original Lineup, Team Name and Team Score columns
    df_player.drop(columns=['Lineup', 'Team Name', 'Team Score'], inplace=True)
                
    # Work for Second DF
    # Define a function to extract each key's value from the dictionary
    def extract_stat(stat_dict, stat):
        return stat_dict.get(stat, 0)  # If the stat is not present, default to 0

    # Extracting all unique stats
    unique_stats = set(stat for stat_dict in points_breakdown['Points Breakdown'] for stat in stat_dict.keys())

    # Creating new columns for each stat
    for stat in unique_stats:
        points_breakdown[stat] = points_breakdown['Points Breakdown'].apply(lambda x: extract_stat(x, stat))
        
    # Drop the 'points_breakdown' column
    points_breakdown.drop(columns=['Points Breakdown'], inplace=True)
    
    # Merge two dataframes based on ID
    cleaned_df = points_breakdown.merge(df_player, how='left', on='Unique ID')

    # Drop the Week_y and Player_y columns
    cleaned_df.drop(columns=['Week_y', 'Player_y'], inplace=True)
    cleaned_df.rename(columns={'Week_x': 'Week', 'Player_x': 'Player'}, inplace=True)

    # Change the data types of the columns to category
    cleaned_df['Week'] = cleaned_df['Week'].astype('str')
    cleaned_df['Player'] = cleaned_df['Player'].astype('category')

    # Check to see if merge was successful
    # print(cleaned_df.shape)
    
    team_name = f"{team_name}"
    return cleaned_df, team_name, team_logo

def get_league_url(league_id, team_id, season_id):
    return f"https://fantasy.espn.com/basketball/team?leagueId={league_id}&teamId={team_id}&seasonId={season_id}"

def get_player_picture(player_id):
    return f"https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/{player_id}.png&w=350&h=254"


if __name__ == "__main__":
    espn_s2 = f"AEBxlh0p0NHPbu6WIY0O0TNX6B7oQkhT1bCnR12c5SvsUf5Dnap49bkneUfyt9h1Y5m1MBalds2N47X5i%2FE6YhYUJDbxumf3HrW1iFK%2BPWOGnTpl%2F0wbLLy7C19hr50jNoma59zfYY5iOKxOvK6yT9cn689C4OoQ%2BTiVm%2FG7TjfaGLFIKIJ8OkuSJBye7xYCgnLh%2BvD5Fbbwgz8pLX6htmu%2BEyilZCOrqQ81zDXUrRQgWhIOOXEx1Uy5d1SOQOPkdfqV%2F6Nsr2jUTvgr2T%2FS9yxs"
    swid = "{5C675DD8-073A-4E00-AD7A-B926A3F2800B}"
    team_id = 2
    league_id = 1267411756
    year = 2024
    test, test1, test3 = get_league_info(espn_s2, swid, team_id, league_id, year)

    print(test)
    print(test1)
    print(test3)
    
    test4 = get_league_url(league_id, team_id, year)
    print(test4)

    player_id = 4065663
    test5 = get_player_picture(player_id)
    print(test5)
