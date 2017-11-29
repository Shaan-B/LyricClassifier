import webscraper
import requests
import loadsongs

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

l = loadsongs.load('testsongs')
print(l[0].title)
print(l[0].artist)
print(l[0].lyrics)
print(l[0].genres)


#TODO: say that a song is only pop if it doesn't fit any other genre
