import json
import pandas as pd
import pycountry

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

# Create a dictionary for alpha-2 to alpha-3 conversion
alpha2_to_alpha3 = {country.alpha_2: country.alpha_3 for country in pycountry.countries}
# Rename columns using the dictionary
df.rename(columns=alpha2_to_alpha3, inplace=True)

# Group by calendar week and average all columns
df_avg = df.groupby('Calendar_Week').mean().round(0) #.astype(int)

# Save the result to a new CSV file
data_dict = df_avg.to_dict('list')
if PREFIX == "":
    df_avg.to_csv('data/avg_xmas_songs_weekly_streams.csv')
    with open(f'data/avg_xmas_songs_weekly_streams.json', 'w') as f:
        json.dump(data_dict, f)
elif PREFIX == "MARIAH":
    df_avg.to_csv('data/mariah_carey_all_i_want_for_christmas_is_you_weekly_streams.csv')
    with open(f'data/mariah_carey_all_i_want_for_christmas_is_you_weekly_streams.json', 'w') as f:
        json.dump(data_dict, f)
elif PREFIX == "WHAM":
    df_avg.to_csv('data/wham_last_christmas_weekly_streams.csv')
    with open(f'data/wham_last_christmas_weekly_streams.json', 'w') as f:
        json.dump(data_dict, f)

print("Processing complete. Averaged data saved to 'data/avg_xmas_songs_weekly_streams.csv'.")
# Transpose the dataframe
df_transposed = df_avg.transpose()
# Convert column labels to int
df_transposed.columns = df_transposed.columns.astype(int)
# df_transposed = df_transposed.reset_index()
# df_transposed = df_transposed.rename(columns={'index': 'Country'})

# Calculate the percentage of each column in a row relative to the sum of all columns in that row
# df_transposed = df_transposed.div(df_transposed.sum(axis=1), axis=0)
# Calculate the percentage of each column in a row relative to the max value of that row
df_transposed = df_transposed.div(df_transposed.max(axis=1), axis=0)

if PREFIX == "":
    df_transposed = df_transposed.sort_values(by=[42,43,45,46,47,48,49,50,51,52,1,2,3,4,5], ascending=False)
elif PREFIX == "MARIAH":
    df_transposed = df_transposed.sort_values(by=[42,43,45,46,47,48,49,50,51,52,1,2], ascending=False)
elif PREFIX == "WHAM":
    df_transposed = df_transposed.sort_values(by=[42,43,45,46,47,48,49,50,51,52,1,2,3,4,5], ascending=False)

# Save the transposed dataframe to a new CSV file
data_dict = df_transposed.to_dict('list')
if PREFIX == "":
    df_transposed.to_csv('data/transposed_avg_xmas_songs_weekly_streams.csv')
    # with open(f'data/transposed_avg_xmas_songs_weekly_streams.json', 'w') as f:
    #     json.dump(data_dict, f)
    df_transposed.to_json('data/transposed_avg_xmas_songs_weekly_streams.json', orient='columns')
    
elif PREFIX == "MARIAH":
    df_transposed.to_csv('data/transposed_mariah_carey_all_i_want_for_christmas_is_you_weekly_streams.csv')
    df_transposed.to_json('data/transposed_avg_xmas_songs_weekly_streams.json', orient='columns')

elif PREFIX == "WHAM":
    df_transposed.to_csv('data/transposed_wham_last_christmas_weekly_streams.csv')
    with open(f'data/transposed_wham_last_christmas_weekly_streams.json', 'w') as f:
        json.dump(data_dict, f)

print("Transposed data saved to 'data/transposed_avg_xmas_songs_weekly_streams.csv'.")
print('First songs to start listening to christmas songs:')

df_top = df_transposed.head(5)
print(df_top)