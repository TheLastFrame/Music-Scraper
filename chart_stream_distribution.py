#%%
import pandas as pd

# Read the dataset
file_path = 'data/charts.csv'
df = pd.read_csv(file_path)

# Sum all streams per date
streams_per_date = df.groupby('date')['streams'].sum().reset_index()
# Print the result
print(streams_per_date)
#%%
import matplotlib.pyplot as plt

# Create calendar week numbers for each date
df['date'] = df['date'].str.replace('/', '-')
df['date'] = pd.to_datetime(df['date'])
df['week'] = df['date'].dt.isocalendar().week
df['year'] = df['date'].dt.year

# Sum streams per week and year
streams_per_week_year = df.groupby(['year', 'week'])['streams'].sum().reset_index()

#%%
# Plot each year in one chart
years = streams_per_week_year['year'].unique()
for year in years:
    data = streams_per_week_year[streams_per_week_year['year'] == year]
    plt.plot(data['week'], data['streams'], label=str(year))

plt.xlabel('Week Number')
plt.ylabel('Streams')
plt.title('Weekly Streams Distribution by Year')
plt.legend()
plt.show()