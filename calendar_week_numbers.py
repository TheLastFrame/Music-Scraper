import pandas as pd

# Read the CSV file
df = pd.read_csv('data/aggregated_weekly_weather_data.csv')

# Convert the 'time' column to datetime
df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d')

# Sort the dataframe by 'time'
df = df.sort_values(by='time')

# Add a 'calendar_week' column
df['calendar_week'] = df['time'].dt.isocalendar().week

# Save the updated dataframe to a new CSV file
df.to_csv('data/aggregated_weekly_weather_data_with_weeks.csv', index=False)