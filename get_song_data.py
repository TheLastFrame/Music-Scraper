import os
import uuid
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from joblib import Parallel, delayed
from io import StringIO

#read in the breakup and christmas songs
breakup = pd.read_csv('data/top_breakup_songs_with_ids.csv')
christmas = pd.read_csv('data/top_xmas_songs_with_ids.csv')

lists = [[christmas, 'top_xmas_songs'], [breakup, 'top_breakup_songs']]

for i in lists:
    print(f'working on {i[1]}')

    df = i[0]
    #itterate over all the links, with tqdm for a progress bar
    for raw_row in tqdm(df.iterrows(), total=df.shape[0]):
    # for raw_row in artists.iterrows():
        row = raw_row[1]
        song_id = row['SongID']
        link = row['SongLink']
        if pd.isna(link):
            continue
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        weekly_div = soup.find('div', {'class': 'weekly'})
        # print(weekly_div)
        if weekly_div is None:
            print(f'No weekly data found for song ID {song_id}')
            continue
        parsed_table = weekly_div.find('table')
        if parsed_table is None:
            print(f'No table found for song ID {song_id}')
            continue
        # print(parsed_table)

        df = pd.read_html(StringIO(str(parsed_table)))[0]
        # df.columns = df.columns.droplevel(0)
        df.replace('', pd.NA, inplace=True)  # Replace empty strings with NaN
        # df.dropna(axis=1, how='all', inplace=True)

        os.makedirs('data/song_data', exist_ok=True)
        df.to_csv(f'data/song_data/{song_id}_spotify_songs_stats.csv', index=False)