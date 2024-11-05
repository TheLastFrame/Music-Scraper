import os
import uuid
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from joblib import Parallel, delayed
from io import StringIO

breakup_path = 'data/top_breakup_songs_with_ids.csv'
christmas_path = 'data/top_xmas_songs_with_ids.csv'

#read in the breakup and christmas songs
breakup = pd.read_csv(breakup_path)
christmas = pd.read_csv(christmas_path)

lists = [[christmas, 'top_xmas_songs'], [breakup, 'top_breakup_songs']]

for i in lists:
    print(f'working on {i[1]}')

    df = i[0]

    def check_valid_link(df, raw_row):
        row = raw_row[1]
        song_id = row['SongID']
        # if pd.isna(row['SongLink']):
        response = requests.get(f'https://kworb.net/spotify/track/{song_id}.html')
        # return response.status_code == 200
        if response.status_code == 200:
            # print(f'found link for {song_id}')
            # df.at[raw_row[0], 'SongLink'] = f'https://kworb.net/spotify/track/{song_id}.html'
            return f'https://kworb.net/spotify/track/{song_id}.html'
        else:
            return pd.NA

        
    results = Parallel(n_jobs=-1)(delayed(check_valid_link)(df, raw_row) for raw_row in df.iterrows())
    df['SongLink'] = results


christmas.to_csv(christmas_path, index=False)
breakup.to_csv(breakup_path, index=False)