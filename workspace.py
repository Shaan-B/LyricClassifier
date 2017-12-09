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
import os
import glob
import webscraper
import tensorflow
import requests
from autoEncoder import *
from oneHotEncoder import *

g = ['blues', 'country', 'pop', 'rock', 'rap', 'r&b']

songs = loadsongs.load('data/larkin1000_v2', g)#_allgenres', g)
songs = [song for song in songs if song.genres[0] != 'rock']
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


print(genreDistribution(songs))

data = vectorize([song.simpleLyrics() for song in songs], 1)

#print data[0].tolist()

tfidfs = np.array(data)
#posData = vectorize(lyrics2POS([song.simpleLyrics() for song in songs]), 3)
#poss = np.array(vectorize(lyrics2POS([song.simpleLyrics() for song in songs]), 3))
labels = np.array(oneHotEncoder(songs))
for i,_ in enumerate(songs):
    if _.title == 'Homegirl': homeGirl = i
print i


#newTensors = np.array([np.append(tfidfs[i], poss[i]) for i in range(len(tfidfs))])
#model = modelBuilder(len(newTensors.tolist()[0]), 10)
#model.fit(newTensors, labels, n_epoch=100, show_metric=True, batch_size=25)
model = modelBuilder(len(tfidfs.tolist()[0]), 10)
model.fit(tfidfs, np.array(oneHotEncoder(songs)), n_epoch=20, batch_size=50, show_metric=True)
print model.predict(np.array([tfidfs.tolist()[i]]))
#posmodel, posencoder = autoEncoder(len(posData.tolist()[0]), 10)
#posmodel = trainEncoder(poss, posmodel, posencoder)
#possencodings = [posencoder.predict(np.array([pos])).tolist()[0] for pos in poss]

#tf.reset_default_graph()
#tfidfmodel, tfidfencoder = autoEncoder(len(data.tolist()[0]), 10)
#tfidfmodel = trainEncoder(tfidfs, tfidfmodel, tfidfencoder)
#tfidfencodings = [tfidfencoder.predict(np.array([tfidf])).tolist()[0] for tfidf in tfidfs]
#trainX, trainY = np.array(data[:int(len(data) * .66)]), np.array(oneHotEncoder(songs)[:int(len(data) * .66)])
#testX, testY = np.array(data[int(len(data) * .66):]), np.array(oneHotEncoder(songs)[int(len(data) * .66):])
#newTensors = [np.append(tfidfencodings[i], (possencodings[i])) for i in range(len(tfidfencodings))]

tf.reset_default_graph()
#model = modelBuilder(len(tfidfencodings[1]) + len(possencodings[0]), 10)
model = modelBuilder(len(tfidfencodings[1]), 10)
model.fit(np.array(tfidfencodings), labels, n_epoch=20, show_metric=True, batch_size=25)


tf.reset_default_graph()
finalModel = encodeAndTrain(tfidfs, poss, labels, 100, tfidfencoder, posencoder)

#model.fit(trainX, trainY, n_epoch=200, batch_size=50, show_metric=True, validation_set=(testX, testY))

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

#genreDistribution(loadsongs.load('MillionPKLs', g))
