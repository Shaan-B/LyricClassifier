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

import webscraper

print(webscraper.getSong('smoke filled room', 'mako').simpleLyrics())
