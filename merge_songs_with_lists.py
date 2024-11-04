import os
import uuid
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from joblib import Parallel, delayed

#read in the breakup and christmas songs
breakup = pd.read_csv('data/top_breakup_songs.csv')
christmas = pd.read_csv('data/top_xmas_songs.csv')

lists = [[christmas, 'top_xmas_songs'], [breakup, 'top_breakup_songs']]

for i in lists:

    print(f'working on {i[1]}')

    df = i[0]

    found = 0
    df['ArtistID'] = pd.NA
    df['SongID'] = pd.NA
    df['SongLink'] = pd.NA
    #itterate over all the links, with tqdm for a progress bar
    for raw_row in tqdm(df.iterrows(), total=df.shape[0]):
        row = raw_row[1]
        artist = row['Artist']
        song = row['Song Title']
        artist_path_name = "".join( x for x in artist if (x.isalnum() or x in "._- ")) # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
        artist_path =f'data/artist_songs/{artist_path_name}_spotify_artist_songs_links.csv'
        if os.path.exists(artist_path):
            found+=1
            artist_df = pd.read_csv(artist_path)
            df.at[raw_row[0], 'ArtistID'] = artist_df.iloc[0]['ArtistID']
            matching_song = artist_df[artist_df['Song'].str.lower() == song.lower()]
            # print(f'found {matching_song.shape[0]} matches for {song} by {artist}')
            # print(matching_song)
            if not matching_song.empty:
                # if matching_song.shape[0] > 1:
                    # print(f'multiple matches for {song} by {artist}')
                    # print(matching_song)
                matching_song = matching_song.iloc[0] #fixes the multiple matches issue and bool issue with ValidLink
                df.at[raw_row[0], 'SongID'] = matching_song['ID']
                if matching_song['ValidLink']:
                    df.at[raw_row[0], 'SongLink'] = matching_song['KworbLink']

    missing = df.shape[0]-found
    print(f'found {found} files')
    print(f'missing {missing} files')

    df.rename(columns={'Song Title': 'Song'}, inplace=True)
    df.to_csv(f'data/{i[1]}_with_ids.csv', index=False)