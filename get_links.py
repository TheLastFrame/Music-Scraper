import pandas as pd
import requests
from bs4 import BeautifulSoup


url = 'https://kworb.net/spotify/' 


response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
parsed_table = soup.find('table')

data = [[td.a['href'] if td.find('a') else 
            ''.join(td.stripped_strings)
            for td in row.find_all('td')]
        for row in parsed_table.find_all('tr')]


df = pd.DataFrame(data, columns=['Country', 'Link'])

df['Link'] = df['Link'].apply(lambda x: url + x.split('.')[0]+ '_totals.html')
df.to_csv('data/spotify.csv', index=False)
df['Link'].to_csv('data/spotify_links_only.txt', index=False, header=False)
