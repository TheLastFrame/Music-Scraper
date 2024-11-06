import pandas as pd
from datetime import datetime, timedelta

#??
#todo read in all data/yearly_top_songs/*
# match date with dates in filtered_df
# sum all years
# ranking of songs

# PREFIX='xmas_'
PREFIX='breakup_'

# Read the CSV files
if PREFIX == 'xmas_':
    songs_df = pd.read_csv('data/top_xmas_songs_total_weekly_streams.csv')
elif PREFIX == 'breakup_':
    songs_df = pd.read_csv('data/top_breakup_songs_total_weekly_streams.csv')

# Read the CSV file
df = pd.read_csv('./data/aggregated_weekly_weather_data.csv')

df = df.groupby(['time']).agg({
    'tavg': 'mean',
    'tmax': 'max',
    'tmin': 'min',
    'snow': 'mean'
}).reset_index()

# Define the date range
start_date = datetime(2023, 12, 11)
end_date = start_date + timedelta(days=6)

# Convert the 'time' column to datetime
df['time'] = pd.to_datetime(df['time'])

songs_df['Date'] = songs_df['Date'].str.replace('/', '-')
songs_df = songs_df[~songs_df['Date'].isin(['Total', 'Peak'])]
songs_df['Date'] = pd.to_datetime(songs_df['Date'])

# Filter the DataFrame regardless of the year
filtered_df = df[(df['time'].dt.month == start_date.month) & (df['time'].dt.day >= start_date.day) & 
                 (df['time'].dt.month == end_date.month) & (df['time'].dt.day <= end_date.day)]

merged_df = pd.merge(songs_df, filtered_df, left_on='Date', right_on='time', how='right')

import matplotlib.pyplot as plt

# Ensure 'Date' column is in datetime format
# merged_df['Date'] = pd.to_datetime(merged_df['Date'])

# Plot the bar chart with thicker bars
plt.figure(figsize=(10, 6))
plt.bar(merged_df['Date'], merged_df['Global'], color='red', width=10.0)  # Adjust the width parameter to make bars thicker
plt.xlabel('Date')
plt.ylabel('Global Streams')
plt.title('Global Streams Over Time in week of dec 11')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Save the filtered DataFrame to a new CSV file
filtered_df.to_csv('dec_11_filtered_data.csv', index=False)
merged_df[['Date', 'Global']].to_csv(PREFIX+'dec_11_filtered_data.csv', index=False)