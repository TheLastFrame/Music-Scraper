from datetime import datetime, timedelta
import pandas as pd
import logging
from meteostat import Point, Daily
import warnings
from joblib import Parallel, delayed

warnings.filterwarnings('ignore')

#Set up logging
logging.basicConfig(filename='skipped_stations.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

start = datetime(2014, 1, 1)
#end = datetime(2014, 2, 1)
end = datetime.now() - timedelta(days=1) 

#Read in WMO file
df = pd.read_csv('WMO_StationID.txt', delimiter=';', encoding='latin1') 

df.columns = df.columns.str.replace(' ', '')
df['Latitude'] = pd.to_numeric(df['Latitude'].astype(str).str.replace(' ', ''), errors='coerce')
df['Longitude'] = pd.to_numeric(df['Longitude'].astype(str).str.replace(' ', ''), errors='coerce')
df['StationName'] = df['StationName'].replace(' ', '')
df['Country'] = df['Country'].replace(' ', '')
df['WMO-StationID'] = df['WMO-StationID'].replace(' ', '')

final_df = pd.DataFrame()
#For each Country
for country in df['Country'].unique():

# def get_country_data(country):
    # final_df = pd.DataFrame()
    country_stations = df[df['Country'] == country]
    print(f"Processing stations for country: {country}")

    if pd.isna(country) or country == 'nan':
        logging.info(f"Skipped {station_name}, Country: {country} - Reason: Country is NaN or 'nan'.")
        # return
        continue
    
    else:
        all_station_data = []
        #For each station
        for _, row in country_stations.iterrows():
            station_name = row['StationName']
            wmo_id = row['WMO-StationID']
            lat = row['Latitude']
            lon = row['Longitude']

            #Check if lat and lon are NaN
            if pd.isna(lat) and pd.isna(lon):
                #If both are NaN, check WMO-StationID
                if pd.isna(wmo_id):
                    #Log the skipped station
                    logging.info(f"Skipped {station_name}, Country: {country} - Reason: Both latitude and longitude are NaN and WMO-StationID is NaN.")
                    continue  #Skip this station
                else:
                    #Use WMO ID
                    data = Daily(wmo_id, start, end).fetch()
            else:
                #Create Point
                point = Point(lat, lon)
                #Get daily data
                data = Daily(point, start, end).fetch()

            if data.empty:
                logging.info(f"No data returned for {station_name}.")
                continue  

            data = data.drop(columns=['prcp','wdir','wspd','wpgt','pres','tsun'], axis=1)
            all_station_data.append(data)

        if not all_station_data:
            logging.info("No data collected from any station.")
            combined_df = pd.DataFrame()
        else:  
            combined_df = pd.concat(all_station_data)
            #Aggregate by date across all stations
            daily_agg = combined_df.groupby(combined_df.index).agg({
                'tavg': 'mean',  # Average of weekly temperature
                'tmin': 'mean',  # Average of weekly minimum temperature
                'tmax': 'mean',  # Average of weekly maximum temperature
                'snow': 'max'    # Maximum snowfall for the week
                })

            daily_agg['Country'] = country.replace(' ', '')
            final_df = pd.concat([final_df, daily_agg])

    # return final_df

# Weekly Data for each Country
# weekly_dataframes = [] 

# for country in final_df['Country'].unique():
#     country_df = final_df[final_df['Country'] == country]

#     # Resample for the country DataFrame
#     weekly_df = country_df.resample('W-THU').agg({
#         'tavg': 'mean',  # Average of weekly temperature
#         'tmin': 'mean',  # Average of weekly minimum temperature
#         'tmax': 'mean',  # Average of weekly maximum temperature
#         'snow': 'max'    # Maximum snowfall for the week
#     })

#     # Add the country name as a column
#     weekly_df['Country'] = country

#     # Store the weekly DataFrame
#     weekly_dataframes.append(weekly_df)

# # Combine all weekly DataFrames into a single DataFrame
# final_weekly_df = pd.concat(weekly_dataframes)

# # Reset index
# final_weekly_df = final_weekly_df.reset_index()

# Save the DataFrame to a CSV file
# output_file_path = 'aggregated_weekly_weather_data.csv'
# final_weekly_df.to_csv(output_file_path, index=False)

# results = Parallel(n_jobs=-1)(delayed(get_country_data)(country) for country in df['Country'].unique())

# final_df = None
# for result in results:
#     if final_df is None:
#         final_df = result
#     else:
#         final_df = pd.concat([final_df, result])

final_df = final_df.reset_index()
output_file_path = 'aggregated_daily_weather_data.csv'
final_df.to_csv(output_file_path, index=False)