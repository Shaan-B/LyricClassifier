"""
import loadsongs

loadsongs.save('songlist.txt', 'songs')
s = loadsongs.load('songs')

print(len(s))

for e in s:
    print(e.title, type(e.title))
    print(e.artist, type(e.artist))
    print(e.lyrics, type(e.lyrics))
    print(e.tokens())
    print(e.simpleLyrics())
    print(e.tokenFrequencies())
"""

import spotifyclient
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import pprint

clientid = '80c0be28d7c244148044c27a87653074'
secret = '3b7ff2e371174bd8891b51744c06488f'

client_credentials_manager = SpotifyClientCredentials(clientid, secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

results = sp.search(q='DAMN', limit = 1, type='album')

for i, t in enumerate(results['albums']['items']):
    uri = t['uri']

album = sp.album(uri)


print(album)

print (album['genres'])
