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
#read the artist links
artist_links = pd.read_csv('data/spotify_artists_links.csv')
print(f"unique artists (links): {artist_links['Artist'].nunique()}")
#group by artist
breakup = breakup.groupby('Artist').sum().reset_index()
christmas = christmas.groupby('Artist').sum().reset_index()
#merge the two dataframes
artists = pd.concat([breakup, christmas], ignore_index=True)
#drop duplicates
artists = artists.drop_duplicates(subset='Artist')
print(f"unique artists (break_up+xmas): {artists['Artist'].nunique()}")
#merge the artist links with the artists, if str of artist_links is in artists str
# artists = artists.merge(artist_links, on='Artist', how='left')
artists['Link'] = artists['Artist'].apply(lambda artist: next((link for link_artist, link in zip(artist_links['Artist'], artist_links['Link']) if link_artist.lower() in artist.lower()), None))
#count the number of missing links
missing_links = artists['Link'].isnull().sum()
print(f"missing links: {missing_links}")
#get names of artists with missing links
missing_artists = artists[artists['Link'].isnull()]['Artist']
#drop the rows with missing links
artists = artists.dropna(subset=['Link'])
#get number of unique artists
#drop duplicates
artists = artists.drop_duplicates(subset='Artist')
#loop over all artists
print(f"unique artists (final - to download): {artists['Artist'].nunique()}")
print(f"missing artists: {missing_artists}")

artists.to_csv('data/artists_found_breakup_xmas_spotify_links.csv', index=False)

# exit(0)

url = 'https://kworb.net' #url2

#manual fixes:
# add 

#itterate over all the links, with tqdm for a progress bar
for raw_row in tqdm(artists.iterrows(), total=artists.shape[0]):
# for raw_row in artists.iterrows():
    row = raw_row[1]
    artist = row['Artist']
    link = url+row['Link']
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    parsed_table = soup.findAll('tbody')[1]
    data = [
        [item for i, td in enumerate(row.find_all('td'))
        for item in (
            td.a['href'] if td.find('a') and i == 0 else '',  # Get href only in the first column
            ''.join(td.stripped_strings)  # Text content for every column
        )]
        for row in parsed_table.find_all('tr')
    ]
    df = pd.DataFrame(data, columns=['Spotify Link', 'Song', 'hStreams', 'Streams', 'hDaily', 'Daily'])
    df.replace('', pd.NA, inplace=True)  # Replace empty strings with NaN
    df.dropna(axis=1, how='all', inplace=True)

    #add the artist column
    df['Artist'] = artist
    df['ID'] = df['Spotify Link'].str.split('/').str[-1]
    df['KworbLink'] = df['ID'].apply(lambda x: f'https://kworb.net/spotify/track/{x}.html')
    artist_path_name = "".join( x for x in artist if (x.isalnum() or x in "._- ")) # https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
    if artist_path_name == "" or artist_path_name.isspace() or artist_path_name == '-' or artist_path_name == '_':
        #create uuid4 as fallback
        artist_path_name = str(uuid.uuid4())

    df['ValidLink'] = False

    def check_valid_link(row):
        response = requests.get(row['KworbLink'])
        return response.status_code == 200

    # Use joblib to run the requests in parallel
    results = Parallel(n_jobs=-1)(delayed(check_valid_link)(row) for _, row in df.iterrows())

    # Update the 'ValidLink' column with the results
    df['ValidLink'] = results

    df['ArtistID'] = link.split('/')[-1].split('_')[0]

    os.makedirs('data/artist_songs', exist_ok=True)
    # df.to_csv(f'data/artist_songs/{artist_path_name}_spotify_artist_songs.csv', index=False)
    df[['Artist', 'Song','ID','ArtistID', 'ValidLink', 'KworbLink', 'Spotify Link']].to_csv(f'data/artist_songs/{artist_path_name}_spotify_artist_songs_links.csv', index=False)
