import loadsongs
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

def genreDistribution(songs, genrelist=[]):
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
            if len(genrelist)>0 and genre not in genrelist:
                continue
            if genre in genrecounts.keys():
                genrecounts[genre] += 1
            else:
                genrecounts[genre] = 1
    for genre in sorted(genrecounts.items(), key=lambda x: x[1]):
        print(genre[0] + ': ' + str(genre[1]))
        #print(genre + ': ' + str(genrecounts[genre]))
    print()
    print('Number of genres:')
    for count in genrecountcounts:
        print(str(count) + ': ' + str(genrecountcounts[count]))

g = ['blues', 'punk', 'reggae', 'gospel', 'country', 'pop', 'rock', 'rap', 'r&b', 'electronic', 'jazz']
genreDistribution(loadsongs.load('MillionPKLs', g))

#print(loaddata.getAlbumTracks('No Secrets', 'Carly'))
