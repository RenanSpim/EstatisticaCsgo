import pandas as pd

# Load data
csgo_data = pd.read_csv('data/csgo_games_with_elo.csv')

# Initialize variables
k = 50  # Set the number of top teams you want
elo_ratings = {}  # Dictionary to store the latest Elo ratings for each team

# Function to save the top k teams to a CSV file
def save_top_k_teams(elo_ratings, k, match_date, file_path='data/top_{}_teams.csv'.format(k)):
    # Sort teams by Elo in descending order and get the top k
    top_k = sorted(elo_ratings.items(), key=lambda x: x[1], reverse=True)[:k]
    
    # Prepare data for the row
    data = {}
    for i, (team, elo) in enumerate(top_k, start=1):
        data['match_date'] = match_date
        data[f'top_{i}'] = team
        data[f'top_{i}_elo'] = elo
    
    # Append data to CSV
    top_k_df = pd.DataFrame([data])
    top_k_df.to_csv(file_path, mode='a', header=not pd.io.common.file_exists(file_path), index=False)

# Process each match in csgo_data
for _, row in csgo_data.iterrows():
    team_1, team_2 = row['team_1'], row['team_2']
    team_1_elo, team_2_elo = row['team_1_elo'], row['team_2_elo']
    
    # Update Elo ratings for each team in the dictionary
    elo_ratings[team_1] = team_1_elo
    elo_ratings[team_2] = team_2_elo
    
    # Save the current top k teams
    save_top_k_teams(elo_ratings, k, row['match_date'])
