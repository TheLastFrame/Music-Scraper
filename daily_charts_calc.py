#%%
import pandas as pd

# Read the CSV file
df = pd.read_csv('data/daily_charts.csv')

#%%
# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'])

# Filter rows where the month is December
df = df[(df['date'].dt.month == 12) | (df['date'].dt.month == 11) | (df['date'].dt.month == 1)]

# Display the filtered DataFrame
# print(december_df.head(5))

# Create a new column 'ID' by splitting the 'link' column and taking the last part
df['ID'] = df['url'].apply(lambda x: x.split('/')[-1])

#%%
# Read the top Christmas songs CSV file
top_xmas_songs_df = pd.read_csv('data/top_xmas_songs_with_ids.csv')

# Create a new column 'IsChristmasSong' and set it to True if the 'ID' is in the top Christmas songs DataFrame
df['IsChristmasSong'] = df['ID'].isin(top_xmas_songs_df['SongID'])

df.drop(columns=['url', 'trend', 'rank'], inplace=True)

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
df = df.groupby(['month', 'day', 'IsChristmasSong'])['streams'].sum().reset_index()

df = df.sort_values(by=['IsChristmasSong', 'streams'], ascending=[False, False]).reset_index()

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

df.drop(columns=['index'], inplace=True)

df[(df['month'] == 12)].to_csv('data/december_all_time_aily_charts_christmas.csv', index=False)

df = df.sort_values(by=['month', 'day'], ascending=[True, True])

df.to_csv('data/nov_to_jan_all_time_aily_charts_christmas.csv', index=False)