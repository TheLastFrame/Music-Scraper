# Music-Scraper
thanks to https://stackoverflow.com/questions/75485470/how-to-scrape-the-specific-text-from-kworb-and-extract-it-as-an-excel-file btw

`get_artist_links.py` -> `get_song_ids.py` -> `merge_songs_with_links.py` -> `get_song_data.py` -> manually add missing data -> `check_song_link_exists.py` -> `clean_kworb_song_data.py` -> `sum_streams_per_week.py`


ToDos:

- [x] download all songs for artists
- [x] check if songs fit the ones we look for
- [x] create xmas song list with rank and spotify ID
- [x] check if weekly data usw is available for ID
    - check daily?
- [x] download weather data
- [x] clean weekly data -> split into positions and streams
- [x] manual adding not matched songs to xmas and breakup list
- [ ] check other spotify dataset (charts.csv) from kaggle, maybe better?
    - and add to weekly sums


Charts Ideas:

- line chart with temp data and occurance of christmas song (zeitraum, median day)
    - [ ] carey & wham herausheben
    - verteilung von christmas zu non christmas songs % von all streams of that week
    - evtl morphing chart year by year to see shift? (climate change)
- [x] vergleich verschiebung von beginn christmas songs zu corona?
    - [x] auch breakup songs
- overlay breakup verteilung mit
    - christmas song streams
    - breakup song streams
- stringency index with top songs at that time        -> scrape
    - or genres?
    - with christmas songs?
    - with breakup songs?
- (top songs (all time) in week of 11 dec -> prove them right or wrong)
    - break up songs 
- word cloud of break up song titles
- sentiment of break up song titles
- 
- [ ] animierte weltkarte wo woche für woche länder aufleuchten in denen christmas songs in den charts sind - avg?
    - all I want for christmas
    - last christmas

(- genre verteilung all time weekly avg?)
- anzahl chart streams per week?
    - also wie vergleich zu warm wochen?

christmas song verteilung im dezember?

ist christmas überhaupt genre nummer 1 in dezember?

wie is die verteilung zu den weihnachtsfeiertagen? % of chart streams



(- (candle) stick chart instead of temp line?)
(- add payment fun fact?)


- gerüst grafik aus facebook breakup daten erstellen?



## Story

**Wie wirkt sich weihnachten auf unser hörverhalten aus?**

1. [x] start of christmas songs in charts worldwide (wenn temp < ?)
    - [ ] all i want for christmas
    - [ ] last christmas
2. [x] start of christmas songs in charts by country mit weltkarte
    - [x] all i want for christmas
    - [ ] last christmas
3. [x] überleitung von nov auf dez? mit verteilung christmas vs non-christmas (ab kw44)
4. [ ] fokus auf dezember
    - [ ] genre nummer 1?
    - [x] weihnachtslieder % of chart streams
    - [x] x von 30 personen (in deinem bim wagon) hören weihnachtslieder
5. [ ] weihnachtstage
    - [ ] sind 24 - 26 weihnachtslieder genre nummer 1?
    - [x] wie viel % der streams machen die songs an den weihnachtstagen aus?
6. [x] wann weihnachtslieder nicht mehr in den charts? - 7. jan last day



## data

popularity csv - https://www.kaggle.com/datasets/pepepython/spotify-huge-database-daily-charts-over-3-years

daily charts - https://www.kaggle.com/datasets/dhruvildave/spotify-charts

## hosting

https://lazy-nanette-fhstpdj-301b7336.koyeb.app/