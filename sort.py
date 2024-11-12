import pandas as pd

# Load the CSV file
df = pd.read_csv('data/csgo_games.csv')

# Convert the 'match_date' column to datetime format to ensure proper sorting
df['match_date'] = pd.to_datetime(df['match_date'])

# Sort the DataFrame by 'match_date'
df_sorted = df.sort_values(by='match_date')

# Save the sorted DataFrame to a new CSV file (optional)
df_sorted.to_csv('data/csgo_games_sorted.csv', index=False)
