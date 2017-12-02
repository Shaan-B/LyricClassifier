from song import *
import webscraper
from preProcessingUtil import *
from classifier import *
import numpy as np
import tflearn
from sklearn import preprocessing
import loadsongs
import song
from song import Song
import spotifyclient
import requests
import loaddata
from autoEncoder import *

def oneHotEncoder(songs):
    genresIndeces = {
    'pop' : 0,
    'rap' : 1,
    'rock' : 2,
    'r&b' : 3,
    'country' : 4,
    'jazz' : 5,
    'blues' : 6,
    'gospel' : 7,
    'reggae' : 8,
    'electronic' : 9 
    }
    encodings = []
    for song in songs:
        if(len(song.genres) >= 1):
        #     zeros  = [0,0,0,0,0,0,0,0]
        #     zeros[genresIndeces[song.genres[0]]] = 1
        # if(len(song.genres > 1)):
            hotVal = 1/len(song.genres)
            zeros  = [ 0 for i in range(len(genreIndeces))]
            for genre in song.genres:
                zeros[genresIndeces[genre]] = hotVal
            encodings.append(zeros)
    return encodings

songs = loadsongs.load('MillionPKLs_v2')
songs = [song for song in songs if(len(song.genres) >= 1)]
songs = [song for song in songs if (song.genres[0] != 'rock')]
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

def filter(songs, genrelist):
	for song in songs:
		newgenres = []
		for genre in song.genres:
			if genre in genrelist:
				newgenres.append(genre)
		song.genres = newgenres


# print("one hots: ", oneHotEncoder(songs)[0])
# print(songs[0].title)
#print(vectorize([song.lyrics for song in songs])[0].tolist())
filter(songs, ["reggae", "rap", "blues", "gospel", "rock", "r&b"])
print(genreDistribution(songs))
data = vectorize(lyrics2POS([song.simpleLyrics() for song in songs if (len(song.genres) > 0)]), 2)
model = modelBuilder(len(data.tolist()[0]), 10)

# model, encoder = autoEncoder(len(data.tolist()[0]), 8)
# trainEncoder(np.array(data[:int(len(data) * .66)]), model, encoder)
trainX, trainY = np.array(data[:int(len(data) * .66)]), np.array(oneHotEncoder(songs)[:int(len(data) * .66)])
testX, testY = np.array(data[int(len(data) * .66):]), np.array(oneHotEncoder(songs)[int(len(data) * .66):])
print(len(testX))
model.fit(trainX, trainY, n_epoch=200, batch_size=50, show_metric=True, validation_set=(testX, testY))
