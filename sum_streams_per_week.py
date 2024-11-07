import pandas as pd
import os

from tqdm import tqdm

# Read the CSV files
breakup = pd.read_csv('data/top_breakup_songs_with_ids.csv')
christmas = pd.read_csv('data/top_xmas_songs_with_ids.csv')

# Initialize an empty DataFrame to store the combined data
combined_xmas_df = pd.DataFrame()
combined_breakup_df = pd.DataFrame()

# Directory containing the song data files
data_dir = 'data/song_data_cleaned/streams'


#read in the breakup and christmas songs

lists = [[christmas, 'top_xmas_songs', combined_xmas_df], [breakup, 'top_breakup_songs', combined_breakup_df]]

for i in lists:
    print(f'working on {i[1]}')

    df = i[0]
    combined_df = i[2]
    # Iterate over each row in the xmas_songs_df
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        song_id = row['SongID']
        file_path = os.path.join(data_dir, f'{song_id}_spotify_songs_stats.csv')
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Read the file and append it to the combined DataFrame
            song_data_df = pd.read_csv(file_path)
            combined_df = pd.concat([combined_df, song_data_df], ignore_index=True)

    combined_df['Date'] = combined_df['Date'].str.replace('/', '-')

    # Sort by date
    combined_df = combined_df.sort_values(by='Date')

    # Group by the 'Date' column and sum the values for each column
    grouped_df = combined_df.groupby('Date').sum().reset_index()

    # Save the final DataFrame to a CSV file
    grouped_df.to_csv(f'data/{i[1]}_total_weekly_streams.csv', index=False)