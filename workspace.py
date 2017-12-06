from loadsongs import *
import loaddata
import song
from song import Song
import spotifyclient
import os
import glob
import hdf5_getters
import webscraper

#loadsongs.convertPKLto2('MillionPKLs', 'MillionPKLs_v2')

#TODO: say that a song is only pop if it doesn't fit any other genre

songs = load('larkin1000_allgenres')
genreDistribution(songs)
songs = clusteredSample(songs, 100, song.GENRES)
genreDistribution(songs)
"""
import spotifyclient
g = ['blues', 'reggae', 'country', 'pop', 'rock', 'rap', 'r&b', 'electronic', 'jazz']
g = song.GENRES
s = loadsongs.load('larkin1000', song.GENRES)
print(genreDistribution(s))
import random
for i in range(len(song.GENRES)):
    for j in range(int(random.random()*len(s)/2), len(s)):
        if g[i] in s[j].genres:
            print(g[i] +': '+ s[j].title +' by ' + s[j].artist)
            break
"""
#print(loadsongs.convertPKLto2('larkin1000', 'larkin1000_v2'))

#print(loaddata.getAlbumTracks('No Secrets', 'Carly'))
