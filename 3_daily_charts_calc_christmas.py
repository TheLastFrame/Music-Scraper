#%%
import json
import pandas as pd

# Read the CSV file
df = pd.read_csv('data/daily_charts.csv')

#%%
# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter rows where the month is December
df = df[(df['date'].dt.month == 12) | (df['date'].dt.month == 1)] # | (df['date'].dt.month == 11)

# Display the filtered DataFrame
# print(december_df.head(5))

# Create a new column 'ID' by splitting the 'link' column and taking the last part
df['ID'] = df['url'].apply(lambda x: x.split('/')[-1])

#%%
# Read the top Christmas songs CSV file
top_xmas_songs_df = pd.read_csv('data/top_xmas_songs_with_ids.csv')

# Create a new column 'IsChristmasSong' and set it to True if the 'ID' is in the top Christmas songs DataFrame
df['IsChristmasSong'] = df['ID'].isin(top_xmas_songs_df['SongID'])

# Create a new column 'IsChristmasSongByTitle' and set it to True if 'christmas' is in the 'title' column
df['IsChristmasSongByTitle'] = df['title'].str.lower().str.contains('christmas')

# Update 'IsChristmasSong' to True if either 'IsChristmasSong' or 'IsChristmasSongByTitle' is True
df['IsChristmasSong'] = df['IsChristmasSong'] | df['IsChristmasSongByTitle']

df.drop(columns=['url', 'trend', 'rank', 'IsChristmasSongByTitle'], inplace=True)

# Display the updated DataFrame
print(df.head(5))

# %%

# Group the DataFrame by 'date' and 'IsChristmasSong' and sum the 'streams' column
df = df.groupby(['date', 'IsChristmasSong'])['streams'].sum().reset_index()

# Split the 'date' column into 'year', 'month', and 'day'
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day

df.drop(columns=['date'], inplace=True)

# Group the DataFrame by 'year', 'month', 'day', and 'IsChristmasSong' and sum the 'streams' column
df = df.groupby(['month', 'day', 'IsChristmasSong'])['streams'].mean().reset_index()

# df = df.sort_values(by=['IsChristmasSong', 'streams'], ascending=[False, False]).reset_index()
df = df.sort_values(by=['month', 'day'], ascending=[True, True])

# Calculate the total streams for each day
total_streams_per_day = df.groupby(['month', 'day'])['streams'].sum().reset_index()
total_streams_per_day.rename(columns={'streams': 'total_streams'}, inplace=True)

# Merge the total streams with the original DataFrame
df = pd.merge(df, total_streams_per_day, on=['month', 'day'])

# Calculate the percentage of IsChristmasSong streams
df['percentage'] = ((df['streams'] / df['total_streams']) * 100).round(2)

# Drop the 'total_streams' column as it's no longer needed
df.drop(columns=['total_streams'], inplace=True)

# Display the grouped DataFrame
print(df.head(5))

# df.drop(columns=['index'], inplace=True)

df[(df['month'] == 12)].to_csv('data/december_all_time_aily_charts_christmas.csv', index=False)
data_dict = df[(df['month'] == 12)].to_dict('list')
with open(f'data/december_all_time_aily_charts_christmas.json', 'w') as f:
    json.dump(data_dict, f)

df = df.sort_values(by=['month', 'day'], ascending=[True, True])

df.to_csv('data/nov_to_jan_all_time_aily_charts_christmas.csv', index=False)
data_dict = df.to_dict('list')
with open(f'data/nov_to_jan_all_time_aily_charts_christmas.json', 'w') as f:
    json.dump(data_dict, f)



# Split the 'IsChristmasSong' column into two columns 'ChristmasSongs' and 'Non-ChristmasSongs'
df['ChristmasSongs'] = df.apply(lambda row: row['streams'] if row['IsChristmasSong'] else 0, axis=1)
df['NonChristmasSongs'] = df.apply(lambda row: row['streams'] if not row['IsChristmasSong'] else 0, axis=1)

print(df.head(5))

# Drop the 'IsChristmasSong' and 'streams' columns as they are no longer needed
df.drop(columns=['IsChristmasSong', 'streams'], inplace=True)
# Group by 'month' and 'day' and sum the 'ChristmasSongs' and 'NonChristmasSongs' columns
df = df.groupby(['month', 'day'])[['ChristmasSongs', 'NonChristmasSongs']].sum().reset_index()

# Calculate the percentage of ChristmasSongs and NonChristmasSongs
df['ChristmasSongsPercentage'] = ((df['ChristmasSongs'] / (df['ChristmasSongs'] + df['NonChristmasSongs'])) * 100).round(2)
df['NonChristmasSongsPercentage'] = ((df['NonChristmasSongs'] / (df['ChristmasSongs'] + df['NonChristmasSongs'])) * 100).round(2)

# Parse 'ChristmasSongs' and 'NonChristmasSongs' as int
df['ChristmasSongs'] = df['ChristmasSongs'].astype(int)
df['NonChristmasSongs'] = df['NonChristmasSongs'].astype(int)

# Display the final DataFrame
print(df.head(5))


df[(df['month'] == 12)].to_csv('data/december_all_time_daily_charts_christmas_clean.csv', index=False)
data_dict = df[(df['month'] == 12)].to_dict('list')
with open(f'data/december_all_time_daily_charts_christmas_clean.json', 'w') as f:
    json.dump(data_dict, f)

df_christmas = df[(df['month'] == 12)]
df_christmas = df_christmas[(df_christmas['day'].isin([24, 25, 26, 27]))]

df_christmas.to_csv('data/christmas_week_all_time_daily_charts_clean.csv', index=False)
data_dict = df_christmas.to_dict('list')
with open(f'data/christmas_week_all_time_daily_charts_clean.json', 'w') as f:
    json.dump(data_dict, f)

df['date'] = df.apply(lambda row: f"{int(row['day']):02d}.{int(row['month']):02d}", axis=1)

df = df[((df['month'] == 12) & (df['day'] > 27)) | (df['month'] == 1)]

df = df.sort_values(by=['month', 'day'], ascending=[False, True])

df.drop(columns=['month', 'day'], inplace=True)

df.to_csv('data/nov_to_jan_all_time_daily_charts_christmas_clean.csv', index=False)
data_dict = df.to_dict('list')
with open(f'data/nov_to_jan_all_time_daily_charts_christmas_clean.json', 'w') as f:
    json.dump(data_dict, f)