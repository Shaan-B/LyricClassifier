

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


larkin = open('Larkin1000Albums.txt')
contents = larkin.read()
new = ''
for i in range(len(contents)):
    c = contents[i]
    if c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890. \n':
        new += c
    elif contents[i-2]==' ' and contents[i+2]==' ':
        new += '-'
newlarkin = open('Larkin1000.txt', 'w+')
newlarkin.write(new)
