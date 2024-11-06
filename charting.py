#TODO: create a calendar week number per week instead of date, average the calendar week number for all years
#%%
import pandas as pd

import matplotlib.pyplot as plt

SHOW_PLOTS = True
PREFIX='xmas_'
# PREFIX='breakup_'

# Read the CSV files
if PREFIX == 'xmas_':
    xmas_songs_df = pd.read_csv('data/top_xmas_songs_total_weekly_streams.csv')
elif PREFIX == 'breakup_':
    xmas_songs_df = pd.read_csv('data/top_breakup_songs_total_weekly_streams.csv')
weather_data_df = pd.read_csv('data/aggregated_weekly_weather_data_with_weeks.csv')

# Replace '/' with '-' in the Date column of the xmas songs data
xmas_songs_df['Date'] = xmas_songs_df['Date'].str.replace('/', '-')

# Remove rows where the value of Date is 'Total' or 'Peak'
xmas_songs_df = xmas_songs_df[~xmas_songs_df['Date'].isin(['Total', 'Peak'])]

# Convert the Date columns to datetime
xmas_songs_df['Date'] = pd.to_datetime(xmas_songs_df['Date'])
weather_data_df['time'] = pd.to_datetime(weather_data_df['time'])

weather_data_df = weather_data_df[weather_data_df['Country'] == 'Austria']

# Group weather_data_df by time and create the required aggregations
weather_data_df = weather_data_df.groupby(['time', 'calendar_week']).agg({
    'tavg': 'mean',
    'tmax': 'max',
    'tmin': 'min',
    'snow': 'mean'
}).reset_index()

# Create a 'year' column from the 'time' column in weather_data_df
weather_data_df['year'] = weather_data_df['time'].dt.year

# Merge the dataframes on the date columns
merged_df = pd.merge(xmas_songs_df, weather_data_df, left_on='Date', right_on='time', how='right')

# Sort merged_df by year and calendar_week
merged_df = merged_df.sort_values(by=['year', 'calendar_week'])

if SHOW_PLOTS:
    # Plot the data with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Create a calendar week column in both dataframes
    # xmas_songs_df['calendar_week'] = xmas_songs_df['Date'].dt.isocalendar().week
    # weather_data_df['calendar_week'] = weather_data_df['time'].dt.isocalendar().week

    # # Merge the dataframes on the calendar week and year columns
    # merged_df = pd.merge(xmas_songs_df, weather_data_df, on=['calendar_week', 'year'])

    # Plot the average temperature on the first y-axis
    ax1.set_xlabel('Calendar Week')
    ax1.set_ylabel('Average Temperature (tavg)', color='tab:blue')
    # Create a second y-axis for the global streams
    ax2 = ax1.twinx()
    ax2.set_ylabel('Global Streams', color='tab:red')

    # Plot each year separately
    for year in merged_df['year'].unique():
        # if year not in [2014, 2015, 2022, 2023]:
        #     continue
        year_data = merged_df[merged_df['year'] == year]
        ax1.plot(year_data['calendar_week'], year_data['tavg'], label=f'Average Temperature {year}')#, color='tab:blue')
        year_data = merged_df[merged_df['year'] == year]
        ax2.plot(year_data['calendar_week'], year_data['Global'], label=f'Global Streams {year}')#, color='tab:green')
        # break
        # break
    ax1.tick_params(axis='y', labelcolor='tab:blue')



    # Plot each year separately
    # for year in merged_df['year'].unique():
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Add labels and title
    fig.tight_layout()
    plt.title('Average Temperature and Global Streams Over Time')
    plt.legend()

    # Show the plot
    plt.show()


# Aggregate the data by calendar week and calculate the average temperature and global streams
aggregated_df = merged_df.groupby('calendar_week').agg({
    'tavg': 'mean',
    'Global': 'mean'
}).reset_index()

aggergated_df_Q4 = aggregated_df[aggregated_df['calendar_week'] > 39]

