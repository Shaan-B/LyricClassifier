import loadsongs
import song
from song import Song
import spotifyclient

"""
song_title = 'The 500 Greatest Albums of All Time'
artist_name = 'Rolling'

search_url = webscraper.base_url + "/search"
params = {'q': song_title + " " + artist_name}
response = requests.get(search_url, params=params, headers=webscraper.headers)
json = response.json()
for hit in json["response"]["hits"]:
    if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower(): #requires artist_name is substring of Genius's artist name
        print(hit["result"]["api_path"])
        break
"""

#print(len(loaddata.getAlbumTracks('Yeezus', 'ye')))



#TODO: say that a song is only pop if it doesn't fit any other genre

import loaddata
import loadsongs

def genreDistribution(songs):
    print('Total number of songs:', len(songs))
    genrecounts = {}
    genrecountcounts = {}
    nogenre = 0
    for song in songs:
        if len(song.genres) in genrecountcounts.keys():
            genrecountcounts[len(song.genres)] += 1
        else:
            genrecountcounts[len(song.genres)] = 1
        for genre in song.genres:
            if genre in genrecounts.keys():
                genrecounts[genre] += 1
            else:
                genrecounts[genre] = 1
    for genre in genrecounts:
        print(genre + ': ' + str(genrecounts[genre]))
    print()
    print('Number of genres:')
    for count in genrecountcounts:
        print(str(count) + ': ' + str(genrecountcounts[count]))


#print(loaddata.getAlbumTracks('No Secrets', 'Carly'))
