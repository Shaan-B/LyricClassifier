import song
from loadsongs import *

#This file provides some basic code to get started with.

folder = 'larkin1000_allgenres' #Replace with a folder of .pkl files containg Song objects


#The line below re-creates a dataset from the RockListMusic.com list and loads them into the directory specified by the 'folder' var.
#NOTE: this code takes a very long time to run. If you would like to try it out, we suggest running it overnight.
#It also creates a .txt file containing info for each song, and a log file to store output.
#loadDataFromAlbums(getLarkin1000(), folder, folder + '.txt', folder + '.log')

#load songs variable with 500 Song objects, using random cluster sampling
songs = load(folder, song.GENRES)
songs = clusteredSample(songs, 500, song.GENRES)

#Print the info for the first 10 songs:
for s in songs[:10]:
    print(s.title, 'by', s.artist+':',s.genres)
print()

#Print the genre frequencies
genreDistribution(songs)
