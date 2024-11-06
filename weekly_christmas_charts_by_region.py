import pandas as pd

PREFIX =""
# PREFIX ="MARIAH"
# PREFIX = "WHAM"

# Read the CSV file
if PREFIX == "":
    df = pd.read_csv('data/top_xmas_songs_total_weekly_streams.csv')
elif PREFIX == "MARIAH":
    df = pd.read_csv('data/song_data_cleaned/streams/0bYg9bo50gSsH3LtXe2SQn_spotify_songs_stats.csv')
elif PREFIX == "WHAM":
    df = pd.read_csv('data/song_data_cleaned/streams/06qMRF18gwbOYYbnP2du6i_spotify_songs_stats.csv')

# Remove rows with 'Total' and 'Peak' in the 'Date' column
df = df[~df['Date'].str.contains('Total|Peak')]

# Convert 'Date' column to datetime
df['Date'] = df['Date'].str.replace('/', '-')
df['Date'] = pd.to_datetime(df['Date'])

# Add calendar week column
df['Calendar_Week'] = df['Date'].dt.isocalendar().week

# Drop the 'Date' column
df = df.drop(columns=['Date'])
df = df.drop(columns=['Global'])

# Group by calendar week and average all columns
df_avg = df.groupby('Calendar_Week').mean().round(0) #.astype(int)

# Save the result to a new CSV file
if PREFIX == "":
    df_avg.to_csv('data/avg_xmas_songs_weekly_streams.csv')
elif PREFIX == "MARIAH":
    df_avg.to_csv('data/mariah_carey_all_i_want_for_christmas_is_you_weekly_streams.csv')
elif PREFIX == "WHAM":
    df_avg.to_csv('data/wham_last_christmas_weekly_streams.csv')

print("Processing complete. Averaged data saved to 'data/avg_xmas_songs_weekly_streams.csv'.")
# Transpose the dataframe
df_transposed = df_avg.transpose()

if PREFIX == "":
    df_transposed = df_transposed.sort_values(by=[42,43,45,46,47,48,49,50,51,52,1,2,3,4,5], ascending=False)
elif PREFIX == "MARIAH":
    df_transposed = df_transposed.sort_values(by=[42,43,45,46,47,48,49,50,51,52,1,2], ascending=False)
elif PREFIX == "WHAM":
    df_transposed = df_transposed.sort_values(by=[42,43,45,46,47,48,49,50,51,52,1,2,3,4,5], ascending=False)

# Save the transposed dataframe to a new CSV file
if PREFIX == "":
    df_transposed.to_csv('data/transposed_avg_xmas_songs_weekly_streams.csv')
elif PREFIX == "MARIAH":
    df_transposed.to_csv('data/transposed_mariah_carey_all_i_want_for_christmas_is_you_weekly_streams.csv')
elif PREFIX == "WHAM":
    df_transposed.to_csv('data/transposed_wham_last_christmas_weekly_streams.csv')

print("Transposed data saved to 'data/transposed_avg_xmas_songs_weekly_streams.csv'.")
print('First songs to start listening to christmas songs:')

df_top = df_transposed.head(5)
print(df_top)