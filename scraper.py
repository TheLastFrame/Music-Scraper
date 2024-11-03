#%% imports
import os
import bs4
import pandas as pd


#%%
ROOT='data/'

base_sites = [
    'data/spotify_links_only.txt',
    'spotify_top_lists.txt'
]

sites = [
    # ['https://kworb.net/spotify/artists.html', ''],
    ['https://kworb.net/youtube/topvideos.html', ''],
    # ['https://kworb.net/spotify/', '']
]

for site in base_sites:
    with open(site, 'r') as f:
        for line in f:            
            sites.append([line, ''])

#%%

#find table by id and select first index from list of dfs

for site in sites:
    page = site[0]
    id = site[1]

    try:
        if id == '':
            df = pd.read_html(page)[0]
        else:
            df = pd.read_html(page, attrs={'id':id})[0]
    except:
        print(f'Error: {page}')
        continue

    # print('Artist and Title' in df.columns)
    if 'Artist and Title' in df.columns:
        df[['Artist','Song']]=df['Artist and Title'].str.split(' - ', n=1, expand=True)

    os.makedirs(ROOT, exist_ok=True)
    df.to_csv(f"{ROOT+page.split('kworb.net')[-1].split('.')[0].replace('/', '_')}.csv", index = False)







# #split the column by delimiter and creat your expected columns
# df[['Artist','Song']]=df['Artist and Title'].str.split(' - ', n=1, expand=True)

# #pick your columns and export to excel
# df[['Pos','Artist','Song']].to_excel('yourfile.xlsx', index = False)