import os
import requests
import pandas as pd
from tqdm import tqdm

# Define the SPARQL endpoint URL
endpoint_url = "https://query.wikidata.org/sparql"

# Define the SPARQL query
def get_query(title: str, artist: str):
    query = f"""
    SELECT ?song ?songLabel ?artist ?artistLabel ?genre ?genreLabel ?subclass1 ?subclass1Label ?subclass2 ?subclass2Label ?spotifyID WHERE {{
    ?song wdt:P175 ?artist;   # Performer (artist)
            rdfs:label ?songENLabel;  # Label of the song is "Cruel Summer"
            wdt:P136 ?genre.   # The genre(s) of the song
    OPTIONAL {{ ?song wdt:P2207 ?spotify. }}
    BIND(COALESCE(?spotify, "") AS ?spotifyID)

    ?artist rdfs:label "{artist}"@en.  # Label of the artist is "Taylor Swift"
    
    ?genre wdt:P279 ?subclass1.
    ?subclass1 wdt:P279 ?subclass2.
    
    
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
    
    FILTER (lang(?songENLabel) = "en" && lcase(str(?songENLabel)) = "{title}")
    }}
    """
    # print(query)
    return query


# Set the headers
headers = {
    "Accept": "application/sparql-results+json",
    'User-Agent': 'CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'
}

print('Loading data...')

all_songs = pd.read_csv('data/_spotify_songs.csv').rename({'Artist':'artist', 'Song':'song'}, axis=1)

if os.path.exists('data/songs_genres_wd.csv'):
    already_searched = pd.read_csv('data/songs_genres_wd.csv')
else:
    already_searched = pd.DataFrame(columns=['artist', 'song'])

songs_to_search = []

print('Checking which songs need to be searched...')

for raw_row in all_songs.iterrows():
    row = raw_row[1]
    # print(row)
    artist = row['artist']
    song = row['song']
    songs_of_artist = already_searched[already_searched.artist == artist]

    if song not in songs_of_artist.song.values:
        songs_to_search.append({'song': str(song), 'artist': str(artist)})



print(f'{len(songs_to_search)} songs to search')
# print('Songs to search:')
# print(songs_to_search)
# #await user input
# input('Press Enter to continue...')
print('Searching...')

not_found = 0
missing='Missing Songs:'
rows = []
for song in tqdm(songs_to_search, unit='songs', total=len(songs_to_search)):
    found = False

    # Send the request
    response = requests.get(endpoint_url, params={'query': get_query(song['song'].lower(), song['artist'])}, headers=headers)

    # print('Download finished, saving data...')

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        # print(data)

        columns = data['head']['vars']
        bindings = data['results']['bindings']

        if bindings != []:
            found = True
            for binding in bindings:
                row = {var: binding[var]['value'] for var in columns}
                rows.append(row)
        else:
            not_found += 1
            # print(f'\nNo data found for {song['song']} by {song['artist']}')
            missing += f'\n\t{song["song"]} by {song["artist"]}'
            rows.append({'artistLabel': song['artist'], 'songLabel': song['song'], 'genreLabel': '', 'artist': '', 'song': '', 'genre': '', 'subclass1':'', 'subclass1Label':'', 'subclass2':'', 'subclass2Label':''})
            #TODO: if artist was found before, then song won't exist, else lower case search the artist and then the song


        # Creating DataFrame
        df = pd.DataFrame(rows, columns=columns)

        # Display DataFrame
        # print(df)

        df_song = df[['artistLabel', 'songLabel', 'genreLabel', 'artist','song', 'genre']].rename({'artistLabel': 'artist', 'songLabel': 'song', 'genreLabel':'genre', 'artist':'artist_wd', 'song':'song_wd', 'genre':'genre_wd'}, axis=1)
        df_song_no_wd = df[['artistLabel', 'songLabel', 'genreLabel']].rename({'artistLabel': 'artist', 'songLabel': 'song', 'genreLabel':'genre'}, axis=1)

        if found:
            df_generes = df[['genreLabel', 'subclass1Label', 'genre', 'subclass1']].rename({'genreLabel': 'genre', 'subclass1Label': 'superclass', 'genre':'genre_wd', 'subclass1':'superclass_wd'}, axis=1)
            df_subgeneres = df[['subclass1Label', 'subclass2Label', 'subclass1', 'subclass2']].rename({'subclass1Label': 'genre', 'subclass2Label': 'superclass', 'subclass1':'genre_wd', 'subclass2':'superclass_wd'}, axis=1)
            df_generes = pd.concat([df_generes, df_subgeneres], ignore_index=True)

        df_song = df_song.drop_duplicates()
        df_song_no_wd = df_song_no_wd.drop_duplicates()
        if found:
            df_generes = df_generes.drop_duplicates()

        song_header = True
        song_mode = 'w'
        if os.path.exists('data/songs_genres_wd.csv'):
            song_header = False
            song_mode = 'a'

        df_song.to_csv('data/songs_genres_wd.csv',  mode=song_mode, index=False, header=song_header)

        song_no_wd_header = True
        song_no_wd_mode = 'w'
        if os.path.exists('data/songs_genres.csv'):
            song_no_wd_header = False
            song_no_wd_mode = 'a'

        df_song_no_wd.to_csv('data/songs_genres.csv',  mode=song_no_wd_mode, index=False, header=song_no_wd_header)

        if found:
            genre_header = True
            genre_mode = 'w'
            if os.path.exists('data/genres_wd.csv'):
                genre_header = False
                genre_mode = 'a'

            df_generes.to_csv('data/genres_wd.csv', mode=genre_mode, index=False, header=genre_header)

        # print('Data saved to data/songs_genres.csv, data/songs_genres_wd.csv and data/genres_wd.csv')

        # Print the results
        # for item in data['results']['bindings']:
        #     print(f"{item['item']['value']} - {item['itemLabel']['value']}")
        # break;
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

if not_found > 0:
    print(missing)
    print(f'{not_found} songs not found')
else:
    print('All songs found')