aggergated_df_Q4.to_csv(f'data/{PREFIX}aggregated_weekly_data_Q4.csv', index=False)

if SHOW_PLOTS:
    # Plot the aggregated data with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Plot the average temperature on the first y-axis
    ax1.set_xlabel('Calendar Week')
    ax1.set_ylabel('Average Temperature (tavg)', color='tab:blue')
    ax1.plot(aggergated_df_Q4['calendar_week'], aggergated_df_Q4['tavg'], label='Average Temperature', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax1.set_xticks(aggergated_df_Q4['calendar_week'][::2])  # Change the step as needed
    ax1.set_xticklabels(aggergated_df_Q4['calendar_week'][::2])  # Rotate labels if needed

    # Create a second y-axis for the global streams
    ax2 = ax1.twinx()
    ax2.set_ylabel('Global Streams', color='tab:red')
    ax2.plot(aggergated_df_Q4['calendar_week'], aggergated_df_Q4['Global'], label='Global Streams', color='tab:green')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    #S Add a vertical marker with a label
    marker_week = 45  # Example week number for the marker
    ax1.axvline(x=marker_week, color='red', linestyle='--')
    ax1.text(marker_week, ax1.get_ylim()[1], 'Start of Christmas Songs', color='gray', ha='center', va='bottom')


    # Add labels and title
    fig.tight_layout()
    plt.title('All Time Average Temperature and Total Global Christmas Song Streams Over Calendar Weeks')
    # ax1.legend(loc='upper left')
    # ax2.legend(loc='upper right')

    # Show the plot
    plt.show()

#%%
# Add the aggregated_df to weather_data_df with 'All Time Avg' for the year column
merged_df = merged_df[['year', 'calendar_week', 'Global', 'tavg', 'tmax', 'tmin', 'snow']]

aggregated_df['year'] = 'All Time Avg'
final_df = pd.concat([merged_df, aggregated_df], ignore_index=True)

final_df.to_csv(f'data/{PREFIX}charts_and_weather_weekly.csv', index=False)

if SHOW_PLOTS:
    # Plot the data with two y-axes
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Create a calendar week column in both dataframes
    # xmas_songs_df['calendar_week'] = xmas_songs_df['Date'].dt.isocalendar().week
    # weather_data_df['calendar_week'] = weather_data_df['time'].dt.isocalendar().week

    # # Merge the dataframes on the calendar week and year columns
    # merged_df = pd.merge(xmas_songs_df, weather_data_df, on=['calendar_week', 'year'])

    # Plot the average temperature on the first y-axis
    ax1.set_xlabel('Calendar Week')
    ax1.set_ylabel('Average Temperature (tavg) (All time avg)', color='tab:blue')

    # Plot each year separately
    # for year in merged_df['year'].unique():
    #     if year != 'All Time Avg':
    #         continue
    year_data = final_df[(final_df['year'] == 'All Time Avg') & (final_df['calendar_week'] > 35)]
    ax1.plot(year_data['calendar_week'], year_data['tavg'], label=f'Average Temperature {year}', color='tab:blue')
        # break
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Create a second y-axis for the global streams
    ax2 = ax1.twinx()
    ax2.set_ylabel('Global Streams', color='tab:red')

    # Plot each year separately
    for year in final_df['year'].unique():
        if year not in [2019, 2020, 2021, 2022, 2023, 'All Time Avg']:
            continue
        year_data = final_df[(final_df['year'] == year) & (final_df['calendar_week'] > 35)]
        ax2.plot(year_data['calendar_week'], year_data['Global'], label=f'Global Streams {year}')#, color='tab:green')
        # break
    ax2.tick_params(axis='y', labelcolor='tab:red')

    # Add labels and title
    fig.tight_layout()
    plt.title('Average Temperature and Global Streams Over Time')
    plt.legend()

    # Show the plot
    plt.show()