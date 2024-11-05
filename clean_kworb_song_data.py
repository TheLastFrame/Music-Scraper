import os
import pandas as pd
import re

# Define the paths
input_folder = 'data/song_data'
positions_folder = 'data/song_data_cleaned/positions'
streams_folder = 'data/song_data_cleaned/streams'

# Create output directories if they don't exist
os.makedirs(positions_folder, exist_ok=True)
os.makedirs(streams_folder, exist_ok=True)

# Function to split the values
def split_values(value):
    if value == '--':
        return pd.NA, pd.NA
    match = re.match(r'(\d+)\s*\(([\d,]+)\)', str(value))
    if match:
        position = int(match.group(1))
        streams = int(match.group(2).replace(',', ''))
        # split = value.split('(')
        # position = int(split[0].strip())
        # streams = int(split[1].replace(')', '').replace(',', ''))
        return position, streams
    else:
        return value, value

# Loop over each CSV file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_folder, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Initialize empty DataFrames for positions and streams
        positions_df = pd.DataFrame(index=df.index, columns=df.columns)
        streams_df = pd.DataFrame(index=df.index, columns=df.columns)
        
        # Split the values and populate the new DataFrames
        for col in df.columns:
            positions_df[col], streams_df[col] = zip(*df[col].apply(split_values))
        
        # Save the new DataFrames to CSV files
        positions_df.to_csv(os.path.join(positions_folder, filename), index=False)
        streams_df.to_csv(os.path.join(streams_folder, filename), index=False)