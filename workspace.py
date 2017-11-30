

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



newlarkin = open('Larkin1000.txt', 'r')
lines = newlarkin.readlines()
for line in lines:
    if ' - ' not in line:
        print(line)
