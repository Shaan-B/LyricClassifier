import song
from loadsongs import *




#This file provides some basic code to get started with.



folder = 'larkin1000_allgenres' #Replace with a folder of .pkl files containg Song objects

#load songs variable with 500 Song objects, using random cluster sampling
songs = load(folder, song.GENRES)
songs = clusteredSample(songs, 500, song.GENRES)

#Print the info for the first 10 songs:
for s in songs[:10]:
    print(s.title, 'by', s.artist+':',s.genres)
print()

#Print the genre frequencies
genreDistribution(songs)
