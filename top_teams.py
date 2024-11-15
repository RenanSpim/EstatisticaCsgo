import pandas as pd
from datetime import datetime, timedelta

# Load data
csgo_data = pd.read_csv('data/csgo_games_with_elo.csv')

# Initialize variables
elo_ratings = {}  # Dictionary to store the latest Elo ratings for each team
last_played = {}  # Dictionary to store the last match date for each team

# Function to save the top 50 teams to a CSV file
def save_top_50_teams(elo_ratings, match_date, team_1, team_2, file_path='data/top_50_teams.csv'):
    # Sort teams by Elo in descending order and get the top 50
    top_50 = sorted(elo_ratings.items(), key=lambda x: x[1], reverse=True)[:50]
    
    # Prepare data for the row
    data = {}

    # Add match date and the names of the teams playing
    data['match_date'] = match_date
    data['team_1'] = team_1
    data['team_2'] = team_2

    # Add the top 50 teams and their Elo ratings
    for i, (team, elo) in enumerate(top_50, start=1):
        data[f'top_{i}'] = team
        data[f'top_{i}_elo'] = elo
    
    # Append data to CSV
    top_k_df = pd.DataFrame([data])
    top_k_df.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)

# Process each match in csgo_data
for _, row in csgo_data.iterrows():
    team_1, team_2 = row['team_1'], row['team_2']
    team_1_elo, team_2_elo = row['team_1_elo'], row['team_2_elo']
    
    # Convert the match date to datetime object
    match_date = pd.to_datetime(row['match_date'])
    
    # Update Elo ratings for each team in the dictionary
    elo_ratings[team_1] = team_1_elo
    elo_ratings[team_2] = team_2_elo
    
    # Update the last played date for each team
    last_played[team_1] = max(last_played.get(team_1, datetime.min), match_date)
    last_played[team_2] = max(last_played.get(team_2, datetime.min), match_date)
    
    # Remove teams that haven't played in the last 6 months before this match
    six_months_before_match = match_date - timedelta(days=6*30)  # 6 months before the match date
    active_teams = {team: elo for team, elo in elo_ratings.items() if last_played[team] > six_months_before_match}
    
    # Save the current top 50 teams along with the teams playing the match
    save_top_50_teams(active_teams, match_date, team_1, team_2)
