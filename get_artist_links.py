import pandas as pd
import requests
from bs4 import BeautifulSoup


url = 'https://kworb.net/spotify/artists.html' #url2

#TODO: add header to df

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
parsed_table = soup.find('tbody')
data = [
    [item for i, td in enumerate(row.find_all('td'))
     for item in (
         td.a['href'] if td.find('a') and i == 0 else '',  # Get href only in the first column
         ''.join(td.stripped_strings)  # Text content for every column
     )]
    for row in parsed_table.find_all('tr')
]
df = pd.DataFrame(data, columns=['Link Artist', 'Artist', 'hStreams', 'Streams', 'hDaily', 'Daily', 'hAs lead', 'As lead', 'hSolo', 'Solo', 'hAs feature', 'As feature'])
df.replace('', pd.NA, inplace=True)  # Replace empty strings with NaN
df.dropna(axis=1, how='all', inplace=True)

df.to_csv('data/spotify_artists.csv', index=False)
df[['Artist', 'Link Artist']].to_csv('data/spotify_artists_links.csv', index=False, header=False)
